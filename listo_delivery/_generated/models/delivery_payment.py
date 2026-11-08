from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_payment_method import DeliveryPaymentMethod
from ..models.delivery_payment_status import DeliveryPaymentStatus

T = TypeVar("T", bound="DeliveryPayment")


@_attrs_define
class DeliveryPayment:
    """How the customer pays, and where that got to.

    Attributes:
        method (DeliveryPaymentMethod):
        status (DeliveryPaymentStatus):
        url (None | str): The branded payment link for a card order still awaiting
            payment. Listo sends it to your customer itself, by WhatsApp
            and by SMS when the WhatsApp does not reach them, so you can
            show it or keep it but need not send it. Null the moment the
            order is paid or cancelled, because the link is then dead.
        cash_to_collect_cents (int | None): What the courier collects at the door: the goods value plus the
            customer's share of the fee. Null, not zero, on any order that
            is not cash. Zero is a real value on a cash order whose door
            total is zero (a `0` order value you fully cover); such an order
            is dispatched with no collection to make.
        paid_at (datetime.datetime | None):
    """

    method: DeliveryPaymentMethod
    status: DeliveryPaymentStatus
    url: None | str
    cash_to_collect_cents: int | None
    paid_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        method = self.method.value

        status = self.status.value

        url: None | str
        url = self.url

        cash_to_collect_cents: int | None
        cash_to_collect_cents = self.cash_to_collect_cents

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
                "url": url,
                "cash_to_collect_cents": cash_to_collect_cents,
                "paid_at": paid_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        method = DeliveryPaymentMethod(d.pop("method"))

        status = DeliveryPaymentStatus(d.pop("status"))

        def _parse_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        url = _parse_url(d.pop("url"))

        def _parse_cash_to_collect_cents(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        cash_to_collect_cents = _parse_cash_to_collect_cents(
            d.pop("cash_to_collect_cents")
        )

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

        delivery_payment = cls(
            method=method,
            status=status,
            url=url,
            cash_to_collect_cents=cash_to_collect_cents,
            paid_at=paid_at,
        )

        delivery_payment.additional_properties = d
        return delivery_payment

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
