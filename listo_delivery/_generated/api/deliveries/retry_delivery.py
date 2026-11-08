from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery import Delivery
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    delivery_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/deliveries/{delivery_id}/retries".format(
            delivery_id=quote(str(delivery_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Delivery | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Delivery.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Delivery | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Delivery | ErrorResponse]:
    """Retry a failed dispatch

     Re-dispatches a delivery that ended at `no_courier`. It is priced and
    debited again, because it is a fresh dispatch, but the delivery id and
    your `external_id` are stable across retries: it stays the same order.

    A retry is a new dispatch, so it asks the store's Plan Listo again: a
    live store whose plan is not paid up is refused with `402
    plan_required`, exactly as the create is.

    A retry the courier network refuses for its distance, at the very edge
    of the store's 15 km service area, answers `422 out_of_service_area`,
    the code the quote and the create give the same fact. It is final: the
    delivery stays at `no_courier`, the attempt is recorded, and nothing is
    charged.

    Args:
        delivery_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
) -> Delivery | ErrorResponse | None:
    """Retry a failed dispatch

     Re-dispatches a delivery that ended at `no_courier`. It is priced and
    debited again, because it is a fresh dispatch, but the delivery id and
    your `external_id` are stable across retries: it stays the same order.

    A retry is a new dispatch, so it asks the store's Plan Listo again: a
    live store whose plan is not paid up is refused with `402
    plan_required`, exactly as the create is.

    A retry the courier network refuses for its distance, at the very edge
    of the store's 15 km service area, answers `422 out_of_service_area`,
    the code the quote and the create give the same fact. It is final: the
    delivery stays at `no_courier`, the attempt is recorded, and nothing is
    charged.

    Args:
        delivery_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return sync_detailed(
        delivery_id=delivery_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Delivery | ErrorResponse]:
    """Retry a failed dispatch

     Re-dispatches a delivery that ended at `no_courier`. It is priced and
    debited again, because it is a fresh dispatch, but the delivery id and
    your `external_id` are stable across retries: it stays the same order.

    A retry is a new dispatch, so it asks the store's Plan Listo again: a
    live store whose plan is not paid up is refused with `402
    plan_required`, exactly as the create is.

    A retry the courier network refuses for its distance, at the very edge
    of the store's 15 km service area, answers `422 out_of_service_area`,
    the code the quote and the create give the same fact. It is final: the
    delivery stays at `no_courier`, the attempt is recorded, and nothing is
    charged.

    Args:
        delivery_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
) -> Delivery | ErrorResponse | None:
    """Retry a failed dispatch

     Re-dispatches a delivery that ended at `no_courier`. It is priced and
    debited again, because it is a fresh dispatch, but the delivery id and
    your `external_id` are stable across retries: it stays the same order.

    A retry is a new dispatch, so it asks the store's Plan Listo again: a
    live store whose plan is not paid up is refused with `402
    plan_required`, exactly as the create is.

    A retry the courier network refuses for its distance, at the very edge
    of the store's 15 km service area, answers `422 out_of_service_area`,
    the code the quote and the create give the same fact. It is final: the
    delivery stays at `no_courier`, the attempt is recorded, and nothing is
    charged.

    Args:
        delivery_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return (
        await asyncio_detailed(
            delivery_id=delivery_id,
            client=client,
        )
    ).parsed
