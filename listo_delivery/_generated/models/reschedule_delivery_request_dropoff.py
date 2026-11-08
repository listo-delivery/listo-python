from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RescheduleDeliveryRequestDropoff")


@_attrs_define
class RescheduleDeliveryRequestDropoff:
    """The part of the drop-off that can still change.

    Attributes:
        notes (None | str): Instructions for the courier at the door, up to 280 characters. Null clears them.
    """

    notes: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        notes: None | str
        notes = self.notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "notes": notes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        reschedule_delivery_request_dropoff = cls(
            notes=notes,
        )

        reschedule_delivery_request_dropoff.additional_properties = d
        return reschedule_delivery_request_dropoff

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
