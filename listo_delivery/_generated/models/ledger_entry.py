from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LedgerEntry")


@_attrs_define
class LedgerEntry:
    """One movement on a balance. Credits are positive, debits negative.

    Attributes:
        id (str): The entry id, `le_` prefixed. Example: le_3kR7pM1xV9tB4nQ6cW2sZdYe.
        type_ (str): Where the movement came from, such as `provider_charge`,
            `provider_charge_reversal`, `plan_charge` or
            `requote_adjustment`. The vocabulary GROWS: it is deliberately a
            plain string, not a closed list, so branch on the values you know
            and count an unfamiliar one toward the balance. `GET /v1/ledger`
            describes each value.
             Example: provider_charge.
        amount_cents (int): Signed centavos. Read the direction off the sign, never off `type`.
        delivery_id (None | str): The `dlv_` id the movement stems from. Null for a top-up, a withdrawal or an
            adjustment.
        store_id (None | str): The `st_` id of the store the movement belongs to. Null when it belongs to no single
            store.
        test (bool):
        occurred_at (datetime.datetime): When the money moved.
    """

    id: str
    type_: str
    amount_cents: int
    delivery_id: None | str
    store_id: None | str
    test: bool
    occurred_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        amount_cents = self.amount_cents

        delivery_id: None | str
        delivery_id = self.delivery_id

        store_id: None | str
        store_id = self.store_id

        test = self.test

        occurred_at = self.occurred_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "amount_cents": amount_cents,
                "delivery_id": delivery_id,
                "store_id": store_id,
                "test": test,
                "occurred_at": occurred_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        amount_cents = d.pop("amount_cents")

        def _parse_delivery_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        delivery_id = _parse_delivery_id(d.pop("delivery_id"))

        def _parse_store_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        store_id = _parse_store_id(d.pop("store_id"))

        test = d.pop("test")

        occurred_at = datetime.datetime.fromisoformat(d.pop("occurred_at"))

        ledger_entry = cls(
            id=id,
            type_=type_,
            amount_cents=amount_cents,
            delivery_id=delivery_id,
            store_id=store_id,
            test=test,
            occurred_at=occurred_at,
        )

        ledger_entry.additional_properties = d
        return ledger_entry

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
