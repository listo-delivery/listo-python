from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery import Delivery
from ...models.error_response import ErrorResponse
from ...models.refund_delivery_request import RefundDeliveryRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    delivery_id: str,
    *,
    body: RefundDeliveryRequest | Unset = UNSET,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/deliveries/{delivery_id}/refunds".format(
            delivery_id=quote(str(delivery_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Delivery | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Delivery.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

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
    body: RefundDeliveryRequest | Unset = UNSET,
    idempotency_key: str,
) -> Response[Delivery | ErrorResponse]:
    """Refund a delivery

    Args:
        delivery_id (str):
        idempotency_key (str):
        body (RefundDeliveryRequest | Unset): How much of the order to refund. Both fields are
            optional.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: RefundDeliveryRequest | Unset = UNSET,
    idempotency_key: str,
) -> Delivery | ErrorResponse | None:
    """Refund a delivery

    Args:
        delivery_id (str):
        idempotency_key (str):
        body (RefundDeliveryRequest | Unset): How much of the order to refund. Both fields are
            optional.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return sync_detailed(
        delivery_id=delivery_id,
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: RefundDeliveryRequest | Unset = UNSET,
    idempotency_key: str,
) -> Response[Delivery | ErrorResponse]:
    """Refund a delivery

    Args:
        delivery_id (str):
        idempotency_key (str):
        body (RefundDeliveryRequest | Unset): How much of the order to refund. Both fields are
            optional.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: RefundDeliveryRequest | Unset = UNSET,
    idempotency_key: str,
) -> Delivery | ErrorResponse | None:
    """Refund a delivery

    Args:
        delivery_id (str):
        idempotency_key (str):
        body (RefundDeliveryRequest | Unset): How much of the order to refund. Both fields are
            optional.

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
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
