from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryProofsPickupType0")


@_attrs_define
class DeliveryProofsPickupType0:
    """The courier collecting the order at the store. Null until the
    pickup photo exists.

        Attributes:
            photo_url (None | str): Photo of the order at the store.
            captured_at (datetime.datetime | None): When Listo first saw this photo.
    """

    photo_url: None | str
    captured_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photo_url: None | str
        photo_url = self.photo_url

        captured_at: None | str
        if isinstance(self.captured_at, datetime.datetime):
            captured_at = self.captured_at.isoformat()
        else:
            captured_at = self.captured_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photo_url": photo_url,
                "captured_at": captured_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_photo_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        photo_url = _parse_photo_url(d.pop("photo_url"))

        def _parse_captured_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                captured_at_type_0 = datetime.datetime.fromisoformat(data)

                return captured_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        captured_at = _parse_captured_at(d.pop("captured_at"))

        delivery_proofs_pickup_type_0 = cls(
            photo_url=photo_url,
            captured_at=captured_at,
        )

        delivery_proofs_pickup_type_0.additional_properties = d
        return delivery_proofs_pickup_type_0

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
