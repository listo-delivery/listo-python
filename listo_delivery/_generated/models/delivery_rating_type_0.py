from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_rating_type_0_food_reasons_item import (
    DeliveryRatingType0FoodReasonsItem,
)

T = TypeVar("T", bound="DeliveryRatingType0")


@_attrs_define
class DeliveryRatingType0:
    """What the customer rated the FOOD, for a store with the `ratings`
    add-on. Null for every other delivery, so the key is always there.
    It is filled only for a rating the customer gave while the add-on
    was on for the store: a rating given before you switched it on, or
    after it ended, stays null for good, and a rating given while it was
    on stays here after the add-on ends. The customer rates the food and
    the delivery separately; only the food half is here. The `delivery.rated`
    event carries the delivery with this filled, once.

        Attributes:
            food_stars (int): The customer's stars for the food, 1 to 5. Example: 2.
            food_reasons (list[DeliveryRatingType0FoodReasonsItem]): What went wrong with the food, when the customer rated
                it 3 stars or
                fewer and chose a reason. Empty otherwise.
                 Example: ['cold'].
            rated_at (datetime.datetime): When the customer gave the rating. Example: 2026-07-28T19:20:00Z.
    """

    food_stars: int
    food_reasons: list[DeliveryRatingType0FoodReasonsItem]
    rated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        food_stars = self.food_stars

        food_reasons = []
        for food_reasons_item_data in self.food_reasons:
            food_reasons_item = food_reasons_item_data.value
            food_reasons.append(food_reasons_item)

        rated_at = self.rated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "food_stars": food_stars,
                "food_reasons": food_reasons,
                "rated_at": rated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        food_stars = d.pop("food_stars")

        food_reasons = []
        _food_reasons = d.pop("food_reasons")
        for food_reasons_item_data in _food_reasons:
            food_reasons_item = DeliveryRatingType0FoodReasonsItem(
                food_reasons_item_data
            )

            food_reasons.append(food_reasons_item)

        rated_at = datetime.datetime.fromisoformat(d.pop("rated_at"))

        delivery_rating_type_0 = cls(
            food_stars=food_stars,
            food_reasons=food_reasons,
            rated_at=rated_at,
        )

        delivery_rating_type_0.additional_properties = d
        return delivery_rating_type_0

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
