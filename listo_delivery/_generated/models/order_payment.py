from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.order_payment_method import OrderPaymentMethod
from ..models.order_payment_status import OrderPaymentStatus

T = TypeVar("T", bound="OrderPayment")


@_attrs_define
class OrderPayment:
    """How the customer pays, and where that got to.

    Attributes:
        method (OrderPaymentMethod): `cash` is paid at the door or at the counter. `card` is paid
            through the payment link Listo sends the customer, before the
            restaurant is asked.
        status (OrderPaymentStatus): A cash order stays `unpaid`: the money is collected by hand and
            is not tracked here. A card order is listed only after the
            customer paid, so it starts at `paid`, and goes to `refunded` or
            `partially_refunded` if money is given back. You never see
            `awaiting_payment` on an order: an order reaches you only once
            the restaurant was asked, a card order reaches the restaurant
            only after it was paid, and a card order switched to cash goes
            to `unpaid`.
        paid_at (datetime.datetime | None): When the card payment landed. Null on a cash order.
    """

    method: OrderPaymentMethod
    status: OrderPaymentStatus
    paid_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method = self.method.value

        status = self.status.value

        paid_at: None | str
        if isinstance(self.paid_at, datetime.datetime):
            paid_at = self.paid_at.isoformat()
        else:
            paid_at = self.paid_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
                "status": status,
                "paid_at": paid_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = OrderPaymentMethod(d.pop("method"))

        status = OrderPaymentStatus(d.pop("status"))

        def _parse_paid_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                paid_at_type_0 = datetime.datetime.fromisoformat(data)

                return paid_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        paid_at = _parse_paid_at(d.pop("paid_at"))

        order_payment = cls(
            method=method,
            status=status,
            paid_at=paid_at,
        )

        order_payment.additional_properties = d
        return order_payment

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
