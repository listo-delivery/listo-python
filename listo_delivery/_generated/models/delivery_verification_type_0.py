from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryVerificationType0")


@_attrs_define
class DeliveryVerificationType0:
    """Present only when the order carries a dropoff PIN: when you asked
    for one (`verification.dropoff_pincode` on the create), or when
    Listo requires a PIN on every delivery of this store's account, in
    which case it is present even though you did not ask. `pincode` is
    null until the order is actually dispatched, which is when the code
    is minted.

        Attributes:
            pincode (None | str):
    """

    pincode: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pincode: None | str
        pincode = self.pincode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pincode": pincode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_pincode(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        pincode = _parse_pincode(d.pop("pincode"))

        delivery_verification_type_0 = cls(
            pincode=pincode,
        )

        delivery_verification_type_0.additional_properties = d
        return delivery_verification_type_0

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
