from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_quote_request_payment_method import CreateQuoteRequestPaymentMethod
from ..models.create_quote_request_vehicle import CreateQuoteRequestVehicle
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_quote_request_dropoff import CreateQuoteRequestDropoff
    from ..models.manifest_type_0 import ManifestType0


T = TypeVar("T", bound="CreateQuoteRequest")


@_attrs_define
class CreateQuoteRequest:
    """The trip to price.

    Attributes:
        store_id (str): The `st_` id of the store the courier collects from.
        dropoff (CreateQuoteRequestDropoff): Where the order goes.
        payment_method (CreateQuoteRequestPaymentMethod | Unset): How the customer pays.
        order_value_cents (int | Unset): The value of the order, in centavos. Required for a `cash`
            quote, where it is what the courier collects. A `prepaid` or
            `card` quote, or one with no `payment_method`, is refused with
            `422 order_value_over_cap` when this is above the store's limit
            (`order_value_limits` on the store).
        business_fee_share (int | Unset): The percent of the delivery fee the store pays. Defaults to the store's own.
        business_fee_cap_cents (int | Unset): The most the store pays toward the fee, in centavos.
        pickup_ready_at (datetime.datetime | Unset): When the order will be ready, ISO-8601 in UTC. Must be in the
            future.
        vehicle (CreateQuoteRequestVehicle | Unset): Defaults to `moto`.
        manifest (ManifestType0 | None | Unset): The descriptive item list for the courier. Money never comes from it;
            its only effect on the trip is that an `xlarge` item makes it a car.
            Absent, null, `{}` and `{"items": null}` all mean no cart.
    """

    store_id: str
    dropoff: CreateQuoteRequestDropoff
    payment_method: CreateQuoteRequestPaymentMethod | Unset = UNSET
    order_value_cents: int | Unset = UNSET
    business_fee_share: int | Unset = UNSET
    business_fee_cap_cents: int | Unset = UNSET
    pickup_ready_at: datetime.datetime | Unset = UNSET
    vehicle: CreateQuoteRequestVehicle | Unset = UNSET
    manifest: ManifestType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.manifest_type_0 import ManifestType0

        store_id = self.store_id

        dropoff = self.dropoff.to_dict()

        payment_method: str | Unset = UNSET
        if not isinstance(self.payment_method, Unset):
            payment_method = self.payment_method.value

        order_value_cents = self.order_value_cents

        business_fee_share = self.business_fee_share

        business_fee_cap_cents = self.business_fee_cap_cents

        pickup_ready_at: str | Unset = UNSET
        if not isinstance(self.pickup_ready_at, Unset):
            pickup_ready_at = self.pickup_ready_at.isoformat()

        vehicle: str | Unset = UNSET
        if not isinstance(self.vehicle, Unset):
            vehicle = self.vehicle.value

        manifest: dict[str, Any] | None | Unset
        if isinstance(self.manifest, Unset):
            manifest = UNSET
        elif isinstance(self.manifest, ManifestType0):
            manifest = self.manifest.to_dict()
        else:
            manifest = self.manifest

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "store_id": store_id,
                "dropoff": dropoff,
            }
        )
        if payment_method is not UNSET:
            field_dict["payment_method"] = payment_method
        if order_value_cents is not UNSET:
            field_dict["order_value_cents"] = order_value_cents
        if business_fee_share is not UNSET:
            field_dict["business_fee_share"] = business_fee_share
        if business_fee_cap_cents is not UNSET:
            field_dict["business_fee_cap_cents"] = business_fee_cap_cents
        if pickup_ready_at is not UNSET:
            field_dict["pickup_ready_at"] = pickup_ready_at
        if vehicle is not UNSET:
            field_dict["vehicle"] = vehicle
        if manifest is not UNSET:
            field_dict["manifest"] = manifest

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.create_quote_request_dropoff import CreateQuoteRequestDropoff
        from ..models.manifest_type_0 import ManifestType0

        d = dict(src_dict)
        store_id = d.pop("store_id")

        dropoff = CreateQuoteRequestDropoff.from_dict(d.pop("dropoff"))

        _payment_method = d.pop("payment_method", UNSET)
        payment_method: CreateQuoteRequestPaymentMethod | Unset
        if isinstance(_payment_method, Unset):
            payment_method = UNSET
        else:
            payment_method = CreateQuoteRequestPaymentMethod(_payment_method)

        order_value_cents = d.pop("order_value_cents", UNSET)

        business_fee_share = d.pop("business_fee_share", UNSET)

        business_fee_cap_cents = d.pop("business_fee_cap_cents", UNSET)

        _pickup_ready_at = d.pop("pickup_ready_at", UNSET)
        pickup_ready_at: datetime.datetime | Unset
        if isinstance(_pickup_ready_at, Unset):
            pickup_ready_at = UNSET
        else:
            pickup_ready_at = datetime.datetime.fromisoformat(_pickup_ready_at)

        _vehicle = d.pop("vehicle", UNSET)
        vehicle: CreateQuoteRequestVehicle | Unset
        if isinstance(_vehicle, Unset):
            vehicle = UNSET
        else:
            vehicle = CreateQuoteRequestVehicle(_vehicle)

        def _parse_manifest(data: object) -> ManifestType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_manifest_type_0 = ManifestType0.from_dict(data)

                return componentsschemas_manifest_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManifestType0 | None | Unset, data)

        manifest = _parse_manifest(d.pop("manifest", UNSET))

        create_quote_request = cls(
            store_id=store_id,
            dropoff=dropoff,
            payment_method=payment_method,
            order_value_cents=order_value_cents,
            business_fee_share=business_fee_share,
            business_fee_cap_cents=business_fee_cap_cents,
            pickup_ready_at=pickup_ready_at,
            vehicle=vehicle,
            manifest=manifest,
        )

        create_quote_request.additional_properties = d
        return create_quote_request

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
