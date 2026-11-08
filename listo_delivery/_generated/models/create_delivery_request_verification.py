from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeliveryRequestVerification")


@_attrs_define
class CreateDeliveryRequestVerification:
    """Proof the customer must give the courier.

    Attributes:
        dropoff_pincode (bool | Unset): True to require a code at the door. Defaults to false.
    """

    dropoff_pincode: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dropoff_pincode = self.dropoff_pincode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dropoff_pincode is not UNSET:
            field_dict["dropoff_pincode"] = dropoff_pincode

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        dropoff_pincode = d.pop("dropoff_pincode", UNSET)

        create_delivery_request_verification = cls(
            dropoff_pincode=dropoff_pincode,
        )

        create_delivery_request_verification.additional_properties = d
        return create_delivery_request_verification

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
