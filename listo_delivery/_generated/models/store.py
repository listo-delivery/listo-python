from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_access_tier import StoreAccessTier
from ..models.store_billing import StoreBilling
from ..models.store_default_fee_split_mode import StoreDefaultFeeSplitMode

if TYPE_CHECKING:
    from ..models.store_add_ons_type_0 import StoreAddOnsType0
    from ..models.store_order_value_limits import StoreOrderValueLimits
    from ..models.store_plan_type_0 import StorePlanType0


T = TypeVar("T", bound="Store")


@_attrs_define
class Store:
    """A pickup location. Card readiness is deliberately NOT a field here: it
    is its own endpoint, with its own outstanding-requirements detail.

        Attributes:
            id (str): The store id, `st_` prefixed. Example: st_4bR8kM2wQ7xT1nV5cZ9pLdYe.
            external_id (None | str): Your own reference for this location, if you sent one. Unique per
                key world, and filterable on the list, so you can reconcile against
                your own store book without storing our ids.
                 Example: pos-store-41.
            name (str): The name you gave the store; for a restaurant that connected an
                account with several branches, the business and the branch, the way
                its own customers read it (`Tortería La Mera Mera, Zapopan`). A
                branch whose own name already begins with the business's name, such
                as `Tortería La Mera Mera Centro`, is published as it is. When
                you send a name, a value that begins with the store's business name
                and a comma is read as that business plus the branch, so sending back
                the name you read changes nothing.
            phone (str): E.164, normalized on the way in.
            street (str):
            apt_unit (None | str):
            lat (float | None):
            lng (float | None):
            pickup_notes (None | str): Standing instructions for the courier collecting here.
            timezone (str): The IANA zone the store keeps its hours in, normalized to one
                spelling per zone. Derived from the store's coordinates, and
                re-derived whenever the store's position moves. A zone you send
                yourself is used only when the position cannot answer (a store with
                no coordinates, or a position no zone claims), and one that
                disagrees with the position is neither stored nor treated as an
                error.
                 Example: America/Mexico_City.
            default_business_fee_share (int): The share of the delivery fee this store covers by default, as a
                percentage. The rest is charged to the customer. In force only when
                `default_fee_split_mode` is `percent`; in either amount mode this is
                the percentage the store keeps for when it goes back to one.
            default_fee_split_mode (StoreDefaultFeeSplitMode): Which shape this store's default split has, and therefore
                which of
                the two fields above and below is in force. `percent` splits the fee
                by `default_business_fee_share`; `business_amount` means the store
                covers up to `default_fee_split_amount_cents` of it and the customer
                pays the rest; `customer_amount` is the mirror, the customer paying
                up to that amount and the store covering the rest.

                Read-only. It is set by the restaurant in its own Listo console, and
                sending `default_business_fee_share` on a create or an update moves
                the store back to `percent`.
            default_fee_split_amount_cents (int | None): The amount the two amount modes divide the fee by, in cents. Null
                in
                `percent` mode, and never null in either amount mode. Read-only.
            access_tier (StoreAccessTier): How much of Listo the store itself uses. An `api_only` store's
                deliveries spend your balance, and a `wallet` or `full` store's
                spend its own; `billing` says which. Writable on create and update
                (on a store your account creates, `wallet` and `full` are not chosen
                here),
                and always `api_only` on a test store. A live store of an account
                whose restaurants pay their own Plan Listo cannot be `api_only`: it
                has no console to buy a plan from, so a create or an update that
                asks for it is refused with `422 validation_failed` and
                `param: "access_tier"`.
            markup_cents (int): Your own markup on every delivery of this store, in cents. It is
                added to the delivery fee, split with the customer like the rest of
                the fee, and credited to your balance when the delivery is
                delivered. Writable on create and update.
            billing (StoreBilling): Whose balance pays this store's deliveries, read off `access_tier`
                so you never have to derive it: `partner` is yours, `store` is the
                store's own. Read-only. It is not who pays the store's plan, which
                is `plan.paid_by`.
            test (bool):
            created_at (datetime.datetime):
            plan (None | StorePlanType0): The store's Plan Listo, or `null` when the store needs no plan: a
                test store, or a live store created before Plan Listo existed, which
                keeps requesting couriers without one. It is also `null` when the
                store pays its own plan (every store of an account whose stores pay
                their own Plan Listo) and the restaurant has not bought one yet: the
                restaurant buys it in its own console, and there is nothing for you
                to pay or to reactivate. It is also `null` for a store of a partner
                on pricing with no Plan Listo, which needs no plan. When it is an
                object every
                key is present, and the ones that do not apply are `null`. See
                [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).
            add_ons (None | StoreAddOnsType0): The store's paid add-ons, or `null` when the store cannot hold any.
                On Listo's self-serve pricing, the stores your account created itself
                can hold add-ons; any other store shows `add_ons: null`.
                When it is an object it has all five keys, each with every field.
                Switch them on and off with `PATCH /v1/stores/{id}`. `wallet` and
                `full_console` read `available: false` and cannot be switched on. See
                [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).
            order_value_limits (StoreOrderValueLimits): The most an order may be worth at this store right now, per payment
                type. A request above it is refused with `order_value_over_cap`
                (prepaid and card) or `cash_over_cap` (cash). The limits can change
                without a `store.updated` event, for example during a special limit,
                so read them from the store when you need them.
    """

    id: str
    external_id: None | str
    name: str
    phone: str
    street: str
    apt_unit: None | str
    lat: float | None
    lng: float | None
    pickup_notes: None | str
    timezone: str
    default_business_fee_share: int
    default_fee_split_mode: StoreDefaultFeeSplitMode
    default_fee_split_amount_cents: int | None
    access_tier: StoreAccessTier
    markup_cents: int
    billing: StoreBilling
    test: bool
    created_at: datetime.datetime
    plan: None | StorePlanType0
    add_ons: None | StoreAddOnsType0
    order_value_limits: StoreOrderValueLimits
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.store_add_ons_type_0 import StoreAddOnsType0
        from ..models.store_plan_type_0 import StorePlanType0

        id = self.id

        external_id: None | str
        external_id = self.external_id

        name = self.name

        phone = self.phone

        street = self.street

        apt_unit: None | str
        apt_unit = self.apt_unit

        lat: float | None
        lat = self.lat

        lng: float | None
        lng = self.lng

        pickup_notes: None | str
        pickup_notes = self.pickup_notes

        timezone = self.timezone

        default_business_fee_share = self.default_business_fee_share

        default_fee_split_mode = self.default_fee_split_mode.value

        default_fee_split_amount_cents: int | None
        default_fee_split_amount_cents = self.default_fee_split_amount_cents

        access_tier = self.access_tier.value

        markup_cents = self.markup_cents

        billing = self.billing.value

        test = self.test

        created_at = self.created_at.isoformat()

        plan: dict[str, Any] | None
        if isinstance(self.plan, StorePlanType0):
            plan = self.plan.to_dict()
        else:
            plan = self.plan

        add_ons: dict[str, Any] | None
        if isinstance(self.add_ons, StoreAddOnsType0):
            add_ons = self.add_ons.to_dict()
        else:
            add_ons = self.add_ons

        order_value_limits = self.order_value_limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "external_id": external_id,
                "name": name,
                "phone": phone,
                "street": street,
                "apt_unit": apt_unit,
                "lat": lat,
                "lng": lng,
                "pickup_notes": pickup_notes,
                "timezone": timezone,
                "default_business_fee_share": default_business_fee_share,
                "default_fee_split_mode": default_fee_split_mode,
                "default_fee_split_amount_cents": default_fee_split_amount_cents,
                "access_tier": access_tier,
                "markup_cents": markup_cents,
                "billing": billing,
                "test": test,
                "created_at": created_at,
                "plan": plan,
                "add_ons": add_ons,
                "order_value_limits": order_value_limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.store_add_ons_type_0 import StoreAddOnsType0
        from ..models.store_order_value_limits import StoreOrderValueLimits
        from ..models.store_plan_type_0 import StorePlanType0

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("external_id"))

        name = d.pop("name")

        phone = d.pop("phone")

        street = d.pop("street")

        def _parse_apt_unit(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        apt_unit = _parse_apt_unit(d.pop("apt_unit"))

        def _parse_lat(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        lat = _parse_lat(d.pop("lat"))

        def _parse_lng(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        lng = _parse_lng(d.pop("lng"))

        def _parse_pickup_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        pickup_notes = _parse_pickup_notes(d.pop("pickup_notes"))

        timezone = d.pop("timezone")

        default_business_fee_share = d.pop("default_business_fee_share")

        default_fee_split_mode = StoreDefaultFeeSplitMode(
            d.pop("default_fee_split_mode")
        )

        def _parse_default_fee_split_amount_cents(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        default_fee_split_amount_cents = _parse_default_fee_split_amount_cents(
            d.pop("default_fee_split_amount_cents")
        )

        access_tier = StoreAccessTier(d.pop("access_tier"))

        markup_cents = d.pop("markup_cents")

        billing = StoreBilling(d.pop("billing"))

        test = d.pop("test")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_plan(data: object) -> None | StorePlanType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_type_0 = StorePlanType0.from_dict(data)

                return plan_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StorePlanType0, data)

        plan = _parse_plan(d.pop("plan"))

        def _parse_add_ons(data: object) -> None | StoreAddOnsType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                add_ons_type_0 = StoreAddOnsType0.from_dict(data)

                return add_ons_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StoreAddOnsType0, data)

        add_ons = _parse_add_ons(d.pop("add_ons"))

        order_value_limits = StoreOrderValueLimits.from_dict(
            d.pop("order_value_limits")
        )

        store = cls(
            id=id,
            external_id=external_id,
            name=name,
            phone=phone,
            street=street,
            apt_unit=apt_unit,
            lat=lat,
            lng=lng,
            pickup_notes=pickup_notes,
            timezone=timezone,
            default_business_fee_share=default_business_fee_share,
            default_fee_split_mode=default_fee_split_mode,
            default_fee_split_amount_cents=default_fee_split_amount_cents,
            access_tier=access_tier,
            markup_cents=markup_cents,
            billing=billing,
            test=test,
            created_at=created_at,
            plan=plan,
            add_ons=add_ons,
            order_value_limits=order_value_limits,
        )

        store.additional_properties = d
        return store

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
