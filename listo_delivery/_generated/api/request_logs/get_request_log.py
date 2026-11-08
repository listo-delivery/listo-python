from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.request_log_detail import RequestLogDetail
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/request_logs/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RequestLogDetail | None:
    if response.status_code == 200:
        response_200 = RequestLogDetail.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RequestLogDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RequestLogDetail]:
    """Retrieve a request log entry

     One call, with what it sent (`request_body`) and what Listo answered
    (`response_body`), both as JSON. For a failure, the answer is the error
    envelope you received and the request is what actually went over the
    wire.

    These are the stored copies. An API key anywhere in a body reads as its
    first characters followed by `[key masked]`. The one-time link in the
    answer to `POST /v1/connect_requests` or to a Stripe onboarding call
    reads `[redacted: one-time link]`; what you received is untouched. A body
    over 64 KB is stored as an object with `_listo_truncated: true`, its
    `original_bytes` and the first 64 KB as `text`, so you are always told
    when you are not reading all of it. Headers are never stored.

    A call that was not yours, or was made with a key of the other mode, is
    `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestLogDetail]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> RequestLogDetail | None:
    """Retrieve a request log entry

     One call, with what it sent (`request_body`) and what Listo answered
    (`response_body`), both as JSON. For a failure, the answer is the error
    envelope you received and the request is what actually went over the
    wire.

    These are the stored copies. An API key anywhere in a body reads as its
    first characters followed by `[key masked]`. The one-time link in the
    answer to `POST /v1/connect_requests` or to a Stripe onboarding call
    reads `[redacted: one-time link]`; what you received is untouched. A body
    over 64 KB is stored as an object with `_listo_truncated: true`, its
    `original_bytes` and the first 64 KB as `text`, so you are always told
    when you are not reading all of it. Headers are never stored.

    A call that was not yours, or was made with a key of the other mode, is
    `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestLogDetail
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[RequestLogDetail]:
    """Retrieve a request log entry

     One call, with what it sent (`request_body`) and what Listo answered
    (`response_body`), both as JSON. For a failure, the answer is the error
    envelope you received and the request is what actually went over the
    wire.

    These are the stored copies. An API key anywhere in a body reads as its
    first characters followed by `[key masked]`. The one-time link in the
    answer to `POST /v1/connect_requests` or to a Stripe onboarding call
    reads `[redacted: one-time link]`; what you received is untouched. A body
    over 64 KB is stored as an object with `_listo_truncated: true`, its
    `original_bytes` and the first 64 KB as `text`, so you are always told
    when you are not reading all of it. Headers are never stored.

    A call that was not yours, or was made with a key of the other mode, is
    `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestLogDetail]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> RequestLogDetail | None:
    """Retrieve a request log entry

     One call, with what it sent (`request_body`) and what Listo answered
    (`response_body`), both as JSON. For a failure, the answer is the error
    envelope you received and the request is what actually went over the
    wire.

    These are the stored copies. An API key anywhere in a body reads as its
    first characters followed by `[key masked]`. The one-time link in the
    answer to `POST /v1/connect_requests` or to a Stripe onboarding call
    reads `[redacted: one-time link]`; what you received is untouched. A body
    over 64 KB is stored as an object with `_listo_truncated: true`, its
    `original_bytes` and the first 64 KB as `text`, so you are always told
    when you are not reading all of it. Headers are never stored.

    A call that was not yours, or was made with a key of the other mode, is
    `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestLogDetail
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
