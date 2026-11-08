from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery import Delivery


T = TypeVar("T", bound="DeliveryList")


@_attrs_define
class DeliveryList:
    """One page of deliveries, newest first.

    Attributes:
        data (list[Delivery]):
        has_more (bool): True when a further page exists.
        cursor (None | str): Pass as `cursor` to read the next page. Null on the last page.
    """

    data: list[Delivery]
    has_more: bool
    cursor: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        has_more = self.has_more

        cursor: None | str
        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery import Delivery

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Delivery.from_dict(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        def _parse_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cursor = _parse_cursor(d.pop("cursor"))

        delivery_list = cls(
            data=data,
            has_more=has_more,
            cursor=cursor,
        )

        delivery_list.additional_properties = d
        return delivery_list

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
