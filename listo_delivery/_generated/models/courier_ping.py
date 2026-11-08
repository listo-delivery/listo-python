from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.courier_ping_location import CourierPingLocation


T = TypeVar("T", bound="CourierPing")


@_attrs_define
class CourierPing:
    """The reduced body of a `delivery.courier_location` event. Correlate it
    with a delivery you already hold; it is not the delivery object.

        Attributes:
            delivery_id (str): The `dlv_` id of the delivery the courier is carrying.
            external_id (None | str): Your own reference for that delivery, so you need not store ours.
            location (CourierPingLocation):
            updated_at (datetime.datetime | None): When this position was last confirmed, which is not the same as when
                the event was sent.
    """

    delivery_id: str
    external_id: None | str
    location: CourierPingLocation
    updated_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivery_id = self.delivery_id

        external_id: None | str
        external_id = self.external_id

        location = self.location.to_dict()

        updated_at: None | str
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_id": delivery_id,
                "external_id": external_id,
                "location": location,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.courier_ping_location import CourierPingLocation

        d = dict(src_dict)
        delivery_id = d.pop("delivery_id")

        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("external_id"))

        location = CourierPingLocation.from_dict(d.pop("location"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updated_at"))

        courier_ping = cls(
            delivery_id=delivery_id,
            external_id=external_id,
            location=location,
            updated_at=updated_at,
        )

        courier_ping.additional_properties = d
        return courier_ping

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
