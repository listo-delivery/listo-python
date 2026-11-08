from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEventEnvelope")


@_attrs_define
class WebhookEventEnvelope:
    """The fields every event shares. Delivery is at-least-once and unordered
    by design: dedupe on `id`, and order by `created_at` or by the object's
    own timestamps rather than by arrival. `type` and `data` are added by
    each event, because their values depend on which event it is.

        Attributes:
            id (str): The event id, `evt_` prefixed. Dedupe on this. Example: evt_9pQ2vX7mKdR4tYb1nZ3sLwCe.
            created_at (datetime.datetime): When the event was recorded, ISO-8601 in UTC. Example: 2026-07-28T18:41:03Z.
            test (bool | Unset): Present, and true, only on a test event you asked for with
                `POST /v1/test_webhooks`. A real event does not carry the field at
                all. A test event's `data` is a sample whose ids resolve to nothing.
                 Example: True.
    """

    id: str
    created_at: datetime.datetime
    test: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        test = self.test

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
            }
        )
        if test is not UNSET:
            field_dict["test"] = test

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        test = d.pop("test", UNSET)

        webhook_event_envelope = cls(
            id=id,
            created_at=created_at,
            test=test,
        )

        webhook_event_envelope.additional_properties = d
        return webhook_event_envelope

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
