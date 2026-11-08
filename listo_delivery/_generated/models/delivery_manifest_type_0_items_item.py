from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_manifest_type_0_items_item_size import (
    DeliveryManifestType0ItemsItemSize,
)

T = TypeVar("T", bound="DeliveryManifestType0ItemsItem")


@_attrs_define
class DeliveryManifestType0ItemsItem:
    """
    Attributes:
        name (str):
        quantity (int):
        size (DeliveryManifestType0ItemsItemSize): What the item was sent as. `small` when you sent none,
            and on every item created before sizes existed, which is
            what those items were sent as.
    """

    name: str
    quantity: int
    size: DeliveryManifestType0ItemsItemSize
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        quantity = self.quantity

        size = self.size.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "quantity": quantity,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        quantity = d.pop("quantity")

        size = DeliveryManifestType0ItemsItemSize(d.pop("size"))

        delivery_manifest_type_0_items_item = cls(
            name=name,
            quantity=quantity,
            size=size,
        )

        delivery_manifest_type_0_items_item.additional_properties = d
        return delivery_manifest_type_0_items_item

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
