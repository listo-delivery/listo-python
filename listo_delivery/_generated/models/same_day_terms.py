from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.same_day_terms_unavailable_reason_type_1 import (
    SameDayTermsUnavailableReasonType1,
)
from ..models.same_day_terms_unavailable_reason_type_2_type_1 import (
    SameDayTermsUnavailableReasonType2Type1,
)
from ..models.same_day_terms_unavailable_reason_type_3_type_1 import (
    SameDayTermsUnavailableReasonType3Type1,
)

T = TypeVar("T", bound="SameDayTerms")


@_attrs_define
class SameDayTerms:
    """What a `same_day` withdrawal would cost you and how large a one you
    could ask for, right now. Every field is always present.

        Attributes:
            fee_cents (int): What a same-day withdrawal costs, IVA included, charged on top of the amount.
            minimum_cents (int): The smallest `amount_cents` a same-day request is accepted for.
            ceiling_cents (int): The largest `amount_cents` a same-day request would be accepted for
                at this moment. Not another name for `available_cents`.
            reach_cents (int): Everything a request could draw on before the fee.
            advanceable_cents (int): The part of `reach_cents` that is still-held cash.
            cap_cents (int): The daily maximum per account.
            cap_used_cents (int): How much of the daily maximum is already used today.
            cap_remaining_cents (int): What is left of the daily maximum today.
            window_open (bool): Whether staff are sending transfers right now.
            due_at (datetime.datetime): The deadline a request made at the moment you read this would carry.
            next_window_opens_at (datetime.datetime): The next time sending resumes.
            offerable (bool): False when no same-day request would be accepted at all.
            unavailable_reason (None | SameDayTermsUnavailableReasonType1 | SameDayTermsUnavailableReasonType2Type1 |
                SameDayTermsUnavailableReasonType3Type1): Why `offerable` is false: `cap_reached` (today's maximum is spent)
                or `below_minimum` (the reach is too small to clear the floor plus
                the fee). Null whenever `offerable` is true.
    """

    fee_cents: int
    minimum_cents: int
    ceiling_cents: int
    reach_cents: int
    advanceable_cents: int
    cap_cents: int
    cap_used_cents: int
    cap_remaining_cents: int
    window_open: bool
    due_at: datetime.datetime
    next_window_opens_at: datetime.datetime
    offerable: bool
    unavailable_reason: (
        None
        | SameDayTermsUnavailableReasonType1
        | SameDayTermsUnavailableReasonType2Type1
        | SameDayTermsUnavailableReasonType3Type1
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fee_cents = self.fee_cents

        minimum_cents = self.minimum_cents

        ceiling_cents = self.ceiling_cents

        reach_cents = self.reach_cents

        advanceable_cents = self.advanceable_cents

        cap_cents = self.cap_cents

        cap_used_cents = self.cap_used_cents

        cap_remaining_cents = self.cap_remaining_cents

        window_open = self.window_open

        due_at = self.due_at.isoformat()

        next_window_opens_at = self.next_window_opens_at.isoformat()

        offerable = self.offerable

        unavailable_reason: None | str
        if (
            isinstance(self.unavailable_reason, SameDayTermsUnavailableReasonType1)
            or isinstance(
                self.unavailable_reason, SameDayTermsUnavailableReasonType2Type1
            )
            or isinstance(
                self.unavailable_reason, SameDayTermsUnavailableReasonType3Type1
            )
        ):
            unavailable_reason = self.unavailable_reason.value
        else:
            unavailable_reason = self.unavailable_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fee_cents": fee_cents,
                "minimum_cents": minimum_cents,
                "ceiling_cents": ceiling_cents,
                "reach_cents": reach_cents,
                "advanceable_cents": advanceable_cents,
                "cap_cents": cap_cents,
                "cap_used_cents": cap_used_cents,
                "cap_remaining_cents": cap_remaining_cents,
                "window_open": window_open,
                "due_at": due_at,
                "next_window_opens_at": next_window_opens_at,
                "offerable": offerable,
                "unavailable_reason": unavailable_reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        fee_cents = d.pop("fee_cents")

        minimum_cents = d.pop("minimum_cents")

        ceiling_cents = d.pop("ceiling_cents")

        reach_cents = d.pop("reach_cents")

        advanceable_cents = d.pop("advanceable_cents")

        cap_cents = d.pop("cap_cents")

        cap_used_cents = d.pop("cap_used_cents")

        cap_remaining_cents = d.pop("cap_remaining_cents")

        window_open = d.pop("window_open")

        due_at = datetime.datetime.fromisoformat(d.pop("due_at"))

        next_window_opens_at = datetime.datetime.fromisoformat(
            d.pop("next_window_opens_at")
        )

        offerable = d.pop("offerable")

        def _parse_unavailable_reason(
            data: object,
        ) -> (
            None
            | SameDayTermsUnavailableReasonType1
            | SameDayTermsUnavailableReasonType2Type1
            | SameDayTermsUnavailableReasonType3Type1
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                unavailable_reason_type_1 = SameDayTermsUnavailableReasonType1(data)

                return unavailable_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                unavailable_reason_type_2_type_1 = (
                    SameDayTermsUnavailableReasonType2Type1(data)
                )

                return unavailable_reason_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                unavailable_reason_type_3_type_1 = (
                    SameDayTermsUnavailableReasonType3Type1(data)
                )

                return unavailable_reason_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                None
                | SameDayTermsUnavailableReasonType1
                | SameDayTermsUnavailableReasonType2Type1
                | SameDayTermsUnavailableReasonType3Type1,
                data,
            )

        unavailable_reason = _parse_unavailable_reason(d.pop("unavailable_reason"))

        same_day_terms = cls(
            fee_cents=fee_cents,
            minimum_cents=minimum_cents,
            ceiling_cents=ceiling_cents,
            reach_cents=reach_cents,
            advanceable_cents=advanceable_cents,
            cap_cents=cap_cents,
            cap_used_cents=cap_used_cents,
            cap_remaining_cents=cap_remaining_cents,
            window_open=window_open,
            due_at=due_at,
            next_window_opens_at=next_window_opens_at,
            offerable=offerable,
            unavailable_reason=unavailable_reason,
        )

        same_day_terms.additional_properties = d
        return same_day_terms

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
