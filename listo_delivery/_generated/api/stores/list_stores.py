from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.store_list import StoreList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["external_id"] = external_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/stores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | StoreList | None:
    if response.status_code == 200:
        response_200 = StoreList.from_dict(response.json())

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
) -> Response[ErrorResponse | StoreList]:
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
    external_id: str | Unset = UNSET,
) -> Response[ErrorResponse | StoreList]:
    """List your stores

     Your stores, newest first, keyset-paginated. Pass the `cursor` from the
    previous page to continue; `has_more` tells you when to stop. There is
    no total count, by design.

    A key only ever sees the stores of its own world: a test key cannot see
    or address live stores, and the reverse.

    Args:
        cursor (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | StoreList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> ErrorResponse | StoreList | None:
    """List your stores

     Your stores, newest first, keyset-paginated. Pass the `cursor` from the
    previous page to continue; `has_more` tells you when to stop. There is
    no total count, by design.

    A key only ever sees the stores of its own world: a test key cannot see
    or address live stores, and the reverse.

    Args:
        cursor (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | StoreList
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        external_id=external_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> Response[ErrorResponse | StoreList]:
    """List your stores

     Your stores, newest first, keyset-paginated. Pass the `cursor` from the
    previous page to continue; `has_more` tells you when to stop. There is
    no total count, by design.

    A key only ever sees the stores of its own world: a test key cannot see
    or address live stores, and the reverse.

    Args:
        cursor (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | StoreList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
) -> ErrorResponse | StoreList | None:
    """List your stores

     Your stores, newest first, keyset-paginated. Pass the `cursor` from the
    previous page to continue; `has_more` tells you when to stop. There is
    no total count, by design.

    A key only ever sees the stores of its own world: a test key cannot see
    or address live stores, and the reverse.

    Args:
        cursor (str | Unset):
        external_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | StoreList
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            external_id=external_id,
        )
    ).parsed
