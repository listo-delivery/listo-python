from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrderLinesItem")


@_attrs_define
class OrderLinesItem:
    """
    Attributes:
        name (str): The dish's name as it was when the order was placed. Example: Taco al pastor.
        quantity (int):  Example: 3.
        options (list[str]): What the customer chose on the dish, one string per question,
            with the answers given inside an option in parentheses, as
            the restaurant's own ticket prints them (`Tamano: Grande (Pan:
            Telera)`). A count above one follows the name (`Extra queso
            x2`). Empty when the dish has no options.
             Example: ['Tamano: Grande (Pan: Telera)', 'Extras: Extra queso x2'].
        note (None | str): What the customer asked for on this line, in their words. Null when they wrote nothing.
            Example: Sin cebolla.
        unit_price_cents (int): The price of ONE unit, with the options included and any sale
            already applied. A dish on sale carries its sale price here.
             Example: 3000.
        sale_discount_cents (int): What a sale took off ONE unit, already inside
            `unit_price_cents`: the unit's regular price is the sum of the
            two. 0 when the dish was not on sale.
             Example: 500.
        line_total_cents (int): The whole line, `unit_price_cents` times `quantity`, BEFORE
            any campaign offer. `offer_discount_cents` is not subtracted
            from it.
             Example: 9000.
        offer_discount_cents (int): What a campaign offer took off the WHOLE line (not per unit),
            not included in `line_total_cents`. 0 when no offer applied.
             Example: 0.
    """

    name: str
    quantity: int
    options: list[str]
    note: None | str
    unit_price_cents: int
    sale_discount_cents: int
    line_total_cents: int
    offer_discount_cents: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        quantity = self.quantity

        options = self.options

        note: None | str
        note = self.note

        unit_price_cents = self.unit_price_cents

        sale_discount_cents = self.sale_discount_cents

        line_total_cents = self.line_total_cents

        offer_discount_cents = self.offer_discount_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "quantity": quantity,
                "options": options,
                "note": note,
                "unit_price_cents": unit_price_cents,
                "sale_discount_cents": sale_discount_cents,
                "line_total_cents": line_total_cents,
                "offer_discount_cents": offer_discount_cents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        quantity = d.pop("quantity")

        options = cast(list[str], d.pop("options"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        unit_price_cents = d.pop("unit_price_cents")

        sale_discount_cents = d.pop("sale_discount_cents")

        line_total_cents = d.pop("line_total_cents")

        offer_discount_cents = d.pop("offer_discount_cents")

        order_lines_item = cls(
            name=name,
            quantity=quantity,
            options=options,
            note=note,
            unit_price_cents=unit_price_cents,
            sale_discount_cents=sale_discount_cents,
            line_total_cents=line_total_cents,
            offer_discount_cents=offer_discount_cents,
        )

        order_lines_item.additional_properties = d
        return order_lines_item

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
