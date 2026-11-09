from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.send_test_webhook_request_type import SendTestWebhookRequestType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SendTestWebhookRequest")


@_attrs_define
class SendTestWebhookRequest:
    """Which event to send a sample of.

    Attributes:
        type_ (SendTestWebhookRequestType): The published event type to send a sample of.
        deliver (bool | Unset): Whether the event is also sent to your webhook URL. `true`, the
            default, sends it. `false` records the event and sends nothing to
            the URL, so no webhook URL has to be configured: the event reaches
            any session listening for your events live and is listed on
            `GET /v1/events` with `test: true`, and no attempt is made. A value
            that is not `true` or `false` is refused with `422 validation_failed`
            and `param: "deliver"`.
             Default: True.
    """

    type_: SendTestWebhookRequestType
    deliver: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        deliver = self.deliver

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if deliver is not UNSET:
            field_dict["deliver"] = deliver

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = SendTestWebhookRequestType(d.pop("type"))

        deliver = d.pop("deliver", UNSET)

        send_test_webhook_request = cls(
            type_=type_,
            deliver=deliver,
        )

        send_test_webhook_request.additional_properties = d
        return send_test_webhook_request

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
