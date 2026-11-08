from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateConnectRequestRequest")


@_attrs_define
class CreateConnectRequestRequest:
    """The restaurant owner to ask, and where to send them back.

    Attributes:
        owner_email (str): The email of the person who signs in to the restaurant's Listo account.
        redirect_uri (str): Where the owner's browser returns after approving.
        state (str | Unset): An opaque value returned to `redirect_uri` unchanged, up to 255 characters.
    """

    owner_email: str
    redirect_uri: str
    state: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        owner_email = self.owner_email

        redirect_uri = self.redirect_uri

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner_email": owner_email,
                "redirect_uri": redirect_uri,
            }
        )
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        owner_email = d.pop("owner_email")

        redirect_uri = d.pop("redirect_uri")

        state = d.pop("state", UNSET)

        create_connect_request_request = cls(
            owner_email=owner_email,
            redirect_uri=redirect_uri,
            state=state,
        )

        create_connect_request_request.additional_properties = d
        return create_connect_request_request

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
