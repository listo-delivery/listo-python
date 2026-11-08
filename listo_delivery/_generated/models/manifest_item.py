from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.manifest_item_size_type_1 import ManifestItemSizeType1
from ..models.manifest_item_size_type_2_type_1 import ManifestItemSizeType2Type1
from ..models.manifest_item_size_type_3_type_1 import ManifestItemSizeType3Type1
from ..types import UNSET, Unset

T = TypeVar("T", bound="ManifestItem")


@_attrs_define
class ManifestItem:
    """One line of the descriptive item list sent to the courier.

    Attributes:
        name (str): What the item is.
        quantity (int): How many of it. A positive whole number.
        size (ManifestItemSizeType1 | ManifestItemSizeType2Type1 | ManifestItemSizeType3Type1 | None | Unset): How big
            the item is. Leave it out for `small`. An `xlarge` item
            makes the trip a car.
    """

    name: str
    quantity: int
    size: (
        ManifestItemSizeType1
        | ManifestItemSizeType2Type1
        | ManifestItemSizeType3Type1
        | None
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        quantity = self.quantity

        size: None | str | Unset
        if isinstance(self.size, Unset):
            size = UNSET
        elif (
            isinstance(self.size, ManifestItemSizeType1)
            or isinstance(self.size, ManifestItemSizeType2Type1)
            or isinstance(self.size, ManifestItemSizeType3Type1)
        ):
            size = self.size.value
        else:
            size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "quantity": quantity,
            }
        )
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        quantity = d.pop("quantity")

        def _parse_size(
            data: object,
        ) -> (
            ManifestItemSizeType1
            | ManifestItemSizeType2Type1
            | ManifestItemSizeType3Type1
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_type_1 = ManifestItemSizeType1(data)

                return size_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_type_2_type_1 = ManifestItemSizeType2Type1(data)

                return size_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                size_type_3_type_1 = ManifestItemSizeType3Type1(data)

                return size_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ManifestItemSizeType1
                | ManifestItemSizeType2Type1
                | ManifestItemSizeType3Type1
                | None
                | Unset,
                data,
            )

        size = _parse_size(d.pop("size", UNSET))

        manifest_item = cls(
            name=name,
            quantity=quantity,
            size=size,
        )

        manifest_item.additional_properties = d
        return manifest_item

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
