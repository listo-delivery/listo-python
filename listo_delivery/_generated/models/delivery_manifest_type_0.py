from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_manifest_type_0_items_item import (
        DeliveryManifestType0ItemsItem,
    )


T = TypeVar("T", bound="DeliveryManifestType0")


@_attrs_define
class DeliveryManifestType0:
    """The descriptive item list you sent, for the courier. Money never
    comes from it, with one exception: an item sized `xlarge` makes the
    trip a car. Null when you sent none.

        Attributes:
            items (list[DeliveryManifestType0ItemsItem]):
    """

    items: list[DeliveryManifestType0ItemsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery_manifest_type_0_items_item import (
            DeliveryManifestType0ItemsItem,
        )

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = DeliveryManifestType0ItemsItem.from_dict(items_item_data)

            items.append(items_item)

        delivery_manifest_type_0 = cls(
            items=items,
        )

        delivery_manifest_type_0.additional_properties = d
        return delivery_manifest_type_0

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
