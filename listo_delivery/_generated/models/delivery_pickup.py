from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryPickup")


@_attrs_define
class DeliveryPickup:
    """Where the courier collects, snapshotted at create, so a historical
    order keeps reporting where the courier actually went even after the
    store is renamed or moved.

        Attributes:
            name (str):
            street (str):
            lat (float | None):
            lng (float | None):
            notes (None | str): The store's standing pickup instructions, not a per-order value.
    """

    name: str
    street: str
    lat: float | None
    lng: float | None
    notes: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        street = self.street

        lat: float | None
        lat = self.lat

        lng: float | None
        lng = self.lng

        notes: None | str
        notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "street": street,
                "lat": lat,
                "lng": lng,
                "notes": notes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        street = d.pop("street")

        def _parse_lat(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        lat = _parse_lat(d.pop("lat"))

        def _parse_lng(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        lng = _parse_lng(d.pop("lng"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        delivery_pickup = cls(
            name=name,
            street=street,
            lat=lat,
            lng=lng,
            notes=notes,
        )

        delivery_pickup.additional_properties = d
        return delivery_pickup

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
