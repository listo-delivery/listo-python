from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_store_request_access_tier import UpdateStoreRequestAccessTier
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_store_request_add_ons import UpdateStoreRequestAddOns


T = TypeVar("T", bound="UpdateStoreRequest")


@_attrs_define
class UpdateStoreRequest:
    """The fields to change. Send only the ones you are changing.

    Attributes:
        name (str | Unset):
        phone (str | Unset): A phone that resolves to an E.164 number.
        street (str | Unset): The full street address, in one string.
        apt_unit (str | Unset):
        lat (float | Unset): Latitude. Send it together with `lng`.
        lng (float | Unset): Longitude. Send it together with `lat`.
        pickup_notes (None | str | Unset): Instructions for the courier at the store, up to 280 characters. Null clears
            them.
        timezone (str | Unset): An IANA time zone name.
        default_business_fee_share (int | Unset):
        access_tier (UpdateStoreRequestAccessTier | Unset): What the store gets besides the API. On a store your account
            created, `wallet` and `full` are not chosen here, so a request that
            asks for either tier is refused with `422 validation_failed` and
            `param: "access_tier"`. `api_only` is always accepted.
        markup_cents (int | Unset):
        external_id (None | str | Unset): Your own reference for this location. Null clears it.
        add_ons (UpdateStoreRequestAddOns | Unset): Add-ons to switch on (`true`) or off (`false`). Send only the ones
            you are changing: a key you leave out is untouched, and this never
            replaces the set. `wallet` and `full_console` cannot be switched
            on: `true` for either is refused with `422 validation_failed` and
            `param: "add_ons.wallet"` or `"add_ons.full_console"`, and `false`
            is accepted. Each value must be a JSON boolean; the string
            `"true"`, `1` and `null` are refused with `422 validation_failed`
            and `param: "add_ons.<key>"`, and so is a key that is not an add-on.
    """

    name: str | Unset = UNSET
    phone: str | Unset = UNSET
    street: str | Unset = UNSET
    apt_unit: str | Unset = UNSET
    lat: float | Unset = UNSET
    lng: float | Unset = UNSET
    pickup_notes: None | str | Unset = UNSET
    timezone: str | Unset = UNSET
    default_business_fee_share: int | Unset = UNSET
    access_tier: UpdateStoreRequestAccessTier | Unset = UNSET
    markup_cents: int | Unset = UNSET
    external_id: None | str | Unset = UNSET
    add_ons: UpdateStoreRequestAddOns | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        phone = self.phone

        street = self.street

        apt_unit = self.apt_unit

        lat = self.lat

        lng = self.lng

        pickup_notes: None | str | Unset
        if isinstance(self.pickup_notes, Unset):
            pickup_notes = UNSET
        else:
            pickup_notes = self.pickup_notes

        timezone = self.timezone

        default_business_fee_share = self.default_business_fee_share

        access_tier: str | Unset = UNSET
        if not isinstance(self.access_tier, Unset):
            access_tier = self.access_tier.value

        markup_cents = self.markup_cents

        external_id: None | str | Unset
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        add_ons: dict[str, Any] | Unset = UNSET
        if not isinstance(self.add_ons, Unset):
            add_ons = self.add_ons.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if phone is not UNSET:
            field_dict["phone"] = phone
        if street is not UNSET:
            field_dict["street"] = street
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
        if add_ons is not UNSET:
            field_dict["add_ons"] = add_ons

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.update_store_request_add_ons import UpdateStoreRequestAddOns

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        phone = d.pop("phone", UNSET)

        street = d.pop("street", UNSET)

        apt_unit = d.pop("apt_unit", UNSET)

        lat = d.pop("lat", UNSET)

        lng = d.pop("lng", UNSET)

        def _parse_pickup_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pickup_notes = _parse_pickup_notes(d.pop("pickup_notes", UNSET))

        timezone = d.pop("timezone", UNSET)

        default_business_fee_share = d.pop("default_business_fee_share", UNSET)

        _access_tier = d.pop("access_tier", UNSET)
        access_tier: UpdateStoreRequestAccessTier | Unset
        if isinstance(_access_tier, Unset):
            access_tier = UNSET
        else:
            access_tier = UpdateStoreRequestAccessTier(_access_tier)

        markup_cents = d.pop("markup_cents", UNSET)

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        _add_ons = d.pop("add_ons", UNSET)
        add_ons: UpdateStoreRequestAddOns | Unset
        if isinstance(_add_ons, Unset):
            add_ons = UNSET
        else:
            add_ons = UpdateStoreRequestAddOns.from_dict(_add_ons)

        update_store_request = cls(
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
            add_ons=add_ons,
        )

        update_store_request.additional_properties = d
        return update_store_request

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
