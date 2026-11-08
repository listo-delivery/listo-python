from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_courier_type_0_location_type_0 import (
        DeliveryCourierType0LocationType0,
    )
    from ..models.delivery_courier_type_0_phone_type_0 import (
        DeliveryCourierType0PhoneType0,
    )


T = TypeVar("T", bound="DeliveryCourierType0")


@_attrs_define
class DeliveryCourierType0:
    """Null until a courier is assigned, and then FROZEN: a terminal
    delivery keeps reporting who carried it.

        Attributes:
            name (str):
            vehicle (None | str): What the courier is riding, in English whatever locale the
                request carried ("Motorcycle", "Bicycle"). Derived from
                `vehicle_type`, so it is null exactly when that is: display it,
                and switch on `vehicle_type` instead.
            vehicle_type (None | str): The machine-readable type: `bicycle`, `car`, `van`, `truck`,
                `scooter`, `motorcycle` or `walker`. Null until the courier is
                assigned a vehicle. Treat an unlisted value as unknown rather
                than an error: this list grows.
            plate (None | str):
            phone (DeliveryCourierType0PhoneType0 | None): A masked number and its IVR PIN, never a personal number. Dial
                `masked` and enter `pin` when the system asks. Null when no
                number has been issued for this courier.
            location (DeliveryCourierType0LocationType0 | None): The live position, present only while the courier is
                actually in
                motion and only once there is a real fix.
            imminent (bool): The courier is about a minute away. Always false once the trip ends.
    """

    name: str
    vehicle: None | str
    vehicle_type: None | str
    plate: None | str
    phone: DeliveryCourierType0PhoneType0 | None
    location: DeliveryCourierType0LocationType0 | None
    imminent: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_courier_type_0_location_type_0 import (
            DeliveryCourierType0LocationType0,
        )
        from ..models.delivery_courier_type_0_phone_type_0 import (
            DeliveryCourierType0PhoneType0,
        )

        name = self.name

        vehicle: None | str
        vehicle = self.vehicle

        vehicle_type: None | str
        vehicle_type = self.vehicle_type

        plate: None | str
        plate = self.plate

        phone: dict[str, Any] | None
        if isinstance(self.phone, DeliveryCourierType0PhoneType0):
            phone = self.phone.to_dict()
        else:
            phone = self.phone

        location: dict[str, Any] | None
        if isinstance(self.location, DeliveryCourierType0LocationType0):
            location = self.location.to_dict()
        else:
            location = self.location

        imminent = self.imminent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "vehicle": vehicle,
                "vehicle_type": vehicle_type,
                "plate": plate,
                "phone": phone,
                "location": location,
                "imminent": imminent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery_courier_type_0_location_type_0 import (
            DeliveryCourierType0LocationType0,
        )
        from ..models.delivery_courier_type_0_phone_type_0 import (
            DeliveryCourierType0PhoneType0,
        )

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_vehicle(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        vehicle = _parse_vehicle(d.pop("vehicle"))

        def _parse_vehicle_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        vehicle_type = _parse_vehicle_type(d.pop("vehicle_type"))

        def _parse_plate(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        plate = _parse_plate(d.pop("plate"))

        def _parse_phone(data: object) -> DeliveryCourierType0PhoneType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                phone_type_0 = DeliveryCourierType0PhoneType0.from_dict(data)

                return phone_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryCourierType0PhoneType0 | None, data)

        phone = _parse_phone(d.pop("phone"))

        def _parse_location(data: object) -> DeliveryCourierType0LocationType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = DeliveryCourierType0LocationType0.from_dict(data)

                return location_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryCourierType0LocationType0 | None, data)

        location = _parse_location(d.pop("location"))

        imminent = d.pop("imminent")

        delivery_courier_type_0 = cls(
            name=name,
            vehicle=vehicle,
            vehicle_type=vehicle_type,
            plate=plate,
            phone=phone,
            location=location,
            imminent=imminent,
        )

        delivery_courier_type_0.additional_properties = d
        return delivery_courier_type_0

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
