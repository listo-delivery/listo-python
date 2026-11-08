from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryProofsDropoffType0")


@_attrs_define
class DeliveryProofsDropoffType0:
    """The courier at the customer's door. Present once the order is
    delivered, or once the attempt left a photo, a signature or a
    signer there, **including an attempt that failed**: read
    `delivered`, not the presence of a photo, to know whether the
    order was handed over.

        Attributes:
            photo_url (None | str): Photo taken at the door.
            signature_url (None | str): Image of the recipient's signature.
            signer_name (None | str): The name the person who signed typed.
            captured_at (datetime.datetime | None): When Listo first saw this evidence.
            delivered (bool): True only when the delivery was delivered. False means the
                evidence is from an attempt that did not hand the order over.
    """

    photo_url: None | str
    signature_url: None | str
    signer_name: None | str
    captured_at: datetime.datetime | None
    delivered: bool
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

        delivered = self.delivered

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photo_url": photo_url,
                "signature_url": signature_url,
                "signer_name": signer_name,
                "captured_at": captured_at,
                "delivered": delivered,
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

        delivered = d.pop("delivered")

        delivery_proofs_dropoff_type_0 = cls(
            photo_url=photo_url,
            signature_url=signature_url,
            signer_name=signer_name,
            captured_at=captured_at,
            delivered=delivered,
        )

        delivery_proofs_dropoff_type_0.additional_properties = d
        return delivery_proofs_dropoff_type_0

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
