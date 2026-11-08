"""The Listo client: one httpx session, the API key, and the retry rule."""

from __future__ import annotations

import datetime
import email.utils
import enum
import json
import time
import uuid
from collections.abc import Mapping
from typing import Any
from urllib.parse import quote

import httpx

from . import webhooks as _webhooks
from ._operation import Operation
from ._resources import RESOURCES, RootOperations, WebhooksResource
from ._version import API_VERSION, SDK_VERSION
from .errors import ListoConnectionError, ListoError

DEFAULT_BASE_URL = "https://api.listo.delivery"
KEY_PREFIXES = {"lst_live_": "live", "lst_test_": "test"}
CLIENT_ID = f"listo-python/{SDK_VERSION} api/{API_VERSION}"
RETRY_AFTER_DEFAULT = 1.0
RETRY_AFTER_MAX = 60.0
_UNEXPECTED_RETRYABLE = {429, 502, 503, 504}

__all__ = ["Listo", "DEFAULT_BASE_URL"]


class _Webhooks(WebhooksResource):
    """``client.webhooks``: the two webhook operations plus the signature helpers."""

    verify = staticmethod(_webhooks.verify)
    construct_event = staticmethod(_webhooks.construct_event)


def _retry_after_seconds(value: str | None) -> float:
    """Seconds to wait on a 429: integer or HTTP date, else 1, never above 60."""
    if value is None:
        return RETRY_AFTER_DEFAULT
    text = value.strip()
    if text.isascii() and text.isdigit():
        seconds = float(int(text))
    else:
        try:
            when = email.utils.parsedate_to_datetime(text)
        except (TypeError, ValueError, IndexError):
            return RETRY_AFTER_DEFAULT
        if when.tzinfo is None:
            when = when.replace(tzinfo=datetime.timezone.utc)
        seconds = (when - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    return min(max(seconds, 0.0), RETRY_AFTER_MAX)


def _query_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def _query_params(query: Mapping[str, Any] | None) -> list[tuple[str, Any]]:
    if not query:
        return []
    params = []
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            params += [(key, _query_value(item)) for item in value]
        else:
            params.append((key, _query_value(value)))
    return params


class Listo(RootOperations):
    """A client for the Listo Delivery API.

    >>> listo = Listo("lst_test_...")
    >>> listo.ping()

    The key decides the world: ``lst_test_`` keys act in test mode (``listo.mode
    == "test"``), ``lst_live_`` keys in live mode. ``max_retries`` above zero
    retries a 429 (and only a 429) after the ``Retry-After`` it names.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        max_retries: int = 0,
        timeout: float | httpx.Timeout = 30.0,
        *,
        http_client: httpx.Client | None = None,
    ) -> None:
        mode = None
        if isinstance(api_key, str):
            for prefix, name in KEY_PREFIXES.items():
                if api_key.startswith(prefix):
                    mode = name
        if mode is None:
            # The key is never echoed, not even a prefix of it.
            raise ValueError("api_key must start with 'lst_live_' or 'lst_test_'.")
        if not isinstance(max_retries, int) or isinstance(max_retries, bool) or max_retries < 0:
            raise ValueError("max_retries must be an integer of 0 or more.")

        self._api_key = api_key
        self.mode: str = mode
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max_retries
        self._sleep = time.sleep
        self._owns_http = http_client is None
        self._http = http_client or httpx.Client(timeout=timeout)

        resources = {**RESOURCES, "webhooks": _Webhooks}
        for name, resource_class in resources.items():
            setattr(self, name, resource_class(self))

    # Declared for type checkers; the loop above sets them.
    webhooks: _Webhooks

    def __repr__(self) -> str:
        return f"Listo(mode={self.mode!r}, base_url={self.base_url!r})"

    def close(self) -> None:
        """Close the HTTP session, unless you passed your own ``http_client``."""
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> Listo:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _headers(self, has_body: bool, idempotency_key: str | None) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": CLIENT_ID,
            "X-Listo-Client": CLIENT_ID,
        }
        if has_body:
            headers["Content-Type"] = "application/json"
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    def _execute(
        self,
        operation: Operation,
        path_args: tuple[str, ...],
        body: Any,
        query: Mapping[str, Any] | None,
        idempotency_key: str | None,
    ) -> Any:
        path = operation.path
        for name, value in zip(operation.path_params, path_args, strict=True):
            if value is None or str(value) == "":
                # An empty id would build the collection URL and answer a list.
                raise ValueError(f"{name} must not be empty.")
            path = path.replace("{" + name + "}", quote(str(value), safe=""))

        content: bytes | None = None
        if operation.has_body:
            if body is None:
                if operation.body_required:
                    raise ValueError("this operation needs a request body.")
            else:
                payload = body.to_dict() if hasattr(body, "to_dict") else body
                content = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()

        key = None
        if operation.idempotent:
            if idempotency_key is None:
                # One fresh key per call, reused only by this call's own retries.
                key = str(uuid.uuid4())
            elif not isinstance(idempotency_key, str):
                raise TypeError("idempotency_key must be a string.")
            elif not idempotency_key.strip():
                raise ValueError("idempotency_key must not be empty or only whitespace.")
            else:
                key = idempotency_key

        request = self._http.build_request(
            operation.method,
            self.base_url + path,
            params=_query_params(query),
            content=content,
            headers=self._headers(content is not None, key),
        )

        attempt = 0
        while True:
            try:
                response = self._http.send(request)
            except httpx.TransportError as error:
                raise ListoConnectionError(
                    f"Could not reach the Listo API ({type(error).__name__})."
                ) from error
            if response.status_code == 429 and attempt < self.max_retries:
                attempt += 1
                self._sleep(_retry_after_seconds(response.headers.get("Retry-After")))
                continue
            break

        return self._result(operation, response)

    def _result(self, operation: Operation, response: httpx.Response) -> Any:
        status = response.status_code
        if not 200 <= status < 300:
            raise self._error(response)
        if status == 204 or not response.content:
            return None
        try:
            data = response.json()
        except ValueError:
            raise self._unexpected(response, "invalid_response") from None
        try:
            return operation.parse(data)
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            raise ListoError(
                f"The response to {operation.operation_id} did not match its schema.",
                code="invalid_response",
                status=status,
                request_id=response.headers.get("X-Request-Id"),
                body=data,
            ) from error

    def _unexpected(self, response: httpx.Response, code: str) -> ListoError:
        status = response.status_code
        return ListoError(
            f"Unexpected response with status {status}",
            code=code,
            status=status,
            request_id=response.headers.get("X-Request-Id"),
            body=response.text,
        )

    def _error(self, response: httpx.Response) -> ListoError:
        status = response.status_code
        header_request_id = response.headers.get("X-Request-Id")
        try:
            body = response.json()
        except ValueError:
            body = None
        envelope = body.get("error") if isinstance(body, dict) else None
        if isinstance(envelope, dict) and isinstance(envelope.get("code"), str):
            return ListoError(
                str(envelope.get("message", "")),
                code=envelope["code"],
                status=status,
                param=envelope.get("param"),
                retryable=envelope.get("retryable"),
                request_id=envelope.get("request_id") or header_request_id,
                doc_url=envelope.get("doc_url"),
                body=body,
            )
        return ListoError(
            f"Unexpected response with status {status}",
            code=f"http_{status}",
            status=status,
            retryable=status in _UNEXPECTED_RETRYABLE,
            request_id=header_request_id,
            body=body if body is not None else response.text,
        )
