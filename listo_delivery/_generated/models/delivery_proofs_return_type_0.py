from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryProofsReturnType0")


@_attrs_define
class DeliveryProofsReturnType0:
    """The courier handing the order back at the store after a failed
    delivery. Null unless the order came back with evidence.

        Attributes:
            photo_url (None | str): Photo of the order handed back at the store.
            signature_url (None | str): Image of the signature of whoever received it at the store.
            signer_name (None | str): The name the person who signed typed.
            captured_at (datetime.datetime | None): When Listo first saw this evidence.
            meters_from_store (int | None): How far from the store the courier was when this was
                captured, in whole metres in a straight line. Null when
                either position is unknown. Evidence for a person to read,
                not a verdict.
    """

    photo_url: None | str
    signature_url: None | str
    signer_name: None | str
    captured_at: datetime.datetime | None
    meters_from_store: int | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photo_url: None | str
        photo_url = self.photo_url

        signature_url: None | str
        signature_url = self.signature_url

        signer_name: None | str
        signer_name = self.signer_name

        captured_at: None | str
        if isinstance(self.captured_at, datetime.datetime):
            captured_at = self.captured_at.isoformat()
        else:
            captured_at = self.captured_at

        meters_from_store: int | None
        meters_from_store = self.meters_from_store

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photo_url": photo_url,
                "signature_url": signature_url,
                "signer_name": signer_name,
                "captured_at": captured_at,
                "meters_from_store": meters_from_store,
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

        def _parse_signature_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        signature_url = _parse_signature_url(d.pop("signature_url"))

        def _parse_signer_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        signer_name = _parse_signer_name(d.pop("signer_name"))

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

        def _parse_meters_from_store(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        meters_from_store = _parse_meters_from_store(d.pop("meters_from_store"))

        delivery_proofs_return_type_0 = cls(
            photo_url=photo_url,
            signature_url=signature_url,
            signer_name=signer_name,
            captured_at=captured_at,
            meters_from_store=meters_from_store,
        )

        delivery_proofs_return_type_0.additional_properties = d
        return delivery_proofs_return_type_0

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
