from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_status_changed_event_type import DeliveryStatusChangedEventType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery import Delivery


T = TypeVar("T", bound="DeliveryStatusChangedEvent")


@_attrs_define
class DeliveryStatusChangedEvent:
    """
    Attributes:
        id (str): The event id, `evt_` prefixed. Dedupe on this. Example: evt_9pQ2vX7mKdR4tYb1nZ3sLwCe.
        created_at (datetime.datetime): When the event was recorded, ISO-8601 in UTC. Example: 2026-07-28T18:41:03Z.
        type_ (DeliveryStatusChangedEventType): Which event this is.
        data (Delivery): The shape of a delivery: every field the object can carry, with the
            nullability each one really has. It is the response of every operation
            that answers a delivery (the create, the fetch, a list row, the
            reschedule, the cancel, the retry and the refund) and the `data` of
            every full delivery event, so ONE type holds all of them.

            Every operation returns the whole object. A field that a given call
            cannot yet have is present and null rather than missing: a create
            response has a null `courier`, because no courier has been assigned
            yet, and a reschedule only ever answers with a still-scheduled order,
            so its `delivered_at` is null.

            Money is integer centavos, timestamps are ISO-8601 in UTC, and every
            enum below is ours rather than a passthrough of anyone else's.
        test (bool | Unset): Present, and true, only on a test event you asked for with
            `POST /v1/test_webhooks`. A real event does not carry the field at
            all. A test event's `data` is a sample whose ids resolve to nothing.
             Example: True.
    """

    id: str
    created_at: datetime.datetime
    type_: DeliveryStatusChangedEventType
    data: Delivery
    test: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_at = self.created_at.isoformat()

        type_ = self.type_.value

        data = self.data.to_dict()

        test = self.test

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "type": type_,
                "data": data,
            }
        )
        if test is not UNSET:
            field_dict["test"] = test

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery import Delivery

        d = dict(src_dict)
        id = d.pop("id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        type_ = DeliveryStatusChangedEventType(d.pop("type"))

        data = Delivery.from_dict(d.pop("data"))

        test = d.pop("test", UNSET)

        delivery_status_changed_event = cls(
            id=id,
            created_at=created_at,
            type_=type_,
            data=data,
            test=test,
        )

        delivery_status_changed_event.additional_properties = d
        return delivery_status_changed_event

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
