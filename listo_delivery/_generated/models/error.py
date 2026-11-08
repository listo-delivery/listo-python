from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """What every refusal and every failure looks like. `code` is the only
    field to branch on; `message` is for a human reading a log and may
    change wording or language without notice.

        Attributes:
            code (str): A stable, machine-readable name for what went wrong, such as
                `validation_failed`, `not_found` or `insufficient_balance`. Branch
                on this and never on `message`. The set grows additively: handle a
                code you do not know as the generic failure its status code says it
                is. Every code has a page under `doc_url`.
                 Example: validation_failed.
            message (str): A sentence for the person debugging. Free to change wording or
                language, so never match on it.
                 Example: order_value_cents is required..
            param (None | str): The request field the refusal is about, when one applies, spelled
                as you sent it (`dropoff.street`, `manifest.items`). Null when the
                failure is not about one field.
                 Example: order_value_cents.
            retryable (bool): Whether sending the identical request again could succeed. `false`
                means it never will without a change on your side or in the world.
                 Example: False.
            doc_url (str): The documentation page for this `code`. Example:
                https://docs.listo.delivery/en/errors/validation_failed.
            request_id (str): Our id for this request, the same value as the `X-Request-Id`
                response header. Quote it to support, and filter
                `GET /v1/request_logs` by it.
                 Example: 0b1f6c9a-7e2d-4c53-9a41-5d8e3f2a6b10.
    """

    code: str
    message: str
    param: None | str
    retryable: bool
    doc_url: str
    request_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        param: None | str
        param = self.param

        retryable = self.retryable

        doc_url = self.doc_url

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "param": param,
                "retryable": retryable,
                "doc_url": doc_url,
                "request_id": request_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        def _parse_param(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        param = _parse_param(d.pop("param"))

        retryable = d.pop("retryable")

        doc_url = d.pop("doc_url")

        request_id = d.pop("request_id")

        error = cls(
            code=code,
            message=message,
            param=param,
            retryable=retryable,
            doc_url=doc_url,
            request_id=request_id,
        )

        error.additional_properties = d
        return error

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
