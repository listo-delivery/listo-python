from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeliveryProofType0")


@_attrs_define
class DeliveryProofType0:
    """Proof of delivery. Null unless we hold some, and each field is null
    when that piece is missing; a photo with no signature is normal. The
    URLs are Listo's own signed links to the stored copy and are valid
    for 24 hours from the response (or webhook) that carried them:
    fetch `GET /v1/deliveries/{id}` again for a fresh link, or keep a
    copy. **A URL is null until Listo has its own copy of the image**
    (a few seconds after the courier takes it); the copy's arrival is
    announced by a `delivery.updated` webhook that carries the link.
    It may come from a delivery attempt that failed at the
    door, so it is not by itself proof that the order was handed over:
    `proofs.dropoff.delivered` says which. Prefer `proofs`, which keeps
    each moment of the trip apart.

        Attributes:
            picture_url (None | str):
            signature_image_url (None | str):
            signature_name (None | str):
            captured_at (datetime.datetime | None):
    """

    picture_url: None | str
    signature_image_url: None | str
    signature_name: None | str
    captured_at: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        picture_url: None | str
        picture_url = self.picture_url

        signature_image_url: None | str
        signature_image_url = self.signature_image_url

        signature_name: None | str
        signature_name = self.signature_name

        captured_at: None | str
        if isinstance(self.captured_at, datetime.datetime):
            captured_at = self.captured_at.isoformat()
        else:
            captured_at = self.captured_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "picture_url": picture_url,
                "signature_image_url": signature_image_url,
                "signature_name": signature_name,
                "captured_at": captured_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_picture_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        picture_url = _parse_picture_url(d.pop("picture_url"))

        def _parse_signature_image_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        signature_image_url = _parse_signature_image_url(d.pop("signature_image_url"))

        def _parse_signature_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        signature_name = _parse_signature_name(d.pop("signature_name"))

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

        delivery_proof_type_0 = cls(
            picture_url=picture_url,
            signature_image_url=signature_image_url,
            signature_name=signature_name,
            captured_at=captured_at,
        )

        delivery_proof_type_0.additional_properties = d
        return delivery_proof_type_0

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
