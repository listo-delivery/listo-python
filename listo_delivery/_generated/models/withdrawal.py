from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.withdrawal_currency import WithdrawalCurrency
from ..models.withdrawal_kind import WithdrawalKind
from ..models.withdrawal_status import WithdrawalStatus

T = TypeVar("T", bound="Withdrawal")


@_attrs_define
class Withdrawal:
    """A request to move money out of your balance to your bank account.

    Attributes:
        id (str): The withdrawal id, `wd_` prefixed. Example: wd_2xN6bK9mR4tQ7vC1sZ8pLwYe.
        amount_cents (int): What your bank receives. On a `same_day` withdrawal the fee is a
            SECOND debit rather than a deduction, so this figure is what lands
            either way and `fee_cents` is what your balance loses on top of it.
        fee_cents (int): What the withdrawal cost, IVA included. Always `0` on a `standard`
            withdrawal. Always present.
        currency (WithdrawalCurrency):
        kind (WithdrawalKind): `standard` is the free path: your released balance only, sent in 1
            to 3 business days. `same_day` costs `fee_cents`, can reach cash
            still on hold, and is sent the same day within the hours in
            `POST /v1/withdrawals`.
        status (WithdrawalStatus): `pending` until a human settles it. The move to `paid`, `failed` or
            `canceled` is what `withdrawal.updated` announces.

            `canceled` means nothing reached your bank: the request was stopped
            before any transfer was sent, and the amount and any same-day fee
            are back in `available_cents`. It happens only when your account
            asked Listo to cancel the withdrawal. A client that switches on
            `status` must handle it.
        requested_at (datetime.datetime | None):
        due_at (datetime.datetime | None): When a `same_day` withdrawal is due to have been sent, stamped when
            you requested it and never recalculated afterwards. Null on every
            `standard` withdrawal: the free path promises a range of business
            days rather than an instant.
        resolved_at (datetime.datetime | None): Null while still pending. Set when the withdrawal was paid, failed
            or canceled, to the moment that happened.
        clave_de_rastreo (None | str): The SPEI tracking key for the transfer: the identifier your own bank
            uses to locate the deposit. This is what you reconcile a payout
            against a bank statement with, and it is the same key you see in the
            dashboard for this withdrawal.

            Always present, null until the transfer is sent. It stays null
            forever on a `failed` or `canceled` withdrawal, because no transfer
            happened.
             Example: MBAN01002608120001234567.
        test (bool):
    """

    id: str
    amount_cents: int
    fee_cents: int
    currency: WithdrawalCurrency
    kind: WithdrawalKind
    status: WithdrawalStatus
    requested_at: datetime.datetime | None
    due_at: datetime.datetime | None
    resolved_at: datetime.datetime | None
    clave_de_rastreo: None | str
    test: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        amount_cents = self.amount_cents

        fee_cents = self.fee_cents

        currency = self.currency.value

        kind = self.kind.value

        status = self.status.value

        requested_at: None | str
        if isinstance(self.requested_at, datetime.datetime):
            requested_at = self.requested_at.isoformat()
        else:
            requested_at = self.requested_at

        due_at: None | str
        if isinstance(self.due_at, datetime.datetime):
            due_at = self.due_at.isoformat()
        else:
            due_at = self.due_at

        resolved_at: None | str
        if isinstance(self.resolved_at, datetime.datetime):
            resolved_at = self.resolved_at.isoformat()
        else:
            resolved_at = self.resolved_at

        clave_de_rastreo: None | str
        clave_de_rastreo = self.clave_de_rastreo

        test = self.test

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "amount_cents": amount_cents,
                "fee_cents": fee_cents,
                "currency": currency,
                "kind": kind,
                "status": status,
                "requested_at": requested_at,
                "due_at": due_at,
                "resolved_at": resolved_at,
                "clave_de_rastreo": clave_de_rastreo,
                "test": test,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        amount_cents = d.pop("amount_cents")

        fee_cents = d.pop("fee_cents")

        currency = WithdrawalCurrency(d.pop("currency"))

        kind = WithdrawalKind(d.pop("kind"))

        status = WithdrawalStatus(d.pop("status"))

        def _parse_requested_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                requested_at_type_0 = datetime.datetime.fromisoformat(data)

                return requested_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        requested_at = _parse_requested_at(d.pop("requested_at"))

        def _parse_due_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_at_type_0 = datetime.datetime.fromisoformat(data)

                return due_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        due_at = _parse_due_at(d.pop("due_at"))

        def _parse_resolved_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolved_at_type_0 = datetime.datetime.fromisoformat(data)

                return resolved_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        resolved_at = _parse_resolved_at(d.pop("resolved_at"))

        def _parse_clave_de_rastreo(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        clave_de_rastreo = _parse_clave_de_rastreo(d.pop("clave_de_rastreo"))

        test = d.pop("test")

        withdrawal = cls(
            id=id,
            amount_cents=amount_cents,
            fee_cents=fee_cents,
            currency=currency,
            kind=kind,
            status=status,
            requested_at=requested_at,
            due_at=due_at,
            resolved_at=resolved_at,
            clave_de_rastreo=clave_de_rastreo,
            test=test,
        )

        withdrawal.additional_properties = d
        return withdrawal

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
