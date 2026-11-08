from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_store_request_access_tier import CreateStoreRequestAccessTier
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateStoreRequest")


@_attrs_define
class CreateStoreRequest:
    """The pickup location to create.

    Attributes:
        name (str):
        phone (str): A phone that resolves to an E.164 number.
        street (str): The full street address, in one string.
        apt_unit (str | Unset):
        lat (float | Unset): Latitude. Send it together with `lng`, or neither.
        lng (float | Unset): Longitude. Send it together with `lat`, or neither.
        pickup_notes (str | Unset): Instructions for the courier at the store, up to 280 characters.
        timezone (str | Unset): An IANA time zone name.
        default_business_fee_share (int | Unset): The percent of the delivery fee the store pays by default.
        access_tier (CreateStoreRequestAccessTier | Unset): What the store gets besides the API.
        markup_cents (int | Unset): Your markup on each delivery, in centavos, up to 1000000.
        external_id (str | Unset): Your own reference for this location.
        owner_email (str | Unset): The restaurant owner to invite, for a store with a console.
    """

    name: str
    phone: str
    street: str
    apt_unit: str | Unset = UNSET
    lat: float | Unset = UNSET
    lng: float | Unset = UNSET
    pickup_notes: str | Unset = UNSET
    timezone: str | Unset = UNSET
    default_business_fee_share: int | Unset = UNSET
    access_tier: CreateStoreRequestAccessTier | Unset = UNSET
    markup_cents: int | Unset = UNSET
    external_id: str | Unset = UNSET
    owner_email: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        phone = self.phone

        street = self.street

        apt_unit = self.apt_unit

        lat = self.lat

        lng = self.lng

        pickup_notes = self.pickup_notes

        timezone = self.timezone

        default_business_fee_share = self.default_business_fee_share

        access_tier: str | Unset = UNSET
        if not isinstance(self.access_tier, Unset):
            access_tier = self.access_tier.value

        markup_cents = self.markup_cents

        external_id = self.external_id

        owner_email = self.owner_email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "phone": phone,
                "street": street,
            }
        )
        if apt_unit is not UNSET:
            field_dict["apt_unit"] = apt_unit
        if lat is not UNSET:
            field_dict["lat"] = lat
        if lng is not UNSET:
            field_dict["lng"] = lng
        if pickup_notes is not UNSET:
            field_dict["pickup_notes"] = pickup_notes
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if default_business_fee_share is not UNSET:
            field_dict["default_business_fee_share"] = default_business_fee_share
        if access_tier is not UNSET:
            field_dict["access_tier"] = access_tier
        if markup_cents is not UNSET:
            field_dict["markup_cents"] = markup_cents
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if owner_email is not UNSET:
            field_dict["owner_email"] = owner_email

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        phone = d.pop("phone")

        street = d.pop("street")

        apt_unit = d.pop("apt_unit", UNSET)

        lat = d.pop("lat", UNSET)

        lng = d.pop("lng", UNSET)

        pickup_notes = d.pop("pickup_notes", UNSET)

        timezone = d.pop("timezone", UNSET)

        default_business_fee_share = d.pop("default_business_fee_share", UNSET)

        _access_tier = d.pop("access_tier", UNSET)
        access_tier: CreateStoreRequestAccessTier | Unset
        if isinstance(_access_tier, Unset):
            access_tier = UNSET
        else:
            access_tier = CreateStoreRequestAccessTier(_access_tier)

        markup_cents = d.pop("markup_cents", UNSET)

        external_id = d.pop("external_id", UNSET)

        owner_email = d.pop("owner_email", UNSET)

        create_store_request = cls(
            name=name,
            phone=phone,
            street=street,
            apt_unit=apt_unit,
            lat=lat,
            lng=lng,
            pickup_notes=pickup_notes,
            timezone=timezone,
            default_business_fee_share=default_business_fee_share,
            access_tier=access_tier,
            markup_cents=markup_cents,
            external_id=external_id,
            owner_email=owner_email,
        )

        create_store_request.additional_properties = d
        return create_store_request

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
