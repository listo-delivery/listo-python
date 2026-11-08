from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_connection_request import CreateConnectionRequest
from ...models.error_response import ErrorResponse
from ...models.store import Store
from ...types import Response


def _get_kwargs(
    *,
    body: CreateConnectionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/connections",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Store | None:
    if response.status_code == 201:
        response_201 = Store.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Store]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateConnectionRequest,
) -> Response[ErrorResponse | Store]:
    """Exchange an approval for the store

     Exchanges the `code` from an approved connect request for the store it
    connected. What comes back is an ordinary store object, identical to what
    `POST /v1/stores` returns, and every store endpoint works on it
    immediately.

    The code is good for 24 hours and can be exchanged more than once: every
    exchange inside the window returns the same store. That is deliberate, so
    an exchange whose response you never received is a retry rather than a
    support thread. Past the window it is `400 code_expired`, but the
    connection itself happened when the owner approved: the store is on
    `GET /v1/stores` and its `store.connected` was sent then, so read it
    from there. Do not start a new connect request for it; the account is
    already connected.

    You do not have to wait for the browser to come back. A `store.connected`
    webhook carries the whole store object the moment the owner approves,
    which is your recovery path when the owner closes the tab before the
    redirect lands.

    Args:
        body (CreateConnectionRequest): The one-time code from an approved connect request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateConnectionRequest,
) -> ErrorResponse | Store | None:
    """Exchange an approval for the store

     Exchanges the `code` from an approved connect request for the store it
    connected. What comes back is an ordinary store object, identical to what
    `POST /v1/stores` returns, and every store endpoint works on it
    immediately.

    The code is good for 24 hours and can be exchanged more than once: every
    exchange inside the window returns the same store. That is deliberate, so
    an exchange whose response you never received is a retry rather than a
    support thread. Past the window it is `400 code_expired`, but the
    connection itself happened when the owner approved: the store is on
    `GET /v1/stores` and its `store.connected` was sent then, so read it
    from there. Do not start a new connect request for it; the account is
    already connected.

    You do not have to wait for the browser to come back. A `store.connected`
    webhook carries the whole store object the moment the owner approves,
    which is your recovery path when the owner closes the tab before the
    redirect lands.

    Args:
        body (CreateConnectionRequest): The one-time code from an approved connect request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateConnectionRequest,
) -> Response[ErrorResponse | Store]:
    """Exchange an approval for the store

     Exchanges the `code` from an approved connect request for the store it
    connected. What comes back is an ordinary store object, identical to what
    `POST /v1/stores` returns, and every store endpoint works on it
    immediately.

    The code is good for 24 hours and can be exchanged more than once: every
    exchange inside the window returns the same store. That is deliberate, so
    an exchange whose response you never received is a retry rather than a
    support thread. Past the window it is `400 code_expired`, but the
    connection itself happened when the owner approved: the store is on
    `GET /v1/stores` and its `store.connected` was sent then, so read it
    from there. Do not start a new connect request for it; the account is
    already connected.

    You do not have to wait for the browser to come back. A `store.connected`
    webhook carries the whole store object the moment the owner approves,
    which is your recovery path when the owner closes the tab before the
    redirect lands.

    Args:
        body (CreateConnectionRequest): The one-time code from an approved connect request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateConnectionRequest,
) -> ErrorResponse | Store | None:
    """Exchange an approval for the store

     Exchanges the `code` from an approved connect request for the store it
    connected. What comes back is an ordinary store object, identical to what
    `POST /v1/stores` returns, and every store endpoint works on it
    immediately.

    The code is good for 24 hours and can be exchanged more than once: every
    exchange inside the window returns the same store. That is deliberate, so
    an exchange whose response you never received is a retry rather than a
    support thread. Past the window it is `400 code_expired`, but the
    connection itself happened when the owner approved: the store is on
    `GET /v1/stores` and its `store.connected` was sent then, so read it
    from there. Do not start a new connect request for it; the account is
    already connected.

    You do not have to wait for the browser to come back. A `store.connected`
    webhook carries the whole store object the moment the owner approves,
    which is your recovery path when the owner closes the tab before the
    redirect lands.

    Args:
        body (CreateConnectionRequest): The one-time code from an approved connect request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
