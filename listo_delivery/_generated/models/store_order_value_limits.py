from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StoreOrderValueLimits")


@_attrs_define
class StoreOrderValueLimits:
    """The most an order may be worth at this store right now, per payment
    type. A request above it is refused with `order_value_over_cap`
    (prepaid and card) or `cash_over_cap` (cash). The limits can change
    without a `store.updated` event, for example during a special limit,
    so read them from the store when you need them.

        Attributes:
            prepaid_max_cents (int): The most an order you record as already paid (`prepaid`) may be
                worth at this store, in cents.
            card_max_cents (int): The most the food of an order paid by card link may be worth at
                this store, in cents. The delivery fee does not count toward it.
            cash_max_cents (int): The most the courier may collect in cash at this store (the order value plus the
                customer's share of the fee), in cents.
    """

    prepaid_max_cents: int
    card_max_cents: int
    cash_max_cents: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prepaid_max_cents = self.prepaid_max_cents

        card_max_cents = self.card_max_cents

        cash_max_cents = self.cash_max_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prepaid_max_cents": prepaid_max_cents,
                "card_max_cents": card_max_cents,
                "cash_max_cents": cash_max_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        prepaid_max_cents = d.pop("prepaid_max_cents")

        card_max_cents = d.pop("card_max_cents")

        cash_max_cents = d.pop("cash_max_cents")

        store_order_value_limits = cls(
            prepaid_max_cents=prepaid_max_cents,
            card_max_cents=card_max_cents,
            cash_max_cents=cash_max_cents,
        )

        store_order_value_limits.additional_properties = d
        return store_order_value_limits

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
