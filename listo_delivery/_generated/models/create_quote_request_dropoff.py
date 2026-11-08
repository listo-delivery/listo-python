from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateQuoteRequestDropoff")


@_attrs_define
class CreateQuoteRequestDropoff:
    """Where the order goes.

    Attributes:
        street (str): The full street address, in one string.
        apt_unit (str | Unset):
        lat (float | Unset): Latitude. Send it together with `lng`, or neither.
        lng (float | Unset): Longitude. Send it together with `lat`, or neither.
    """

    street: str
    apt_unit: str | Unset = UNSET
    lat: float | Unset = UNSET
    lng: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        street = self.street

        apt_unit = self.apt_unit

        lat = self.lat

        lng = self.lng

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "street": street,
            }
        )
        if apt_unit is not UNSET:
            field_dict["apt_unit"] = apt_unit
        if lat is not UNSET:
            field_dict["lat"] = lat
        if lng is not UNSET:
            field_dict["lng"] = lng

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        street = d.pop("street")

        apt_unit = d.pop("apt_unit", UNSET)

        lat = d.pop("lat", UNSET)

        lng = d.pop("lng", UNSET)

        create_quote_request_dropoff = cls(
            street=street,
            apt_unit=apt_unit,
            lat=lat,
            lng=lng,
        )

        create_quote_request_dropoff.additional_properties = d
        return create_quote_request_dropoff

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
