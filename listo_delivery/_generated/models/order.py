from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.order_currency import OrderCurrency
from ..models.order_fulfillment import OrderFulfillment
from ..models.order_rejection_reason_type_1 import OrderRejectionReasonType1
from ..models.order_rejection_reason_type_2_type_1 import OrderRejectionReasonType2Type1
from ..models.order_rejection_reason_type_3_type_1 import OrderRejectionReasonType3Type1
from ..models.order_status import OrderStatus

if TYPE_CHECKING:
    from ..models.order_customer import OrderCustomer
    from ..models.order_dropoff_type_0 import OrderDropoffType0
    from ..models.order_lines_item import OrderLinesItem
    from ..models.order_payment import OrderPayment


T = TypeVar("T", bound="Order")


@_attrs_define
class Order:
    """An order a customer placed with the WhatsApp assistant at one of your
    stores. It is what the restaurant reads on its screen and what the
    customer was quoted: the lines, the amounts, where it goes and how it
    is paid.

    An order appears once the restaurant was asked to confirm it. A card
    order the customer has not paid yet has not reached the restaurant, so
    it is not listed, and asking for it is `404 not_found`. A key reads only
    the orders taken in its own mode (a live store is where customers order,
    so live mode is where nearly all of them are), and `test` says which
    mode an order was taken in. An order taken before its store joined your
    account is not yours and is never shown.

    An order can change without its `status` changing: the restaurant can
    add or remove a line, or move the time it promised. Read the order again
    before you act on its lines or its total, instead of keeping the copy
    you first saw.

    Money is integer centavos, timestamps are ISO-8601 in UTC, and every
    enum below is ours. The order carries no numeric id of ours: `id` is the
    only handle.

        Attributes:
            id (str): The order id, `ord_` prefixed. Example: ord_4tQ9mXv7LbR2cN8sKdYh3WpZ.
            store_id (str): The `st_` id of the store that takes the order. Example: st_9pQ2vX7mKdR4tYb1nZ3sLwCe.
            code (str): The human order code the restaurant and the customer both quote. It
                is the same code the order's delivery carries as `code`. Unique per
                store, not globally, so never address an order by it: use `id`, or
                join to the delivery by `delivery_id`.
                 Example: LS-2048.
            status (OrderStatus): `pending_confirmation`: the restaurant has been asked and has not
                answered yet. `preparing`: it accepted the order and is making it.
                `ready`: the food is ready to be handed over. `completed`: it was
                handed over, to the courier or to the customer at the counter.
                `rejected`: the restaurant did not accept it, and `rejection_reason`
                says why. `canceled`: it ended without the restaurant refusing it:
                the customer or the restaurant called it off, or Listo did (for
                example when no courier could be found). It can happen before the
                restaurant answered, so an order can go straight from
                `pending_confirmation` to `canceled`.

                `completed`, `rejected` and `canceled` are final. There is no
                status for an order that is still waiting for the customer to pay
                by card, because such an order is not listed yet.
                 Example: preparing.
            test (bool): True when the order was taken in test mode, and false for a live
                one. It is the mode the order was taken in, and it does not change
                if the store later changes mode.
                 Example: False.
            created_at (datetime.datetime): When the customer placed the order. Example: 2026-11-17T17:59:40Z.
            fulfillment (OrderFulfillment): `delivery`: a courier brings it to the customer, and `dropoff` says
                where. `pickup`: the customer collects it at the counter, `dropoff`
                is null and `customer_fee_cents` is 0.
                 Example: delivery.
            payment (OrderPayment): How the customer pays, and where that got to.
            lines (list[OrderLinesItem]): What was ordered, in the order the customer gave it. Each line is a
                snapshot taken when the order was placed (or when the restaurant
                amended it), so changing the menu later never changes a placed
                order.
            subtotal_cents (int): The sum of the lines' `line_total_cents`, before any campaign offer. Example: 18700.
            offer_discount_cents (int): What a campaign offer took off the food in total: the sum of the
                lines' `offer_discount_cents`. 0 when the order used no offer.
                 Example: 0.
            food_cents (int): The food the customer pays: `subtotal_cents` minus
                `offer_discount_cents`.
                 Example: 18700.
            customer_fee_cents (int): What the customer pays for the delivery, already net of a delivery
                offer, so it can be 0 on a delivery order whose offer covered all of
                it. 0 on a pickup order.
                 Example: 4500.
            total_cents (int): What the customer pays in all: `food_cents` plus
                `customer_fee_cents`.
                 Example: 23200.
            currency (OrderCurrency): Always `MXN`; every amount is in centavos of it. Example: MXN.
            customer (OrderCustomer): Who placed the order.
            dropoff (None | OrderDropoffType0): Where the order goes, on a delivery order. Null on a pickup order.
                The same object a delivery carries as `dropoff`; the name is the
                customer's.
            requested_for (datetime.datetime | None): The time the customer asked for the order. Null means as soon as
                possible.
                 Example: 2026-11-17T20:00:00Z.
            ready_at (datetime.datetime | None): The time the restaurant promised the order ready. Null until it
                accepts the order. It moves when the restaurant asks for more time,
                so read it again rather than keeping the first one you saw.
                 Example: 2026-11-17T18:30:00Z.
            rejection_reason (None | OrderRejectionReasonType1 | OrderRejectionReasonType2Type1 |
                OrderRejectionReasonType3Type1): Why the restaurant did not accept the order, on a `rejected` order
                and null otherwise. `out_of_stock`: something ran out. `saturated`:
                the kitchen has too many orders. `closed`: the restaurant is closed.
                `other`: the restaurant wrote its own reason in `rejection_note`.
                `unanswered`: nobody at the restaurant answered in time.
                 Example: other.
            rejection_note (None | str): The restaurant's own words, only when `rejection_reason` is
                `other`. Null otherwise.
                 Example: Se acabo el gas..
            promotions (list[str]): The promotions the restaurant was running when the order arrived and
                that the order qualifies for, as the owner wrote them (a gift such as
                "Refresco de regalo"). They are promised with the order and are not
                part of any amount. Empty when there were none.
                 Example: ['Refresco de regalo'].
            delivery_id (None | str): The `dlv_` id of the order's delivery, once the restaurant accepted
                a delivery order and a courier was requested for it. Null on a
                pickup order and on an order not accepted yet. Read it with
                `GET /v1/deliveries/{id}`.
                 Example: dlv_7hK2mQ9xR4tV6bN1cZ8sLwYe.
    """

    id: str
    store_id: str
    code: str
    status: OrderStatus
    test: bool
    created_at: datetime.datetime
    fulfillment: OrderFulfillment
    payment: OrderPayment
    lines: list[OrderLinesItem]
    subtotal_cents: int
    offer_discount_cents: int
    food_cents: int
    customer_fee_cents: int
    total_cents: int
    currency: OrderCurrency
    customer: OrderCustomer
    dropoff: None | OrderDropoffType0
    requested_for: datetime.datetime | None
    ready_at: datetime.datetime | None
    rejection_reason: (
        None
        | OrderRejectionReasonType1
        | OrderRejectionReasonType2Type1
        | OrderRejectionReasonType3Type1
    )
    rejection_note: None | str
    promotions: list[str]
    delivery_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.order_dropoff_type_0 import OrderDropoffType0

        id = self.id

        store_id = self.store_id

        code = self.code

        status = self.status.value

        test = self.test

        created_at = self.created_at.isoformat()

        fulfillment = self.fulfillment.value

        payment = self.payment.to_dict()

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)

        subtotal_cents = self.subtotal_cents

        offer_discount_cents = self.offer_discount_cents

        food_cents = self.food_cents

        customer_fee_cents = self.customer_fee_cents

        total_cents = self.total_cents

        currency = self.currency.value

        customer = self.customer.to_dict()

        dropoff: dict[str, Any] | None
        if isinstance(self.dropoff, OrderDropoffType0):
            dropoff = self.dropoff.to_dict()
        else:
            dropoff = self.dropoff

        requested_for: None | str
        if isinstance(self.requested_for, datetime.datetime):
            requested_for = self.requested_for.isoformat()
        else:
            requested_for = self.requested_for

        ready_at: None | str
        if isinstance(self.ready_at, datetime.datetime):
            ready_at = self.ready_at.isoformat()
        else:
            ready_at = self.ready_at

        rejection_reason: None | str
        if (
            isinstance(self.rejection_reason, OrderRejectionReasonType1)
            or isinstance(self.rejection_reason, OrderRejectionReasonType2Type1)
            or isinstance(self.rejection_reason, OrderRejectionReasonType3Type1)
        ):
            rejection_reason = self.rejection_reason.value
        else:
            rejection_reason = self.rejection_reason

        rejection_note: None | str
        rejection_note = self.rejection_note

        promotions = self.promotions

        delivery_id: None | str
        delivery_id = self.delivery_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "store_id": store_id,
                "code": code,
                "status": status,
                "test": test,
                "created_at": created_at,
                "fulfillment": fulfillment,
                "payment": payment,
                "lines": lines,
                "subtotal_cents": subtotal_cents,
                "offer_discount_cents": offer_discount_cents,
                "food_cents": food_cents,
                "customer_fee_cents": customer_fee_cents,
                "total_cents": total_cents,
                "currency": currency,
                "customer": customer,
                "dropoff": dropoff,
                "requested_for": requested_for,
                "ready_at": ready_at,
                "rejection_reason": rejection_reason,
                "rejection_note": rejection_note,
                "promotions": promotions,
                "delivery_id": delivery_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.order_customer import OrderCustomer
        from ..models.order_dropoff_type_0 import OrderDropoffType0
        from ..models.order_lines_item import OrderLinesItem
        from ..models.order_payment import OrderPayment

        d = dict(src_dict)
        id = d.pop("id")

        store_id = d.pop("store_id")

        code = d.pop("code")

        status = OrderStatus(d.pop("status"))

        test = d.pop("test")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        fulfillment = OrderFulfillment(d.pop("fulfillment"))

        payment = OrderPayment.from_dict(d.pop("payment"))

        lines = []
        _lines = d.pop("lines")
        for lines_item_data in _lines:
            lines_item = OrderLinesItem.from_dict(lines_item_data)

            lines.append(lines_item)

        subtotal_cents = d.pop("subtotal_cents")

        offer_discount_cents = d.pop("offer_discount_cents")

        food_cents = d.pop("food_cents")

        customer_fee_cents = d.pop("customer_fee_cents")

        total_cents = d.pop("total_cents")

        currency = OrderCurrency(d.pop("currency"))

        customer = OrderCustomer.from_dict(d.pop("customer"))

        def _parse_dropoff(data: object) -> None | OrderDropoffType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dropoff_type_0 = OrderDropoffType0.from_dict(data)

                return dropoff_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OrderDropoffType0, data)

        dropoff = _parse_dropoff(d.pop("dropoff"))

        def _parse_requested_for(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                requested_for_type_0 = datetime.datetime.fromisoformat(data)

                return requested_for_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        requested_for = _parse_requested_for(d.pop("requested_for"))

        def _parse_ready_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ready_at_type_0 = datetime.datetime.fromisoformat(data)

                return ready_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        ready_at = _parse_ready_at(d.pop("ready_at"))

        def _parse_rejection_reason(
            data: object,
        ) -> (
            None
            | OrderRejectionReasonType1
            | OrderRejectionReasonType2Type1
            | OrderRejectionReasonType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rejection_reason_type_1 = OrderRejectionReasonType1(data)

                return rejection_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rejection_reason_type_2_type_1 = OrderRejectionReasonType2Type1(data)

                return rejection_reason_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rejection_reason_type_3_type_1 = OrderRejectionReasonType3Type1(data)

                return rejection_reason_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | OrderRejectionReasonType1
                | OrderRejectionReasonType2Type1
                | OrderRejectionReasonType3Type1,
                data,
            )

        rejection_reason = _parse_rejection_reason(d.pop("rejection_reason"))

        def _parse_rejection_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rejection_note = _parse_rejection_note(d.pop("rejection_note"))

        promotions = cast(list[str], d.pop("promotions"))

        def _parse_delivery_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        delivery_id = _parse_delivery_id(d.pop("delivery_id"))

        order = cls(
            id=id,
            store_id=store_id,
            code=code,
            status=status,
            test=test,
            created_at=created_at,
            fulfillment=fulfillment,
            payment=payment,
            lines=lines,
            subtotal_cents=subtotal_cents,
            offer_discount_cents=offer_discount_cents,
            food_cents=food_cents,
            customer_fee_cents=customer_fee_cents,
            total_cents=total_cents,
            currency=currency,
            customer=customer,
            dropoff=dropoff,
            requested_for=requested_for,
            ready_at=ready_at,
            rejection_reason=rejection_reason,
            rejection_note=rejection_note,
            promotions=promotions,
            delivery_id=delivery_id,
        )

        order.additional_properties = d
        return order

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
