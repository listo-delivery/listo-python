from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RefundDeliveryRequest")


@_attrs_define
class RefundDeliveryRequest:
    """How much of the order to refund. Both fields are optional.

    Attributes:
        amount_cents (int | Unset): A smaller amount than the whole, in centavos. Leave it out to refund what is left.
        reason (str | Unset): Why the refund is being made, up to 500 characters.
    """

    amount_cents: int | Unset = UNSET
    reason: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount_cents is not UNSET:
            field_dict["amount_cents"] = amount_cents
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents", UNSET)

        reason = d.pop("reason", UNSET)

        refund_delivery_request = cls(
            amount_cents=amount_cents,
            reason=reason,
        )

        refund_delivery_request.additional_properties = d
        return refund_delivery_request

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
