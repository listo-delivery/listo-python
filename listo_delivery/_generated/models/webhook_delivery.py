from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_delivery_event_type import WebhookDeliveryEventType

T = TypeVar("T", bound="WebhookDelivery")


@_attrs_define
class WebhookDelivery:
    """One attempt to POST an event to your webhook URL, and what came back. An
    event has one attempt per try: the first send, each automatic retry, and
    each resend you asked for.

        Attributes:
            id (str): The attempt's id, `whd_` prefixed. Example: whd_8d2e5f1a7c3b9046a1b2c3d4.
            event_id (str): The event this was an attempt to deliver, `evt_` prefixed. Example:
                evt_9pQ2vX7mKdR4tYb1nZ3sLwCe.
            event_type (WebhookDeliveryEventType): The type of that event.
            attempt (int): Which attempt this is for the event, counted from 1 in the order they
                were made. A resend continues the count.
                 Example: 1.
            resent (bool): True when you asked for this attempt (`POST /v1/events/{id}/resend`) rather than Listo making it
                on its own schedule.
            url (str): The URL that was posted to, as it was when the attempt was made. Example:
                https://example.com/listo/webhooks.
            status_code (int | None): The HTTP status your endpoint answered with. Null when nothing answered at all (a
                timeout, a refused connection, a certificate error); `error_message` says which. Example: 200.
            error_message (None | str): Why the attempt counted as failed, in words (a timeout, a refused connection, a
                non-2xx status). Null on a successful attempt.
            response_body (None | str): The first 500 characters of the body your endpoint answered with. Null when nothing
                answered or the body was empty. Example: ok.
            duration_ms (int | None): How long the attempt took, in milliseconds. Null when it was not measured. Example:
                84.
            succeeded (bool): True when your endpoint answered with a 2xx. Anything else is retried, unless the attempt was
                a resend or the event is a courier position.
            created_at (datetime.datetime): When the attempt was made, ISO-8601 in UTC. Example: 2026-11-06T16:04:31Z.
    """

    id: str
    event_id: str
    event_type: WebhookDeliveryEventType
    attempt: int
    resent: bool
    url: str
    status_code: int | None
    error_message: None | str
    response_body: None | str
    duration_ms: int | None
    succeeded: bool
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        event_type = self.event_type.value

        attempt = self.attempt

        resent = self.resent

        url = self.url

        status_code: int | None
        status_code = self.status_code

        error_message: None | str
        error_message = self.error_message

        response_body: None | str
        response_body = self.response_body

        duration_ms: int | None
        duration_ms = self.duration_ms

        succeeded = self.succeeded

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "event_type": event_type,
                "attempt": attempt,
                "resent": resent,
                "url": url,
                "status_code": status_code,
                "error_message": error_message,
                "response_body": response_body,
                "duration_ms": duration_ms,
                "succeeded": succeeded,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("event_id")

        event_type = WebhookDeliveryEventType(d.pop("event_type"))

        attempt = d.pop("attempt")

        resent = d.pop("resent")

        url = d.pop("url")

        def _parse_status_code(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        status_code = _parse_status_code(d.pop("status_code"))

        def _parse_error_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_message = _parse_error_message(d.pop("error_message"))

        def _parse_response_body(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        response_body = _parse_response_body(d.pop("response_body"))

        def _parse_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms"))

        succeeded = d.pop("succeeded")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        webhook_delivery = cls(
            id=id,
            event_id=event_id,
            event_type=event_type,
            attempt=attempt,
            resent=resent,
            url=url,
            status_code=status_code,
            error_message=error_message,
            response_body=response_body,
            duration_ms=duration_ms,
            succeeded=succeeded,
            created_at=created_at,
        )

        webhook_delivery.additional_properties = d
        return webhook_delivery

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
