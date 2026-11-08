from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RequestLog")


@_attrs_define
class RequestLog:
    """One call your key made to this API: what was called, how it was
    answered and how long it took. The list carries no bodies; read one call
    to get them.

        Attributes:
            id (str): The call's id, `req_` prefixed. Pass it to `GET /v1/request_logs/{id}`. Example:
                req_4f9c2b7e1a8d3056b1c2d3e4.
            method (str): The HTTP method of the call. Example: POST.
            path (None | str): The path that was called, with its query string. Null on a call made
                before paths were kept.
                 Example: /v1/deliveries.
            endpoint (str): Which operation the call reached, as `controller#action`. This is
                the exact value `?endpoint=` filters by.
                 Example: api/v1/deliveries#create.
            status (int): The HTTP status Listo answered with. Example: 422.
            error_code (None | str): The `error.code` of the answer when it was an error, otherwise null. Example:
                validation_failed.
            duration_ms (int | None): How long Listo took to answer, in milliseconds. Null when it was not measured.
                Example: 118.
            request_id (None | str): The call's request id, the value of the `X-Request-Id` response
                header. Quote it when you write to support. Null on a call made
                before request ids were kept.
                 Example: 0b1f6c9a-7e2d-4c53-9a41-5d8e3f2a6b10.
            api_key_prefix (None | str): The first characters of the key that made the call, the same text
                the dashboard's keys page shows, never the secret. Null when no key
                is on record for the call.
                 Example: lst_test_Ab1.
            test (bool): True when the call was made with a test key.
            created_at (datetime.datetime): When Listo received the call, ISO-8601 in UTC. Example: 2026-11-06T16:02:11Z.
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

        request_log = cls(
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
        )

        request_log.additional_properties = d
        return request_log

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
