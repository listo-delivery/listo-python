"""Turning a webhook payload into the typed event the schema describes."""

from __future__ import annotations

import datetime
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from ._events import EVENT_TYPES, WebhookEvent
from .errors import ListoError

__all__ = [
    "EVENT_TYPES",
    "UnknownEvent",
    "WebhookEvent",
    "parse_event",
    "parse_event_page",
    "parse_event_response",
]


@dataclass
class UnknownEvent:
    """An event whose ``type`` this SDK version does not know.

    The API adds event types without breaking v1, so a receiver must survive
    one. ``data`` is the raw object and ``raw`` the whole payload.
    """

    id: str | None
    type: str | None
    created_at: datetime.datetime | None
    data: Any
    raw: Mapping[str, Any] = field(repr=False)

    @property
    def type_(self) -> str | None:
        """The same value as ``type``, spelled as on the generated event models."""
        return self.type


def _timestamp(value: Any) -> datetime.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return None


def _read_event(payload: Any) -> WebhookEvent | UnknownEvent:
    """The typed event, or an UnknownEvent for a type this version lacks.

    Raises TypeError or ValueError (or KeyError, AttributeError) when the
    payload is not an object, or is a KNOWN type whose body the models cannot
    read. The caller decides which error code that becomes.
    """
    if not isinstance(payload, Mapping):
        raise TypeError("The event payload is not a JSON object.")
    event_class = EVENT_TYPES.get(payload.get("type"))
    if event_class is not None:
        return event_class.from_dict(payload)
    return UnknownEvent(
        id=payload.get("id"),
        type=payload.get("type"),
        created_at=_timestamp(payload.get("created_at")),
        data=payload.get("data"),
        raw=payload,
    )


def parse_event(payload: Any) -> WebhookEvent | UnknownEvent:
    """The typed event for a webhook ``payload``.

    Only a ``type`` this version does not know comes back as an UnknownEvent.
    A known type whose body cannot be read raises ListoError ``invalid_payload``
    (a receiver must not ignore a real event), as does a payload that is not a
    JSON object.
    """
    try:
        return _read_event(payload)
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise ListoError(
            "The event payload does not match the event schema.",
            code="invalid_payload",
            body=payload,
        ) from error


def parse_event_response(payload: Any) -> WebhookEvent | UnknownEvent:
    """The parser for an API response holding one event.

    The same reading as ``parse_event``; its failures are the ones the client
    turns into ``invalid_response``, because here the API sent the payload.
    """
    return _read_event(payload)


def parse_event_page(model: Any) -> Callable[[Any], Any]:
    """A parser for a page model whose ``data`` is a list of webhook events.

    The generated page parser tries each known event class and fails the whole
    page on an event type it does not know; this one reads the items itself.
    """

    def parse(payload: Any) -> Any:
        page = model.from_dict({**payload, "data": []})
        page.data = [_read_event(item) for item in payload["data"]]
        return page

    return parse
