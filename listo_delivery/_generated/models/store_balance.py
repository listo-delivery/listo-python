from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_balance_billing import StoreBalanceBilling
from ..models.store_balance_currency import StoreBalanceCurrency

T = TypeVar("T", bound="StoreBalance")


@_attrs_define
class StoreBalance:
    """One store's balance, for the store's own billing.

    Attributes:
        balance_cents (int):
        available_cents (int):
        currency (StoreBalanceCurrency):
        billing (StoreBalanceBilling): Whose balance pays this store's deliveries. A `partner` store has
            no balance of its own and these figures describe the account that
            pays for it.
        in_review_cents (int): The part of `balance_cents` that is cash from an order we are still reviewing.
    """

    balance_cents: int
    available_cents: int
    currency: StoreBalanceCurrency
    billing: StoreBalanceBilling
    in_review_cents: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance_cents = self.balance_cents

        available_cents = self.available_cents

        currency = self.currency.value

        billing = self.billing.value

        in_review_cents = self.in_review_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "balance_cents": balance_cents,
                "available_cents": available_cents,
                "currency": currency,
                "billing": billing,
                "in_review_cents": in_review_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        balance_cents = d.pop("balance_cents")

        available_cents = d.pop("available_cents")

        currency = StoreBalanceCurrency(d.pop("currency"))

        billing = StoreBalanceBilling(d.pop("billing"))

        in_review_cents = d.pop("in_review_cents")

        store_balance = cls(
            balance_cents=balance_cents,
            available_cents=available_cents,
            currency=currency,
            billing=billing,
            in_review_cents=in_review_cents,
        )

        store_balance.additional_properties = d
        return store_balance

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
