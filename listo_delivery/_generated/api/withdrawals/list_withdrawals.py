from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.withdrawal_list import WithdrawalList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/withdrawals",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | WithdrawalList | None:
    if response.status_code == 200:
        response_200 = WithdrawalList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | WithdrawalList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | WithdrawalList]:
    """List your withdrawals

     Your withdrawal requests, newest first, keyset-paginated.

    Args:
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WithdrawalList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | WithdrawalList | None:
    """List your withdrawals

     Your withdrawal requests, newest first, keyset-paginated.

    Args:
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WithdrawalList
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | WithdrawalList]:
    """List your withdrawals

     Your withdrawal requests, newest first, keyset-paginated.

    Args:
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WithdrawalList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | WithdrawalList | None:
    """List your withdrawals

     Your withdrawal requests, newest first, keyset-paginated.

    Args:
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WithdrawalList
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
        )
    ).parsed
