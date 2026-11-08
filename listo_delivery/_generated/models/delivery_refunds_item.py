from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_refunds_item_party import DeliveryRefundsItemParty
from ..models.delivery_refunds_item_requested_via import DeliveryRefundsItemRequestedVia
from ..models.delivery_refunds_item_status import DeliveryRefundsItemStatus

T = TypeVar("T", bound="DeliveryRefundsItem")


@_attrs_define
class DeliveryRefundsItem:
    """
    Attributes:
        id (str): The refund id, `rfn_` prefixed. Example: rfn_4bQ7wS2xK9mT6vN3cZ8pLdYe.
        amount_cents (int | None): What went back, positive, in Mexican peso cents. NULL AND NOT
            ZERO while a refund of the remaining balance is still in
            flight: it carries no amount until the refund is confirmed,
            and a zero would say a refund moved nothing. Read
            `refunded_cents` below rather than summing this array, which
            is exactly why both totals are published.
        reason (None | str): The free text whoever asked for the refund supplied, or null.
            Your own words when you sent them; it is never an enum.
        status (DeliveryRefundsItemStatus): `pending` IS NOT A FAILURE and must not be retried: a
            direct-charge refund is held while the account's balance is
            short and applied once funds land. It flips to `succeeded` on
            its own and publishes that as `delivery.updated`. `failed`
            means nothing moved.
        requested_via (DeliveryRefundsItemRequestedVia): Which lane issued it. `api` is your own
            `POST /v1/deliveries/{id}/refunds`. `console` is the merchant
            pressing it in the Listo console. `automatic` is one we issued
            with nobody asking, on a cancel or a return. `external` is one
            made in the merchant's own payment dashboard, which we learned
            about afterwards.
        party (DeliveryRefundsItemParty): Whose decision it was. `business` is the merchant, or you
            acting for your store. `platform` is Listo issuing it because
            the order ended without reaching the customer.
        created_at (datetime.datetime): When the refund was asked for.
        succeeded_at (datetime.datetime | None): When the money was confirmed on its way. Null on a pending or
            failed refund.
    """

    id: str
    amount_cents: int | None
    reason: None | str
    status: DeliveryRefundsItemStatus
    requested_via: DeliveryRefundsItemRequestedVia
    party: DeliveryRefundsItemParty
    created_at: datetime.datetime
    succeeded_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        amount_cents: int | None
        amount_cents = self.amount_cents

        reason: None | str
        reason = self.reason

        status = self.status.value

        requested_via = self.requested_via.value

        party = self.party.value

        created_at = self.created_at.isoformat()

        succeeded_at: None | str
        if isinstance(self.succeeded_at, datetime.datetime):
            succeeded_at = self.succeeded_at.isoformat()
        else:
            succeeded_at = self.succeeded_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "amount_cents": amount_cents,
                "reason": reason,
                "status": status,
                "requested_via": requested_via,
                "party": party,
                "created_at": created_at,
                "succeeded_at": succeeded_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_amount_cents(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        amount_cents = _parse_amount_cents(d.pop("amount_cents"))

        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))

        status = DeliveryRefundsItemStatus(d.pop("status"))

        requested_via = DeliveryRefundsItemRequestedVia(d.pop("requested_via"))

        party = DeliveryRefundsItemParty(d.pop("party"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_succeeded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                succeeded_at_type_0 = datetime.datetime.fromisoformat(data)

                return succeeded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        succeeded_at = _parse_succeeded_at(d.pop("succeeded_at"))

        delivery_refunds_item = cls(
            id=id,
            amount_cents=amount_cents,
            reason=reason,
            status=status,
            requested_via=requested_via,
            party=party,
            created_at=created_at,
            succeeded_at=succeeded_at,
        )

        delivery_refunds_item.additional_properties = d
        return delivery_refunds_item

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
