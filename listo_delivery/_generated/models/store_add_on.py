from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_add_on_charged import StoreAddOnCharged
from ..models.store_add_on_status import StoreAddOnStatus

T = TypeVar("T", bound="StoreAddOn")


@_attrs_define
class StoreAddOn:
    """One paid add-on of a store and where it stands. `customer_whatsapp`
    sends the customer WhatsApp updates on each delivered trip, `ratings`
    lets customers rate the delivery, `card_payments` lets the store take
    card payments, `wallet` gives the store its own balance, and
    `full_console` gives the store its own console and its Plan Listo.

        Attributes:
            status (StoreAddOnStatus): `off` is not switched on. `on` is switched on. `ending` is a monthly
                add-on you switched off that keeps running until `ends_on`, the end
                of the month already paid (`ends_on` is null only while a payment
                for the next month is still being confirmed). `scheduled` is a monthly add-on that
                starts when a month already running ends (`wallet` switched on
                while `full_console` is running out). `past_due` is `full_console`
                only: its renewal was refused and it is being retried, and the store
                is still served meanwhile.
            price_cents (int): What the add-on costs, in cents before IVA: per month for a
                `monthly` add-on and per use for the other two. While it is off this
                is today's price; once it is on it is the price it was switched on at.
                 Example: 9900.
            charged (StoreAddOnCharged): How it is charged. `per_delivered_trip` is once for each trip that
                is delivered, `per_paid_payment` once for each card payment that is
                paid, and `monthly` is a month up front, charged when you switch it
                on and again on `renews_on`.
            renews_on (datetime.date | None): The day a monthly add-on is charged next. Null unless the add-on is
                `on` and monthly, and also null while its renewal payment is being
                confirmed: a payment for its next month has been started and the new
                date is not known until that payment resolves (it then renews a
                month later if it was paid, or the add-on ends if it was not). On the
                renewal day itself, before any payment has been started, it is that
                day.
            ends_on (datetime.date | None): The last day an `ending` add-on runs. Null in every other status.
                For an `ending` add-on it is null ONLY while a payment is still
                being confirmed: its month was due to renew when you switched it
                off, a payment for the next month was started, and the end date is
                not known until that payment resolves (it then ends at the end of
                that month if it was paid, or at once if it was not). With no
                payment pending it is always the last day of the month already
                paid, including the hours after that day has passed and before the
                add-on is ended.
            available (bool): Whether this add-on can be switched on for the store. `false` for
                `wallet` and `full_console` on every store: they cannot be switched
                on, and asking to is refused with `422 validation_failed`. `true`
                for the other three.
    """

    status: StoreAddOnStatus
    price_cents: int
    charged: StoreAddOnCharged
    renews_on: datetime.date | None
    ends_on: datetime.date | None
    available: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        price_cents = self.price_cents

        charged = self.charged.value

        renews_on: None | str
        if isinstance(self.renews_on, datetime.date):
            renews_on = self.renews_on.isoformat()
        else:
            renews_on = self.renews_on

        ends_on: None | str
        if isinstance(self.ends_on, datetime.date):
            ends_on = self.ends_on.isoformat()
        else:
            ends_on = self.ends_on

        available = self.available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "price_cents": price_cents,
                "charged": charged,
                "renews_on": renews_on,
                "ends_on": ends_on,
                "available": available,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = StoreAddOnStatus(d.pop("status"))

        price_cents = d.pop("price_cents")

        charged = StoreAddOnCharged(d.pop("charged"))

        def _parse_renews_on(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                renews_on_type_0 = datetime.date.fromisoformat(data)

                return renews_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        renews_on = _parse_renews_on(d.pop("renews_on"))

        def _parse_ends_on(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ends_on_type_0 = datetime.date.fromisoformat(data)

                return ends_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        ends_on = _parse_ends_on(d.pop("ends_on"))

        available = d.pop("available")

        store_add_on = cls(
            status=status,
            price_cents=price_cents,
            charged=charged,
            renews_on=renews_on,
            ends_on=ends_on,
            available=available,
        )

        store_add_on.additional_properties = d
        return store_add_on

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
