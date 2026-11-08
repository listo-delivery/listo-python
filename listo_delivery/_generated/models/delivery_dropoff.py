from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_dropoff_handoff import DeliveryDropoffHandoff

T = TypeVar("T", bound="DeliveryDropoff")


@_attrs_define
class DeliveryDropoff:
    """Where the courier delivers, echoed back as you sent it.

    Attributes:
        name (str):
        phone (str): E.164, normalized on the way in. Example: +528112345678.
        street (str):
        apt_unit (None | str):
        lat (float | None): Null when the address was never geocoded and the text was judged
            instead. Never a fabricated zero.
        lng (float | None):
        notes (None | str):
        handoff (DeliveryDropoffHandoff):
    """

    name: str
    phone: str
    street: str
    apt_unit: None | str
    lat: float | None
    lng: float | None
    notes: None | str
    handoff: DeliveryDropoffHandoff
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        phone = self.phone

        street = self.street

        apt_unit: None | str
        apt_unit = self.apt_unit

        lat: float | None
        lat = self.lat

        lng: float | None
        lng = self.lng

        notes: None | str
        notes = self.notes

        handoff = self.handoff.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "phone": phone,
                "street": street,
                "apt_unit": apt_unit,
                "lat": lat,
                "lng": lng,
                "notes": notes,
                "handoff": handoff,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        phone = d.pop("phone")

        street = d.pop("street")

        def _parse_apt_unit(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        apt_unit = _parse_apt_unit(d.pop("apt_unit"))

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

        handoff = DeliveryDropoffHandoff(d.pop("handoff"))

        delivery_dropoff = cls(
            name=name,
            phone=phone,
            street=street,
            apt_unit=apt_unit,
            lat=lat,
            lng=lng,
            notes=notes,
            handoff=handoff,
        )

        delivery_dropoff.additional_properties = d
        return delivery_dropoff

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
