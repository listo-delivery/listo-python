from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cancel_delivery_request import CancelDeliveryRequest
from ...models.delivery import Delivery
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    delivery_id: str,
    *,
    body: CancelDeliveryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/deliveries/{delivery_id}/cancellations".format(
            delivery_id=quote(str(delivery_id), safe=""),
        ),
    }

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
    body: CancelDeliveryRequest,
) -> Response[Delivery | ErrorResponse]:
    """Cancel a delivery

     Cancels a delivery. Valid from every status except `delivered`,
    `canceled`, `returned` and `returning`.

    `returning` is refused for the same substance as the three terminal
    ones even though it is not terminal: the drop-off has already failed,
    the courier is already carrying the order back, and both trips are
    already charged. There is nothing left to call off, so it answers
    `409 not_cancellable`.

    The courier is called off BEFORE anything changes on our side, so a
    cancellation that fails leaves the delivery live and untouched rather
    than telling you it stopped while a courier is still driving. That case
    answers `409 cancel_failed` with `retryable: true`.

    Cancelling an already-cancelled delivery is not an error: it answers
    `200` with the current object.

    Cancellation charges depend on how far the trip had progressed and are
    posted to your balance as a separate ledger entry, never folded into the
    delivery's fee.

    Args:
        delivery_id (str):
        body (CancelDeliveryRequest): Why the order is being canceled.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: CancelDeliveryRequest,
) -> Delivery | ErrorResponse | None:
    """Cancel a delivery

     Cancels a delivery. Valid from every status except `delivered`,
    `canceled`, `returned` and `returning`.

    `returning` is refused for the same substance as the three terminal
    ones even though it is not terminal: the drop-off has already failed,
    the courier is already carrying the order back, and both trips are
    already charged. There is nothing left to call off, so it answers
    `409 not_cancellable`.

    The courier is called off BEFORE anything changes on our side, so a
    cancellation that fails leaves the delivery live and untouched rather
    than telling you it stopped while a courier is still driving. That case
    answers `409 cancel_failed` with `retryable: true`.

    Cancelling an already-cancelled delivery is not an error: it answers
    `200` with the current object.

    Cancellation charges depend on how far the trip had progressed and are
    posted to your balance as a separate ledger entry, never folded into the
    delivery's fee.

    Args:
        delivery_id (str):
        body (CancelDeliveryRequest): Why the order is being canceled.

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
    ).parsed


async def asyncio_detailed(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: CancelDeliveryRequest,
) -> Response[Delivery | ErrorResponse]:
    """Cancel a delivery

     Cancels a delivery. Valid from every status except `delivered`,
    `canceled`, `returned` and `returning`.

    `returning` is refused for the same substance as the three terminal
    ones even though it is not terminal: the drop-off has already failed,
    the courier is already carrying the order back, and both trips are
    already charged. There is nothing left to call off, so it answers
    `409 not_cancellable`.

    The courier is called off BEFORE anything changes on our side, so a
    cancellation that fails leaves the delivery live and untouched rather
    than telling you it stopped while a courier is still driving. That case
    answers `409 cancel_failed` with `retryable: true`.

    Cancelling an already-cancelled delivery is not an error: it answers
    `200` with the current object.

    Cancellation charges depend on how far the trip had progressed and are
    posted to your balance as a separate ledger entry, never folded into the
    delivery's fee.

    Args:
        delivery_id (str):
        body (CancelDeliveryRequest): Why the order is being canceled.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        delivery_id=delivery_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    delivery_id: str,
    *,
    client: AuthenticatedClient,
    body: CancelDeliveryRequest,
) -> Delivery | ErrorResponse | None:
    """Cancel a delivery

     Cancels a delivery. Valid from every status except `delivered`,
    `canceled`, `returned` and `returning`.

    `returning` is refused for the same substance as the three terminal
    ones even though it is not terminal: the drop-off has already failed,
    the courier is already carrying the order back, and both trips are
    already charged. There is nothing left to call off, so it answers
    `409 not_cancellable`.

    The courier is called off BEFORE anything changes on our side, so a
    cancellation that fails leaves the delivery live and untouched rather
    than telling you it stopped while a courier is still driving. That case
    answers `409 cancel_failed` with `retryable: true`.

    Cancelling an already-cancelled delivery is not an error: it answers
    `200` with the current object.

    Cancellation charges depend on how far the trip had progressed and are
    posted to your balance as a separate ledger entry, never folded into the
    delivery's fee.

    Args:
        delivery_id (str):
        body (CancelDeliveryRequest): Why the order is being canceled.

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
        )
    ).parsed
