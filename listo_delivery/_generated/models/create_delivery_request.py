from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_delivery_request_handoff import CreateDeliveryRequestHandoff
from ..models.create_delivery_request_payment_method import (
    CreateDeliveryRequestPaymentMethod,
)
from ..models.create_delivery_request_simulate import CreateDeliveryRequestSimulate
from ..models.create_delivery_request_vehicle import CreateDeliveryRequestVehicle
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_delivery_request_dropoff import CreateDeliveryRequestDropoff
    from ..models.create_delivery_request_verification import (
        CreateDeliveryRequestVerification,
    )
    from ..models.manifest_type_0 import ManifestType0


T = TypeVar("T", bound="CreateDeliveryRequest")


@_attrs_define
class CreateDeliveryRequest:
    """The order to dispatch.

    Attributes:
        store_id (str): The `st_` id of the store the courier collects from.
        external_id (str): Your own reference for this order. Echoed back as `external_id`.
        payment_method (CreateDeliveryRequestPaymentMethod): How the customer pays.
        order_value_cents (int): The value of the order, in centavos.
        dropoff (CreateDeliveryRequestDropoff): Where the order goes, and who receives it.
        quote_id (str | Unset): The `qt_` id of a quote to book at exactly its price. Without one
            the delivery is priced as it is created.
        business_fee_share (int | Unset): The percent of the delivery fee the store pays. Defaults to the
            store's own, and is forced to `100` on a `prepaid` order.
        business_fee_cap_cents (int | Unset): The most the store pays toward the fee, in centavos.
        tip_cents (int | Unset): A tip for the courier, in centavos, up to 100000. Allowed on a `prepaid` order only.
        handoff (CreateDeliveryRequestHandoff | Unset): Where the courier hands the order over. Defaults to
            `meet_at_door`.
        manifest (ManifestType0 | None | Unset): The descriptive item list for the courier. Money never comes from it;
            its only effect on the trip is that an `xlarge` item makes it a car.
            Absent, null, `{}` and `{"items": null}` all mean no cart.
        verification (CreateDeliveryRequestVerification | Unset): Proof the customer must give the courier.
        pickup_ready_at (datetime.datetime | Unset): When the order will be ready, ISO-8601 in UTC, between 10 minutes
            and 29 days from now. Leave it out to dispatch now.
        vehicle (CreateDeliveryRequestVehicle | Unset): Defaults to `moto`, or to the quote's when you book one.
        simulate (CreateDeliveryRequestSimulate | Unset): Test keys only: the scenario the simulated courier plays. A
            live
            key that sends it is refused.
    """

    store_id: str
    external_id: str
    payment_method: CreateDeliveryRequestPaymentMethod
    order_value_cents: int
    dropoff: CreateDeliveryRequestDropoff
    quote_id: str | Unset = UNSET
    business_fee_share: int | Unset = UNSET
    business_fee_cap_cents: int | Unset = UNSET
    tip_cents: int | Unset = UNSET
    handoff: CreateDeliveryRequestHandoff | Unset = UNSET
    manifest: ManifestType0 | None | Unset = UNSET
    verification: CreateDeliveryRequestVerification | Unset = UNSET
    pickup_ready_at: datetime.datetime | Unset = UNSET
    vehicle: CreateDeliveryRequestVehicle | Unset = UNSET
    simulate: CreateDeliveryRequestSimulate | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.manifest_type_0 import ManifestType0

        store_id = self.store_id

        external_id = self.external_id

        payment_method = self.payment_method.value

        order_value_cents = self.order_value_cents

        dropoff = self.dropoff.to_dict()

        quote_id = self.quote_id

        business_fee_share = self.business_fee_share

        business_fee_cap_cents = self.business_fee_cap_cents

        tip_cents = self.tip_cents

        handoff: str | Unset = UNSET
        if not isinstance(self.handoff, Unset):
            handoff = self.handoff.value

        manifest: dict[str, Any] | None | Unset
        if isinstance(self.manifest, Unset):
            manifest = UNSET
        elif isinstance(self.manifest, ManifestType0):
            manifest = self.manifest.to_dict()
        else:
            manifest = self.manifest

        verification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.verification, Unset):
            verification = self.verification.to_dict()

        pickup_ready_at: str | Unset = UNSET
        if not isinstance(self.pickup_ready_at, Unset):
            pickup_ready_at = self.pickup_ready_at.isoformat()

        vehicle: str | Unset = UNSET
        if not isinstance(self.vehicle, Unset):
            vehicle = self.vehicle.value

        simulate: str | Unset = UNSET
        if not isinstance(self.simulate, Unset):
            simulate = self.simulate.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "store_id": store_id,
                "external_id": external_id,
                "payment_method": payment_method,
                "order_value_cents": order_value_cents,
                "dropoff": dropoff,
            }
        )
        if quote_id is not UNSET:
            field_dict["quote_id"] = quote_id
        if business_fee_share is not UNSET:
            field_dict["business_fee_share"] = business_fee_share
        if business_fee_cap_cents is not UNSET:
            field_dict["business_fee_cap_cents"] = business_fee_cap_cents
        if tip_cents is not UNSET:
            field_dict["tip_cents"] = tip_cents
        if handoff is not UNSET:
            field_dict["handoff"] = handoff
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if verification is not UNSET:
            field_dict["verification"] = verification
        if pickup_ready_at is not UNSET:
            field_dict["pickup_ready_at"] = pickup_ready_at
        if vehicle is not UNSET:
            field_dict["vehicle"] = vehicle
        if simulate is not UNSET:
            field_dict["simulate"] = simulate

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.create_delivery_request_dropoff import (
            CreateDeliveryRequestDropoff,
        )
        from ..models.create_delivery_request_verification import (
            CreateDeliveryRequestVerification,
        )
        from ..models.manifest_type_0 import ManifestType0

        d = dict(src_dict)
        store_id = d.pop("store_id")

        external_id = d.pop("external_id")

        payment_method = CreateDeliveryRequestPaymentMethod(d.pop("payment_method"))

        order_value_cents = d.pop("order_value_cents")

        dropoff = CreateDeliveryRequestDropoff.from_dict(d.pop("dropoff"))

        quote_id = d.pop("quote_id", UNSET)

        business_fee_share = d.pop("business_fee_share", UNSET)

        business_fee_cap_cents = d.pop("business_fee_cap_cents", UNSET)

        tip_cents = d.pop("tip_cents", UNSET)

        _handoff = d.pop("handoff", UNSET)
        handoff: CreateDeliveryRequestHandoff | Unset
        if isinstance(_handoff, Unset):
            handoff = UNSET
        else:
            handoff = CreateDeliveryRequestHandoff(_handoff)

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

        _verification = d.pop("verification", UNSET)
        verification: CreateDeliveryRequestVerification | Unset
        if isinstance(_verification, Unset):
            verification = UNSET
        else:
            verification = CreateDeliveryRequestVerification.from_dict(_verification)

        _pickup_ready_at = d.pop("pickup_ready_at", UNSET)
        pickup_ready_at: datetime.datetime | Unset
        if isinstance(_pickup_ready_at, Unset):
            pickup_ready_at = UNSET
        else:
            pickup_ready_at = datetime.datetime.fromisoformat(_pickup_ready_at)

        _vehicle = d.pop("vehicle", UNSET)
        vehicle: CreateDeliveryRequestVehicle | Unset
        if isinstance(_vehicle, Unset):
            vehicle = UNSET
        else:
            vehicle = CreateDeliveryRequestVehicle(_vehicle)

        _simulate = d.pop("simulate", UNSET)
        simulate: CreateDeliveryRequestSimulate | Unset
        if isinstance(_simulate, Unset):
            simulate = UNSET
        else:
            simulate = CreateDeliveryRequestSimulate(_simulate)

        create_delivery_request = cls(
            store_id=store_id,
            external_id=external_id,
            payment_method=payment_method,
            order_value_cents=order_value_cents,
            dropoff=dropoff,
            quote_id=quote_id,
            business_fee_share=business_fee_share,
            business_fee_cap_cents=business_fee_cap_cents,
            tip_cents=tip_cents,
            handoff=handoff,
            manifest=manifest,
            verification=verification,
            pickup_ready_at=pickup_ready_at,
            vehicle=vehicle,
            simulate=simulate,
        )

        create_delivery_request.additional_properties = d
        return create_delivery_request

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
