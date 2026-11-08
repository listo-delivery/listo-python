from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_proofs_dropoff_type_0 import DeliveryProofsDropoffType0
    from ..models.delivery_proofs_pickup_type_0 import DeliveryProofsPickupType0
    from ..models.delivery_proofs_return_type_0 import DeliveryProofsReturnType0


T = TypeVar("T", bound="DeliveryProofs")


@_attrs_define
class DeliveryProofs:
    """The evidence the trip left, one entry per moment. Each moment is
    null until it happens (nothing has been captured for it yet), so
    this object is always present with its three keys. A photo or
    signature link is Listo's own signed link to the stored copy, and
    **it is null until Listo holds that copy** (a few seconds after the
    courier takes the photo): the rest of the moment, the signer, the
    time and the distance, is there from the start, and when the copy
    lands a `delivery.updated` webhook carries the link. **Each link is
    valid for 24 hours** from the response (or webhook) that carried
    it: it is a short-lived signed link, never a permanent one. A
    partner that needs the image later fetches
    `GET /v1/deliveries/{id}` again for a fresh link, or keeps a copy.

        Attributes:
            pickup (DeliveryProofsPickupType0 | None): The courier collecting the order at the store. Null until the
                pickup photo exists.
            dropoff (DeliveryProofsDropoffType0 | None): The courier at the customer's door. Present once the order is
                delivered, or once the attempt left a photo, a signature or a
                signer there, **including an attempt that failed**: read
                `delivered`, not the presence of a photo, to know whether the
                order was handed over.
            return_ (DeliveryProofsReturnType0 | None): The courier handing the order back at the store after a failed
                delivery. Null unless the order came back with evidence.
    """

    pickup: DeliveryProofsPickupType0 | None
    dropoff: DeliveryProofsDropoffType0 | None
    return_: DeliveryProofsReturnType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_proofs_dropoff_type_0 import DeliveryProofsDropoffType0
        from ..models.delivery_proofs_pickup_type_0 import DeliveryProofsPickupType0
        from ..models.delivery_proofs_return_type_0 import DeliveryProofsReturnType0

        pickup: dict[str, Any] | None
        if isinstance(self.pickup, DeliveryProofsPickupType0):
            pickup = self.pickup.to_dict()
        else:
            pickup = self.pickup

        dropoff: dict[str, Any] | None
        if isinstance(self.dropoff, DeliveryProofsDropoffType0):
            dropoff = self.dropoff.to_dict()
        else:
            dropoff = self.dropoff

        return_: dict[str, Any] | None
        if isinstance(self.return_, DeliveryProofsReturnType0):
            return_ = self.return_.to_dict()
        else:
            return_ = self.return_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pickup": pickup,
                "dropoff": dropoff,
                "return": return_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery_proofs_dropoff_type_0 import DeliveryProofsDropoffType0
        from ..models.delivery_proofs_pickup_type_0 import DeliveryProofsPickupType0
        from ..models.delivery_proofs_return_type_0 import DeliveryProofsReturnType0

        d = dict(src_dict)

        def _parse_pickup(data: object) -> DeliveryProofsPickupType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pickup_type_0 = DeliveryProofsPickupType0.from_dict(data)

                return pickup_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryProofsPickupType0 | None, data)

        pickup = _parse_pickup(d.pop("pickup"))

        def _parse_dropoff(data: object) -> DeliveryProofsDropoffType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dropoff_type_0 = DeliveryProofsDropoffType0.from_dict(data)

                return dropoff_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryProofsDropoffType0 | None, data)

        dropoff = _parse_dropoff(d.pop("dropoff"))

        def _parse_return_(data: object) -> DeliveryProofsReturnType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return_type_0 = DeliveryProofsReturnType0.from_dict(data)

                return return_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryProofsReturnType0 | None, data)

        return_ = _parse_return_(d.pop("return"))

        delivery_proofs = cls(
            pickup=pickup,
            dropoff=dropoff,
            return_=return_,
        )

        delivery_proofs.additional_properties = d
        return delivery_proofs

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
