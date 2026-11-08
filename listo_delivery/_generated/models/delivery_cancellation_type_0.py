from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_cancellation_type_0_party import DeliveryCancellationType0Party
from ..models.delivery_cancellation_type_0_reason_type_1 import (
    DeliveryCancellationType0ReasonType1,
)
from ..models.delivery_cancellation_type_0_reason_type_2_type_1 import (
    DeliveryCancellationType0ReasonType2Type1,
)
from ..models.delivery_cancellation_type_0_reason_type_3_type_1 import (
    DeliveryCancellationType0ReasonType3Type1,
)

T = TypeVar("T", bound="DeliveryCancellationType0")


@_attrs_define
class DeliveryCancellationType0:
    """Who called the order off, and why. Null on an order that was not cancelled.

    Attributes:
        party (DeliveryCancellationType0Party): `partner` is you. `courier` is the person carrying it.
            `platform` is us, and it also covers a cancellation reported to
            us on the customer's behalf: the end customer is not an actor in
            this API, so this field never names a person you cannot
            correlate.
        reason (DeliveryCancellationType0ReasonType1 | DeliveryCancellationType0ReasonType2Type1 |
            DeliveryCancellationType0ReasonType3Type1 | None): The reason you sent on a cancel. Null when the attribution
            was
            derived rather than given, which is every cancellation you did
            not make.
        description (None | str):
    """

    party: DeliveryCancellationType0Party
    reason: (
        DeliveryCancellationType0ReasonType1
        | DeliveryCancellationType0ReasonType2Type1
        | DeliveryCancellationType0ReasonType3Type1
        | None
    )
    description: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        party = self.party.value

        reason: None | str
        if (
            isinstance(self.reason, DeliveryCancellationType0ReasonType1)
            or isinstance(self.reason, DeliveryCancellationType0ReasonType2Type1)
            or isinstance(self.reason, DeliveryCancellationType0ReasonType3Type1)
        ):
            reason = self.reason.value
        else:
            reason = self.reason

        description: None | str
        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "party": party,
                "reason": reason,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        party = DeliveryCancellationType0Party(d.pop("party"))

        def _parse_reason(
            data: object,
        ) -> (
            DeliveryCancellationType0ReasonType1
            | DeliveryCancellationType0ReasonType2Type1
            | DeliveryCancellationType0ReasonType3Type1
            | None
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = DeliveryCancellationType0ReasonType1(data)

                return reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = DeliveryCancellationType0ReasonType2Type1(data)

                return reason_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = DeliveryCancellationType0ReasonType3Type1(data)

                return reason_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DeliveryCancellationType0ReasonType1
                | DeliveryCancellationType0ReasonType2Type1
                | DeliveryCancellationType0ReasonType3Type1
                | None,
                data,
            )

        reason = _parse_reason(d.pop("reason"))

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        delivery_cancellation_type_0 = cls(
            party=party,
            reason=reason,
            description=description,
        )

        delivery_cancellation_type_0.additional_properties = d
        return delivery_cancellation_type_0

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
