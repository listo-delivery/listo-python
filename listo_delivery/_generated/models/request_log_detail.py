from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RequestLogDetail")


@_attrs_define
class RequestLogDetail:
    """One call with what was sent and what came back. The bodies are the
    stored copy: an API key anywhere in them reads as its first characters
    and `[key masked]`, the link in the answer to `POST /v1/connect_requests`
    or a Stripe onboarding call reads `[redacted: one-time link]`, and a body
    over 64 KB is an object with `_listo_truncated: true`, its
    `original_bytes` and the first 64 KB as `text`. Headers are never kept.

        Attributes:
            id (str): The call's id, `req_` prefixed. Example: req_4f9c2b7e1a8d3056b1c2d3e4.
            method (str): The HTTP method of the call. Example: POST.
            path (None | str): The path that was called, with its query string. Null on a call made
                before paths were kept.
                 Example: /v1/deliveries.
            endpoint (str): Which operation the call reached, as `controller#action`. Example: api/v1/deliveries#create.
            status (int): The HTTP status Listo answered with. Example: 422.
            error_code (None | str): The `error.code` of the answer when it was an error, otherwise null. Example:
                validation_failed.
            duration_ms (int | None): How long Listo took to answer, in milliseconds. Null when it was not measured.
                Example: 118.
            request_id (None | str): The call's request id, the value of the `X-Request-Id` response header. Null on a call
                made before request ids were kept. Example: 0b1f6c9a-7e2d-4c53-9a41-5d8e3f2a6b10.
            api_key_prefix (None | str): The first characters of the key that made the call, never the secret. Null when no
                key is on record for the call. Example: lst_test_Ab1.
            test (bool): True when the call was made with a test key.
            created_at (datetime.datetime): When Listo received the call, ISO-8601 in UTC. Example: 2026-11-06T16:02:11Z.
            request_body (Any): What the call sent, as JSON. Null when nothing was sent, on a call
                made before bodies were kept, and on the three debugging reads
                themselves, which keep no bodies.
            response_body (Any): What Listo answered, as JSON. Null on the same rows `request_body`
                is.
    """

    id: str
    method: str
    path: None | str
    endpoint: str
    status: int
    error_code: None | str
    duration_ms: int | None
    request_id: None | str
    api_key_prefix: None | str
    test: bool
    created_at: datetime.datetime
    request_body: Any
    response_body: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        method = self.method

        path: None | str
        path = self.path

        endpoint = self.endpoint

        status = self.status

        error_code: None | str
        error_code = self.error_code

        duration_ms: int | None
        duration_ms = self.duration_ms

        request_id: None | str
        request_id = self.request_id

        api_key_prefix: None | str
        api_key_prefix = self.api_key_prefix

        test = self.test

        created_at = self.created_at.isoformat()

        request_body = self.request_body

        response_body = self.response_body

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "method": method,
                "path": path,
                "endpoint": endpoint,
                "status": status,
                "error_code": error_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
                "api_key_prefix": api_key_prefix,
                "test": test,
                "created_at": created_at,
                "request_body": request_body,
                "response_body": response_body,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        method = d.pop("method")

        def _parse_path(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        path = _parse_path(d.pop("path"))

        endpoint = d.pop("endpoint")

        status = d.pop("status")

        def _parse_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_code = _parse_error_code(d.pop("error_code"))

        def _parse_duration_ms(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        duration_ms = _parse_duration_ms(d.pop("duration_ms"))

        def _parse_request_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        request_id = _parse_request_id(d.pop("request_id"))

        def _parse_api_key_prefix(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        api_key_prefix = _parse_api_key_prefix(d.pop("api_key_prefix"))

        test = d.pop("test")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        request_body = d.pop("request_body")

        response_body = d.pop("response_body")

        request_log_detail = cls(
            id=id,
            method=method,
            path=path,
            endpoint=endpoint,
            status=status,
            error_code=error_code,
            duration_ms=duration_ms,
            request_id=request_id,
            api_key_prefix=api_key_prefix,
            test=test,
            created_at=created_at,
            request_body=request_body,
            response_body=response_body,
        )

        request_log_detail.additional_properties = d
        return request_log_detail

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
