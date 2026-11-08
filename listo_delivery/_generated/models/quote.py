from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quote_currency import QuoteCurrency
from ..models.quote_vehicle import QuoteVehicle

T = TypeVar("T", bound="Quote")


@_attrs_define
class Quote:
    """A delivery priced and held for a short while. Hand `id` to
    `POST /v1/deliveries` as `quote_id` to book at exactly this price.

        Attributes:
            id (str): The quote id, `qt_` prefixed. Example: qt_5nW3jP8vT2xQ6bM9cZ1sRdKe.
            fee_cents (int): The total delivery fee, in centavos, and the number a booking
                against this quote is held to. `business_fee_cents` plus
                `customer_fee_cents` always add back to it.
            business_fee_cents (int): The part of the fee the store pays.
            customer_fee_cents (int): The part of the fee the customer pays.
            cash_to_collect_cents (int | None): What the courier collects at the door on a cash order: the order
                value plus the customer's share of the fee. Null on every quote
                that is not a cash quote, which is not the same as `0` (a cash
                order that collects nothing).
            currency (QuoteCurrency): Always `MXN`; money is integer centavos.
            pickup_duration_min (int | None): Minutes until a courier is expected at the store, when the quote
                came back with an estimate. Null otherwise.
            dropoff_eta_at (datetime.datetime | None): When the order is expected at the door, when the quote came back with
                an estimate. Null otherwise.
            expires_at (datetime.datetime): The deadline for booking this price. Past it, a create answers
                `quote_expired` and you quote again.
            test (bool): Whether the quote belongs to the sandbox world.
            created_at (datetime.datetime):
            vehicle (QuoteVehicle): What this price was built for: `car` when you asked for one or an
                item was sized `xlarge`, `moto` otherwise. Always present.
                 Example: moto.
    """

    id: str
    fee_cents: int
    business_fee_cents: int
    customer_fee_cents: int
    cash_to_collect_cents: int | None
    currency: QuoteCurrency
    pickup_duration_min: int | None
    dropoff_eta_at: datetime.datetime | None
    expires_at: datetime.datetime
    test: bool
    created_at: datetime.datetime
    vehicle: QuoteVehicle
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        fee_cents = self.fee_cents

        business_fee_cents = self.business_fee_cents

        customer_fee_cents = self.customer_fee_cents

        cash_to_collect_cents: int | None
        cash_to_collect_cents = self.cash_to_collect_cents

        currency = self.currency.value

        pickup_duration_min: int | None
        pickup_duration_min = self.pickup_duration_min

        dropoff_eta_at: None | str
        if isinstance(self.dropoff_eta_at, datetime.datetime):
            dropoff_eta_at = self.dropoff_eta_at.isoformat()
        else:
            dropoff_eta_at = self.dropoff_eta_at

        expires_at = self.expires_at.isoformat()

        test = self.test

        created_at = self.created_at.isoformat()

        vehicle = self.vehicle.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "fee_cents": fee_cents,
                "business_fee_cents": business_fee_cents,
                "customer_fee_cents": customer_fee_cents,
                "cash_to_collect_cents": cash_to_collect_cents,
                "currency": currency,
                "pickup_duration_min": pickup_duration_min,
                "dropoff_eta_at": dropoff_eta_at,
                "expires_at": expires_at,
                "test": test,
                "created_at": created_at,
                "vehicle": vehicle,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        fee_cents = d.pop("fee_cents")

        business_fee_cents = d.pop("business_fee_cents")

        customer_fee_cents = d.pop("customer_fee_cents")

        def _parse_cash_to_collect_cents(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cash_to_collect_cents = _parse_cash_to_collect_cents(
            d.pop("cash_to_collect_cents")
        )

        currency = QuoteCurrency(d.pop("currency"))

        def _parse_pickup_duration_min(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        pickup_duration_min = _parse_pickup_duration_min(d.pop("pickup_duration_min"))

        def _parse_dropoff_eta_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                dropoff_eta_at_type_0 = datetime.datetime.fromisoformat(data)

                return dropoff_eta_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        dropoff_eta_at = _parse_dropoff_eta_at(d.pop("dropoff_eta_at"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        test = d.pop("test")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        vehicle = QuoteVehicle(d.pop("vehicle"))

        quote = cls(
            id=id,
            fee_cents=fee_cents,
            business_fee_cents=business_fee_cents,
            customer_fee_cents=customer_fee_cents,
            cash_to_collect_cents=cash_to_collect_cents,
            currency=currency,
            pickup_duration_min=pickup_duration_min,
            dropoff_eta_at=dropoff_eta_at,
            expires_at=expires_at,
            test=test,
            created_at=created_at,
            vehicle=vehicle,
        )

        quote.additional_properties = d
        return quote

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
