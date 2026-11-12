from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_plan_type_0_paid_by import StorePlanType0PaidBy
from ..models.store_plan_type_0_status import StorePlanType0Status

T = TypeVar("T", bound="StorePlanType0")


@_attrs_define
class StorePlanType0:
    """The store's Plan Listo, or `null` when the store needs no plan: a
    test store, or a live store created before Plan Listo existed, which
    keeps requesting couriers without one. It is also `null` when the
    store pays its own plan (every store of an account whose stores pay
    their own Plan Listo) and the restaurant has not bought one yet: the
    restaurant buys it in its own console, and there is nothing for you
    to pay or to reactivate. It is also `null` for a store your account
    created itself on Listo's self-serve pricing, which needs no plan (a
    restaurant that connected to such an account keeps its own plan).
    When it is an object every
    key is present, and the ones that do not apply are `null`. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

        Attributes:
            status (StorePlanType0Status): `active` is paid up and renews on `next_charge_on` (null on a
                plan that is passing to the restaurant, see `pending_paid_by`). `past_due`
                has an unpaid month, and its deliveries are refused with `402
                plan_required` until the charge goes through. `awaiting_payment`
                is a store whose first month your balance and card could not
                cover: it holds no plan yet, `price_cents` is the price it
                will be charged before IVA (the amount needed to pay is that
                plus IVA), every date is null, its deliveries are refused with
                `402 plan_required`, and Listo charges it by itself as soon as
                your balance or card covers it. `canceling` was
                canceled and is served up to the day before `ends_on`.
                `canceled` has ended, and can be restarted.
            price_cents (int): What one month of this store's plan costs you, before IVA: your
                price, even while a restaurant that connected to you is still
                paying its own plan. When `paid_by` is `store` because the
                store pays its own plan, it is the price of one `interval` of
                the restaurant's own plan, which is not yours to pay.
                 Example: 199000.
            currency (str):  Example: MXN.
            interval (str): How long one period of this plan is, and the cycle `price_cents`
                is the price of. `month` for every plan you pay. A store that
                pays its own plan reports the interval its restaurant bought,
                so `year` is a restaurant that paid twelve months at once.
                 Example: month.
            current_period_ends_on (datetime.date | None): The last day of the current period, already paid unless
                `status` is `past_due`.
            next_charge_on (datetime.date | None): The day you are charged next: the next renewal, or, while a
                restaurant that connected to you still pays its own plan, your
                first charge. Null once the plan is ending or has ended, and
                null while it is `past_due`: the month owed is charged the
                moment your balance or saved card allows, and retried every
                day until it is paid. Null while `courtesy` is true, too. Null
                as well on a plan you pay that is passing to the restaurant
                (`pending_paid_by` is `store`): you pay the period you are in
                and nothing after it. When `paid_by` is `store` because the
                store pays its own plan, it is the day the restaurant's own plan
                renews, not a charge to you.
            canceled_at (datetime.datetime | None): When you canceled the plan.
            ends_on (datetime.date | None): The day the plan stops serving the store, which is the day after
                the last day paid, or the day a plan whose charge was pending was
                canceled. Null unless the plan is ending or has ended.
            paid_by (StorePlanType0PaidBy): Who pays this plan: `partner`, which is you, or `store`, the
                restaurant itself. `store` is a restaurant that connected to you
                and still pays its own plan, and every store that pays its own
                Plan Listo because your account is set up that way; none of
                those is yours to pay.
            pending_paid_by (None | str): Who will pay it from `pending_paid_by_on`, when that is about to
                change, or null. `partner` is you: a restaurant that connected to
                you and still pays its own plan, until the renewal you pay from.
                `store` is the restaurant: a plan you pay that passes to the
                restaurant at its next renewal because your account is set up so
                that each restaurant pays its own plan. You pay the period you
                are in and nothing after it, so `next_charge_on` is null.
            pending_paid_by_on (datetime.date | None): The date that change lands (the day the new payer's first
                period starts), or null.
            courtesy (bool): `courtesy` is true while Listo waives this store's plan: nothing
                is charged and `next_charge_on` is null.
    """

    status: StorePlanType0Status
    price_cents: int
    currency: str
    interval: str
    current_period_ends_on: datetime.date | None
    next_charge_on: datetime.date | None
    canceled_at: datetime.datetime | None
    ends_on: datetime.date | None
    paid_by: StorePlanType0PaidBy
    pending_paid_by: None | str
    pending_paid_by_on: datetime.date | None
    courtesy: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        price_cents = self.price_cents

        currency = self.currency

        interval = self.interval

        current_period_ends_on: None | str
        if isinstance(self.current_period_ends_on, datetime.date):
            current_period_ends_on = self.current_period_ends_on.isoformat()
        else:
            current_period_ends_on = self.current_period_ends_on

        next_charge_on: None | str
        if isinstance(self.next_charge_on, datetime.date):
            next_charge_on = self.next_charge_on.isoformat()
        else:
            next_charge_on = self.next_charge_on

        canceled_at: None | str
        if isinstance(self.canceled_at, datetime.datetime):
            canceled_at = self.canceled_at.isoformat()
        else:
            canceled_at = self.canceled_at

        ends_on: None | str
        if isinstance(self.ends_on, datetime.date):
            ends_on = self.ends_on.isoformat()
        else:
            ends_on = self.ends_on

        paid_by = self.paid_by.value

        pending_paid_by: None | str
        pending_paid_by = self.pending_paid_by

        pending_paid_by_on: None | str
        if isinstance(self.pending_paid_by_on, datetime.date):
            pending_paid_by_on = self.pending_paid_by_on.isoformat()
        else:
            pending_paid_by_on = self.pending_paid_by_on

        courtesy = self.courtesy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "price_cents": price_cents,
                "currency": currency,
                "interval": interval,
                "current_period_ends_on": current_period_ends_on,
                "next_charge_on": next_charge_on,
                "canceled_at": canceled_at,
                "ends_on": ends_on,
                "paid_by": paid_by,
                "pending_paid_by": pending_paid_by,
                "pending_paid_by_on": pending_paid_by_on,
                "courtesy": courtesy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        status = StorePlanType0Status(d.pop("status"))

        price_cents = d.pop("price_cents")

        currency = d.pop("currency")

        interval = d.pop("interval")

        def _parse_current_period_ends_on(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                current_period_ends_on_type_0 = datetime.date.fromisoformat(data)

                return current_period_ends_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        current_period_ends_on = _parse_current_period_ends_on(
            d.pop("current_period_ends_on")
        )

        def _parse_next_charge_on(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_charge_on_type_0 = datetime.date.fromisoformat(data)

                return next_charge_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        next_charge_on = _parse_next_charge_on(d.pop("next_charge_on"))

        def _parse_canceled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                canceled_at_type_0 = datetime.datetime.fromisoformat(data)

                return canceled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        canceled_at = _parse_canceled_at(d.pop("canceled_at"))

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

        paid_by = StorePlanType0PaidBy(d.pop("paid_by"))

        def _parse_pending_paid_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        pending_paid_by = _parse_pending_paid_by(d.pop("pending_paid_by"))

        def _parse_pending_paid_by_on(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pending_paid_by_on_type_0 = datetime.date.fromisoformat(data)

                return pending_paid_by_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        pending_paid_by_on = _parse_pending_paid_by_on(d.pop("pending_paid_by_on"))

        courtesy = d.pop("courtesy")

        store_plan_type_0 = cls(
            status=status,
            price_cents=price_cents,
            currency=currency,
            interval=interval,
            current_period_ends_on=current_period_ends_on,
            next_charge_on=next_charge_on,
            canceled_at=canceled_at,
            ends_on=ends_on,
            paid_by=paid_by,
            pending_paid_by=pending_paid_by,
            pending_paid_by_on=pending_paid_by_on,
            courtesy=courtesy,
        )

        store_plan_type_0.additional_properties = d
        return store_plan_type_0

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
