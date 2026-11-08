from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_withdrawal_request_kind_type_1 import (
    CreateWithdrawalRequestKindType1,
)
from ..models.create_withdrawal_request_kind_type_2_type_1 import (
    CreateWithdrawalRequestKindType2Type1,
)
from ..models.create_withdrawal_request_kind_type_3_type_1 import (
    CreateWithdrawalRequestKindType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWithdrawalRequest")


@_attrs_define
class CreateWithdrawalRequest:
    """How much to move out of your balance.

    Attributes:
        amount_cents (int): What your bank receives, in centavos.
        kind (CreateWithdrawalRequestKindType1 | CreateWithdrawalRequestKindType2Type1 |
            CreateWithdrawalRequestKindType3Type1 | None | Unset): Defaults to `standard`.
    """

    amount_cents: int
    kind: (
        CreateWithdrawalRequestKindType1
        | CreateWithdrawalRequestKindType2Type1
        | CreateWithdrawalRequestKindType3Type1
        | None
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_cents = self.amount_cents

        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        elif (
            isinstance(self.kind, CreateWithdrawalRequestKindType1)
            or isinstance(self.kind, CreateWithdrawalRequestKindType2Type1)
            or isinstance(self.kind, CreateWithdrawalRequestKindType3Type1)
        ):
            kind = self.kind.value
        else:
            kind = self.kind

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount_cents": amount_cents,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        amount_cents = d.pop("amount_cents")

        def _parse_kind(
            data: object,
        ) -> (
            CreateWithdrawalRequestKindType1
            | CreateWithdrawalRequestKindType2Type1
            | CreateWithdrawalRequestKindType3Type1
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_1 = CreateWithdrawalRequestKindType1(data)

                return kind_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_2_type_1 = CreateWithdrawalRequestKindType2Type1(data)

                return kind_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_3_type_1 = CreateWithdrawalRequestKindType3Type1(data)

                return kind_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CreateWithdrawalRequestKindType1
                | CreateWithdrawalRequestKindType2Type1
                | CreateWithdrawalRequestKindType3Type1
                | None
                | Unset,
                data,
            )

        kind = _parse_kind(d.pop("kind", UNSET))

        create_withdrawal_request = cls(
            amount_cents=amount_cents,
            kind=kind,
        )

        create_withdrawal_request.additional_properties = d
        return create_withdrawal_request

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
