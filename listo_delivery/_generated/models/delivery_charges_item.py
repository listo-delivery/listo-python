from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_charges_item_type import DeliveryChargesItemType

T = TypeVar("T", bound="DeliveryChargesItem")


@_attrs_define
class DeliveryChargesItem:
    """
    Attributes:
        type_ (DeliveryChargesItemType): What the charge was for. `cancellation_fee` is a
            cancellation late enough that a courier was already working
            on the order. `return_fee` is a return trip after a failed
            dropoff, and it bills as ONE entry covering both legs of the
            journey rather than two.
        amount_cents (int): What you were charged, positive, in Mexican peso cents: the
            delivery fee for each leg that was driven, less your own
            store markup.
        charged_at (datetime.datetime): When the charge was recorded, which is not when the delivery
            ended.
    """

    type_: DeliveryChargesItemType
    amount_cents: int
    charged_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        amount_cents = self.amount_cents

        charged_at = self.charged_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "amount_cents": amount_cents,
                "charged_at": charged_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = DeliveryChargesItemType(d.pop("type"))

        amount_cents = d.pop("amount_cents")

        charged_at = datetime.datetime.fromisoformat(d.pop("charged_at"))

        delivery_charges_item = cls(
            type_=type_,
            amount_cents=amount_cents,
            charged_at=charged_at,
        )

        delivery_charges_item.additional_properties = d
        return delivery_charges_item

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
