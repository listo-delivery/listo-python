from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryCourierType0PhoneType0")


@_attrs_define
class DeliveryCourierType0PhoneType0:
    """A masked number and its IVR PIN, never a personal number. Dial
    `masked` and enter `pin` when the system asks. Null when no
    number has been issued for this courier.

        Attributes:
            masked (str):
            pin (None | str):
    """

    masked: str
    pin: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        masked = self.masked

        pin: None | str
        pin = self.pin

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "masked": masked,
                "pin": pin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        masked = d.pop("masked")

        def _parse_pin(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        pin = _parse_pin(d.pop("pin"))

        delivery_courier_type_0_phone_type_0 = cls(
            masked=masked,
            pin=pin,
        )

        delivery_courier_type_0_phone_type_0.additional_properties = d
        return delivery_courier_type_0_phone_type_0

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
