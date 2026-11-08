from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ping_mode import PingMode

if TYPE_CHECKING:
    from ..models.ping_partner import PingPartner


T = TypeVar("T", bound="Ping")


@_attrs_define
class Ping:
    """Proof that your key works, and which world it acts in.

    Attributes:
        partner (PingPartner): The company the key belongs to.
        mode (PingMode): The world the key acts in. A `test` key dispatches simulated
            couriers and moves no money.
        test (bool): True when `mode` is `test`.
    """

    partner: PingPartner
    mode: PingMode
    test: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        partner = self.partner.to_dict()

        mode = self.mode.value

        test = self.test

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partner": partner,
                "mode": mode,
                "test": test,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.ping_partner import PingPartner

        d = dict(src_dict)
        partner = PingPartner.from_dict(d.pop("partner"))

        mode = PingMode(d.pop("mode"))

        test = d.pop("test")

        ping = cls(
            partner=partner,
            mode=mode,
            test=test,
        )

        ping.additional_properties = d
        return ping

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
