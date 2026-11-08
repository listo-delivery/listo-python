from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.card_status import CardStatus
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/stripe_status",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardStatus | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = CardStatus.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CardStatus | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CardStatus | ErrorResponse]:
    """Read your company's card readiness

     Whether your company can take card payments yet, and what is still
    outstanding if not. Re-read this after a `store.updated` webhook: card
    readiness is never a field on the store object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardStatus | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> CardStatus | ErrorResponse | None:
    """Read your company's card readiness

     Whether your company can take card payments yet, and what is still
    outstanding if not. Re-read this after a `store.updated` webhook: card
    readiness is never a field on the store object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardStatus | ErrorResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CardStatus | ErrorResponse]:
    """Read your company's card readiness

     Whether your company can take card payments yet, and what is still
    outstanding if not. Re-read this after a `store.updated` webhook: card
    readiness is never a field on the store object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardStatus | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> CardStatus | ErrorResponse | None:
    """Read your company's card readiness

     Whether your company can take card payments yet, and what is still
    outstanding if not. Re-read this after a `store.updated` webhook: card
    readiness is never a field on the store object.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardStatus | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
