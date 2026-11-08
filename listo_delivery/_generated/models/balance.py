from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.balance_currency import BalanceCurrency

if TYPE_CHECKING:
    from ..models.same_day_terms import SameDayTerms


T = TypeVar("T", bound="Balance")


@_attrs_define
class Balance:
    """Your prepaid balance for the world the key acts in.

    Attributes:
        balance_cents (int): Everything in the account, in centavos.
        available_cents (int): What you can withdraw today. Spending is not gated on it.
        currency (BalanceCurrency):
        same_day (SameDayTerms): What a `same_day` withdrawal would cost you and how large a one you
            could ask for, right now. Every field is always present.
        in_review_cents (int): The part of `balance_cents` that is cash from an order we are still
            reviewing. `0` when nothing is under review. Already left out of
            `available_cents`, and a delivery cannot be paid from it.
    """

    balance_cents: int
    available_cents: int
    currency: BalanceCurrency
    same_day: SameDayTerms
    in_review_cents: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balance_cents = self.balance_cents

        available_cents = self.available_cents

        currency = self.currency.value

        same_day = self.same_day.to_dict()

        in_review_cents = self.in_review_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "balance_cents": balance_cents,
                "available_cents": available_cents,
                "currency": currency,
                "same_day": same_day,
                "in_review_cents": in_review_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.same_day_terms import SameDayTerms

        d = dict(src_dict)
        balance_cents = d.pop("balance_cents")

        available_cents = d.pop("available_cents")

        currency = BalanceCurrency(d.pop("currency"))

        same_day = SameDayTerms.from_dict(d.pop("same_day"))

        in_review_cents = d.pop("in_review_cents")

        balance = cls(
            balance_cents=balance_cents,
            available_cents=available_cents,
            currency=currency,
            same_day=same_day,
            in_review_cents=in_review_cents,
        )

        balance.additional_properties = d
        return balance

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
