from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.ledger_entry_list import LedgerEntryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    *,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["delivery_id"] = delivery_id

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/stores/{store_id}/ledger".format(
            store_id=quote(str(store_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LedgerEntryList | None:
    if response.status_code == 200:
        response_200 = LedgerEntryList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | LedgerEntryList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> Response[ErrorResponse | LedgerEntryList]:
    """List a store's ledger entries

    Args:
        store_id (str):
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LedgerEntryList]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> ErrorResponse | LedgerEntryList | None:
    """List a store's ledger entries

    Args:
        store_id (str):
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LedgerEntryList
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> Response[ErrorResponse | LedgerEntryList]:
    """List a store's ledger entries

    Args:
        store_id (str):
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LedgerEntryList]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> ErrorResponse | LedgerEntryList | None:
    """List a store's ledger entries

    Args:
        store_id (str):
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LedgerEntryList
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            cursor=cursor,
            delivery_id=delivery_id,
            type_=type_,
        )
    ).parsed
