from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.store_add_on import StoreAddOn


T = TypeVar("T", bound="StoreAddOnsType0")


@_attrs_define
class StoreAddOnsType0:
    """The store's paid add-ons, or `null` when the store cannot hold any.
    On Listo's self-serve pricing, the stores your account created itself
    can hold add-ons; any other store shows `add_ons: null`.
    When it is an object it has all five keys, each with every field.
    Switch them on and off with `PATCH /v1/stores/{id}`. `wallet` and
    `full_console` change the store's `access_tier` and are for live
    stores: on a test store they read `available: false`. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

        Attributes:
            customer_whatsapp (StoreAddOn): One paid add-on of a store and where it stands. `customer_whatsapp`
                sends the customer WhatsApp updates on each delivered trip, `ratings`
                gives you the customer's rating of the food on the delivery (`rating`)
                and sends a `delivery.rated` event, for the ratings given while it is on;
                `card_payments` lets the store take
                card payments, `wallet` gives the store its own balance, and
                `full_console` gives the store its own console and its Plan Listo.
            ratings (StoreAddOn): One paid add-on of a store and where it stands. `customer_whatsapp`
                sends the customer WhatsApp updates on each delivered trip, `ratings`
                gives you the customer's rating of the food on the delivery (`rating`)
                and sends a `delivery.rated` event, for the ratings given while it is on;
                `card_payments` lets the store take
                card payments, `wallet` gives the store its own balance, and
                `full_console` gives the store its own console and its Plan Listo.
            card_payments (StoreAddOn): One paid add-on of a store and where it stands. `customer_whatsapp`
                sends the customer WhatsApp updates on each delivered trip, `ratings`
                gives you the customer's rating of the food on the delivery (`rating`)
                and sends a `delivery.rated` event, for the ratings given while it is on;
                `card_payments` lets the store take
                card payments, `wallet` gives the store its own balance, and
                `full_console` gives the store its own console and its Plan Listo.
            wallet (StoreAddOn): One paid add-on of a store and where it stands. `customer_whatsapp`
                sends the customer WhatsApp updates on each delivered trip, `ratings`
                gives you the customer's rating of the food on the delivery (`rating`)
                and sends a `delivery.rated` event, for the ratings given while it is on;
                `card_payments` lets the store take
                card payments, `wallet` gives the store its own balance, and
                `full_console` gives the store its own console and its Plan Listo.
            full_console (StoreAddOn): One paid add-on of a store and where it stands. `customer_whatsapp`
                sends the customer WhatsApp updates on each delivered trip, `ratings`
                gives you the customer's rating of the food on the delivery (`rating`)
                and sends a `delivery.rated` event, for the ratings given while it is on;
                `card_payments` lets the store take
                card payments, `wallet` gives the store its own balance, and
                `full_console` gives the store its own console and its Plan Listo.
    """

    customer_whatsapp: StoreAddOn
    ratings: StoreAddOn
    card_payments: StoreAddOn
    wallet: StoreAddOn
    full_console: StoreAddOn
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_whatsapp = self.customer_whatsapp.to_dict()

        ratings = self.ratings.to_dict()

        card_payments = self.card_payments.to_dict()

        wallet = self.wallet.to_dict()

        full_console = self.full_console.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_whatsapp": customer_whatsapp,
                "ratings": ratings,
                "card_payments": card_payments,
                "wallet": wallet,
                "full_console": full_console,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.store_add_on import StoreAddOn

        d = dict(src_dict)
        customer_whatsapp = StoreAddOn.from_dict(d.pop("customer_whatsapp"))

        ratings = StoreAddOn.from_dict(d.pop("ratings"))

        card_payments = StoreAddOn.from_dict(d.pop("card_payments"))

        wallet = StoreAddOn.from_dict(d.pop("wallet"))

        full_console = StoreAddOn.from_dict(d.pop("full_console"))

        store_add_ons_type_0 = cls(
            customer_whatsapp=customer_whatsapp,
            ratings=ratings,
            card_payments=card_payments,
            wallet=wallet,
            full_console=full_console,
        )

        store_add_ons_type_0.additional_properties = d
        return store_add_ons_type_0

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
