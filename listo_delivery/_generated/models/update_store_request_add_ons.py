from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateStoreRequestAddOns")


@_attrs_define
class UpdateStoreRequestAddOns:
    """Add-ons to switch on (`true`) or off (`false`). Send only the ones
    you are changing: a key you leave out is untouched, and this never
    replaces the set. `wallet` and `full_console` cannot be switched
    on: `true` for either is refused with `422 validation_failed` and
    `param: "add_ons.wallet"` or `"add_ons.full_console"`, and `false`
    is accepted. Each value must be a JSON boolean; the string
    `"true"`, `1` and `null` are refused with `422 validation_failed`
    and `param: "add_ons.<key>"`, and so is a key that is not an add-on.

        Attributes:
            customer_whatsapp (bool | Unset):
            ratings (bool | Unset):
            card_payments (bool | Unset):
            wallet (bool | Unset):
            full_console (bool | Unset):
    """

    customer_whatsapp: bool | Unset = UNSET
    ratings: bool | Unset = UNSET
    card_payments: bool | Unset = UNSET
    wallet: bool | Unset = UNSET
    full_console: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        customer_whatsapp = self.customer_whatsapp

        ratings = self.ratings

        card_payments = self.card_payments

        wallet = self.wallet

        full_console = self.full_console

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if customer_whatsapp is not UNSET:
            field_dict["customer_whatsapp"] = customer_whatsapp
        if ratings is not UNSET:
            field_dict["ratings"] = ratings
        if card_payments is not UNSET:
            field_dict["card_payments"] = card_payments
        if wallet is not UNSET:
            field_dict["wallet"] = wallet
        if full_console is not UNSET:
            field_dict["full_console"] = full_console

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        customer_whatsapp = d.pop("customer_whatsapp", UNSET)

        ratings = d.pop("ratings", UNSET)

        card_payments = d.pop("card_payments", UNSET)

        wallet = d.pop("wallet", UNSET)

        full_console = d.pop("full_console", UNSET)

        update_store_request_add_ons = cls(
            customer_whatsapp=customer_whatsapp,
            ratings=ratings,
            card_payments=card_payments,
            wallet=wallet,
            full_console=full_console,
        )

        return update_store_request_add_ons
