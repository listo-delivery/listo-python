from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_list import DeliveryList
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
    origin: str | Unset = UNSET,
    payment_status: str | Unset = UNSET,
    status: str | Unset = UNSET,
    store_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["cursor"] = cursor

    params["external_id"] = external_id

    params["origin"] = origin

    params["payment_status"] = payment_status

    params["status"] = status

    params["store_id"] = store_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/deliveries",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeliveryList | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = DeliveryList.from_dict(response.json())

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
) -> Response[DeliveryList | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
    origin: str | Unset = UNSET,
    payment_status: str | Unset = UNSET,
    status: str | Unset = UNSET,
    store_id: str | Unset = UNSET,
) -> Response[DeliveryList | ErrorResponse]:
    """List deliveries

     Your deliveries, newest first, keyset-paginated the same way stores are.
    Filter by `status`, `payment_status`, `store_id`, `external_id`,
    `created_after` and `created_before`.

    This is also the recovery path after a webhook outage. Re-read the
    deliveries whose state you may have missed; the object you get back is
    the same one the webhook would have carried, and it is where things
    stand now. You can send one event again with
    `POST /v1/events/{event_id}/resend`, but a resent event carries the
    snapshot from the moment it happened, so a day-old status change
    describes a state the order has since left. Use a resend to debug a
    handler, and this list to catch up.

    Args:
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):
        external_id (str | Unset):
        origin (str | Unset):
        payment_status (str | Unset):
        status (str | Unset):
        store_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
        external_id=external_id,
        origin=origin,
        payment_status=payment_status,
        status=status,
        store_id=store_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
    origin: str | Unset = UNSET,
    payment_status: str | Unset = UNSET,
    status: str | Unset = UNSET,
    store_id: str | Unset = UNSET,
) -> DeliveryList | ErrorResponse | None:
    """List deliveries

     Your deliveries, newest first, keyset-paginated the same way stores are.
    Filter by `status`, `payment_status`, `store_id`, `external_id`,
    `created_after` and `created_before`.

    This is also the recovery path after a webhook outage. Re-read the
    deliveries whose state you may have missed; the object you get back is
    the same one the webhook would have carried, and it is where things
    stand now. You can send one event again with
    `POST /v1/events/{event_id}/resend`, but a resent event carries the
    snapshot from the moment it happened, so a day-old status change
    describes a state the order has since left. Use a resend to debug a
    handler, and this list to catch up.

    Args:
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):
        external_id (str | Unset):
        origin (str | Unset):
        payment_status (str | Unset):
        status (str | Unset):
        store_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryList | ErrorResponse
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
        external_id=external_id,
        origin=origin,
        payment_status=payment_status,
        status=status,
        store_id=store_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
    origin: str | Unset = UNSET,
    payment_status: str | Unset = UNSET,
    status: str | Unset = UNSET,
    store_id: str | Unset = UNSET,
) -> Response[DeliveryList | ErrorResponse]:
    """List deliveries

     Your deliveries, newest first, keyset-paginated the same way stores are.
    Filter by `status`, `payment_status`, `store_id`, `external_id`,
    `created_after` and `created_before`.

    This is also the recovery path after a webhook outage. Re-read the
    deliveries whose state you may have missed; the object you get back is
    the same one the webhook would have carried, and it is where things
    stand now. You can send one event again with
    `POST /v1/events/{event_id}/resend`, but a resent event carries the
    snapshot from the moment it happened, so a day-old status change
    describes a state the order has since left. Use a resend to debug a
    handler, and this list to catch up.

    Args:
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):
        external_id (str | Unset):
        origin (str | Unset):
        payment_status (str | Unset):
        status (str | Unset):
        store_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryList | ErrorResponse]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
        external_id=external_id,
        origin=origin,
        payment_status=payment_status,
        status=status,
        store_id=store_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
    external_id: str | Unset = UNSET,
    origin: str | Unset = UNSET,
    payment_status: str | Unset = UNSET,
    status: str | Unset = UNSET,
    store_id: str | Unset = UNSET,
) -> DeliveryList | ErrorResponse | None:
    """List deliveries

     Your deliveries, newest first, keyset-paginated the same way stores are.
    Filter by `status`, `payment_status`, `store_id`, `external_id`,
    `created_after` and `created_before`.

    This is also the recovery path after a webhook outage. Re-read the
    deliveries whose state you may have missed; the object you get back is
    the same one the webhook would have carried, and it is where things
    stand now. You can send one event again with
    `POST /v1/events/{event_id}/resend`, but a resent event carries the
    snapshot from the moment it happened, so a day-old status change
    describes a state the order has since left. Use a resend to debug a
    handler, and this list to catch up.

    Args:
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):
        external_id (str | Unset):
        origin (str | Unset):
        payment_status (str | Unset):
        status (str | Unset):
        store_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryList | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
            created_before=created_before,
            cursor=cursor,
            external_id=external_id,
            origin=origin,
            payment_status=payment_status,
            status=status,
            store_id=store_id,
        )
    ).parsed
