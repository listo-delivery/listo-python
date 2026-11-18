from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_orders_status import ListOrdersStatus
from ...models.order_list import OrderList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: ListOrdersStatus | Unset = UNSET,
    store_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["store_id"] = store_id

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/orders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OrderList | None:
    if response.status_code == 200:
        response_200 = OrderList.from_dict(response.json())

        return response_200

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
) -> Response[ErrorResponse | OrderList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: ListOrdersStatus | Unset = UNSET,
    store_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | OrderList]:
    """List orders

     The orders customers placed with the WhatsApp assistant at your stores,
    newest first, keyset-paginated the same way deliveries are. Filter by
    `status`, `store_id`, `created_after` and `created_before`.

    An order is listed once the restaurant was asked to confirm it. A card
    order the customer has not paid yet is not listed, and neither is an
    order taken before its store joined your account. A key reads only the
    orders taken in its own mode, so a test key does not see live orders.

    An order can change without its `status` changing (the restaurant can
    add or remove a line, or move the time it promised), so read it again
    with `GET /v1/orders/{id}` before you act on its lines. Its delivery,
    when it has one, is `delivery_id`; the same order and delivery also
    share a `code`.

    Args:
        status (ListOrdersStatus | Unset):
        store_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OrderList]
    """

    kwargs = _get_kwargs(
        status=status,
        store_id=store_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    status: ListOrdersStatus | Unset = UNSET,
    store_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | OrderList | None:
    """List orders

     The orders customers placed with the WhatsApp assistant at your stores,
    newest first, keyset-paginated the same way deliveries are. Filter by
    `status`, `store_id`, `created_after` and `created_before`.

    An order is listed once the restaurant was asked to confirm it. A card
    order the customer has not paid yet is not listed, and neither is an
    order taken before its store joined your account. A key reads only the
    orders taken in its own mode, so a test key does not see live orders.

    An order can change without its `status` changing (the restaurant can
    add or remove a line, or move the time it promised), so read it again
    with `GET /v1/orders/{id}` before you act on its lines. Its delivery,
    when it has one, is `delivery_id`; the same order and delivery also
    share a `code`.

    Args:
        status (ListOrdersStatus | Unset):
        store_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OrderList
    """

    return sync_detailed(
        client=client,
        status=status,
        store_id=store_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: ListOrdersStatus | Unset = UNSET,
    store_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | OrderList]:
    """List orders

     The orders customers placed with the WhatsApp assistant at your stores,
    newest first, keyset-paginated the same way deliveries are. Filter by
    `status`, `store_id`, `created_after` and `created_before`.

    An order is listed once the restaurant was asked to confirm it. A card
    order the customer has not paid yet is not listed, and neither is an
    order taken before its store joined your account. A key reads only the
    orders taken in its own mode, so a test key does not see live orders.

    An order can change without its `status` changing (the restaurant can
    add or remove a line, or move the time it promised), so read it again
    with `GET /v1/orders/{id}` before you act on its lines. Its delivery,
    when it has one, is `delivery_id`; the same order and delivery also
    share a `code`.

    Args:
        status (ListOrdersStatus | Unset):
        store_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OrderList]
    """

    kwargs = _get_kwargs(
        status=status,
        store_id=store_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: ListOrdersStatus | Unset = UNSET,
    store_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | OrderList | None:
    """List orders

     The orders customers placed with the WhatsApp assistant at your stores,
    newest first, keyset-paginated the same way deliveries are. Filter by
    `status`, `store_id`, `created_after` and `created_before`.

    An order is listed once the restaurant was asked to confirm it. A card
    order the customer has not paid yet is not listed, and neither is an
    order taken before its store joined your account. A key reads only the
    orders taken in its own mode, so a test key does not see live orders.

    An order can change without its `status` changing (the restaurant can
    add or remove a line, or move the time it promised), so read it again
    with `GET /v1/orders/{id}` before you act on its lines. Its delivery,
    when it has one, is `delivery_id`; the same order and delivery also
    share a `code`.

    Args:
        status (ListOrdersStatus | Unset):
        store_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OrderList
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            store_id=store_id,
            created_after=created_after,
            created_before=created_before,
            cursor=cursor,
        )
    ).parsed
