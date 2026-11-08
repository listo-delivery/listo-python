from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeliveryRequestDropoff")


@_attrs_define
class CreateDeliveryRequestDropoff:
    """Where the order goes, and who receives it.

    Attributes:
        name (str): Who receives the order.
        phone (str): A phone the courier can call, any format that resolves to an E.164 number.
        street (str): The full street address, in one string.
        apt_unit (str | Unset):
        lat (float | Unset): Latitude. Send it together with `lng`, or neither.
        lng (float | Unset): Longitude. Send it together with `lat`, or neither.
        notes (str | Unset): Instructions for the courier at the door, up to 280 characters.
    """

    name: str
    phone: str
    street: str
    apt_unit: str | Unset = UNSET
    lat: float | Unset = UNSET
    lng: float | Unset = UNSET
    notes: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        phone = self.phone

        street = self.street

        apt_unit = self.apt_unit

        lat = self.lat

        lng = self.lng

        notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "phone": phone,
                "street": street,
            }
        )
        if apt_unit is not UNSET:
            field_dict["apt_unit"] = apt_unit
        if lat is not UNSET:
            field_dict["lat"] = lat
        if lng is not UNSET:
            field_dict["lng"] = lng
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        phone = d.pop("phone")

        street = d.pop("street")

        apt_unit = d.pop("apt_unit", UNSET)

        lat = d.pop("lat", UNSET)

        lng = d.pop("lng", UNSET)

        notes = d.pop("notes", UNSET)

        create_delivery_request_dropoff = cls(
            name=name,
            phone=phone,
            street=street,
            apt_unit=apt_unit,
            lat=lat,
            lng=lng,
            notes=notes,
        )

        create_delivery_request_dropoff.additional_properties = d
        return create_delivery_request_dropoff

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
