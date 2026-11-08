from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_courier_location_event import DeliveryCourierLocationEvent
from ...models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
from ...models.delivery_status_changed_event import DeliveryStatusChangedEvent
from ...models.delivery_updated_event import DeliveryUpdatedEvent
from ...models.error_response import ErrorResponse
from ...models.send_test_webhook_request import SendTestWebhookRequest
from ...models.store_connected_event import StoreConnectedEvent
from ...models.store_updated_event import StoreUpdatedEvent
from ...models.withdrawal_updated_event import WithdrawalUpdatedEvent
from ...types import Response


def _get_kwargs(
    *,
    body: SendTestWebhookRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/test_webhooks",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
    | None
):
    if response.status_code == 202:

        def _parse_response_202(
            data: object,
        ) -> (
            DeliveryCourierLocationEvent
            | DeliveryMessageSkippedEvent
            | DeliveryStatusChangedEvent
            | DeliveryUpdatedEvent
            | StoreConnectedEvent
            | StoreUpdatedEvent
            | WithdrawalUpdatedEvent
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_0 = (
                    DeliveryStatusChangedEvent.from_dict(data)
                )

                return componentsschemas_webhook_event_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_1 = DeliveryUpdatedEvent.from_dict(
                    data
                )

                return componentsschemas_webhook_event_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_2 = (
                    DeliveryCourierLocationEvent.from_dict(data)
                )

                return componentsschemas_webhook_event_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_3 = (
                    WithdrawalUpdatedEvent.from_dict(data)
                )

                return componentsschemas_webhook_event_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_4 = StoreUpdatedEvent.from_dict(
                    data
                )

                return componentsschemas_webhook_event_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_5 = StoreConnectedEvent.from_dict(
                    data
                )

                return componentsschemas_webhook_event_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_webhook_event_type_6 = (
                DeliveryMessageSkippedEvent.from_dict(data)
            )

            return componentsschemas_webhook_event_type_6

        response_202 = _parse_response_202(response.json())

        return response_202

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SendTestWebhookRequest,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
]:
    """Send a test webhook

     Sends a synthetic event of one published `type` to your webhook URL, so
    you can exercise an endpoint without placing an order. The answer is `202`
    with the event as your endpoint receives it, and the attempt appears on
    `GET /v1/webhook_deliveries` like any other.

    - **`test: true` is on the envelope.** A real event never carries the
      field. Branch on it before doing anything with consequences.
    - **Its ids resolve to nothing.** `data` is a realistic sample of the
      type, but the delivery, store, withdrawal or quote it names does not
      exist, so reading it back answers `404`.
    - **Either mode.** A test key sends to your test endpoint and a live key
      to your live one. The live endpoint does receive the test event.
    - **Thirty an hour per mode.** The thirty-first is
      `429 test_webhook_limit_reached`, retryable once the hour has moved on.
      `Retry-After` says how many seconds until you can send again.

    A `type` that is not a published event type is `422 validation_failed`
    with `param: "type"`. With no webhook URL configured for the key's mode
    the answer is `409 webhook_endpoint_not_configured`.

    Args:
        body (SendTestWebhookRequest): Which event to send a sample of.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse]
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
    body: SendTestWebhookRequest,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
    | None
):
    """Send a test webhook

     Sends a synthetic event of one published `type` to your webhook URL, so
    you can exercise an endpoint without placing an order. The answer is `202`
    with the event as your endpoint receives it, and the attempt appears on
    `GET /v1/webhook_deliveries` like any other.

    - **`test: true` is on the envelope.** A real event never carries the
      field. Branch on it before doing anything with consequences.
    - **Its ids resolve to nothing.** `data` is a realistic sample of the
      type, but the delivery, store, withdrawal or quote it names does not
      exist, so reading it back answers `404`.
    - **Either mode.** A test key sends to your test endpoint and a live key
      to your live one. The live endpoint does receive the test event.
    - **Thirty an hour per mode.** The thirty-first is
      `429 test_webhook_limit_reached`, retryable once the hour has moved on.
      `Retry-After` says how many seconds until you can send again.

    A `type` that is not a published event type is `422 validation_failed`
    with `param: "type"`. With no webhook URL configured for the key's mode
    the answer is `409 webhook_endpoint_not_configured`.

    Args:
        body (SendTestWebhookRequest): Which event to send a sample of.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SendTestWebhookRequest,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
]:
    """Send a test webhook

     Sends a synthetic event of one published `type` to your webhook URL, so
    you can exercise an endpoint without placing an order. The answer is `202`
    with the event as your endpoint receives it, and the attempt appears on
    `GET /v1/webhook_deliveries` like any other.

    - **`test: true` is on the envelope.** A real event never carries the
      field. Branch on it before doing anything with consequences.
    - **Its ids resolve to nothing.** `data` is a realistic sample of the
      type, but the delivery, store, withdrawal or quote it names does not
      exist, so reading it back answers `404`.
    - **Either mode.** A test key sends to your test endpoint and a live key
      to your live one. The live endpoint does receive the test event.
    - **Thirty an hour per mode.** The thirty-first is
      `429 test_webhook_limit_reached`, retryable once the hour has moved on.
      `Retry-After` says how many seconds until you can send again.

    A `type` that is not a published event type is `422 validation_failed`
    with `param: "type"`. With no webhook URL configured for the key's mode
    the answer is `409 webhook_endpoint_not_configured`.

    Args:
        body (SendTestWebhookRequest): Which event to send a sample of.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SendTestWebhookRequest,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
    | None
):
    """Send a test webhook

     Sends a synthetic event of one published `type` to your webhook URL, so
    you can exercise an endpoint without placing an order. The answer is `202`
    with the event as your endpoint receives it, and the attempt appears on
    `GET /v1/webhook_deliveries` like any other.

    - **`test: true` is on the envelope.** A real event never carries the
      field. Branch on it before doing anything with consequences.
    - **Its ids resolve to nothing.** `data` is a realistic sample of the
      type, but the delivery, store, withdrawal or quote it names does not
      exist, so reading it back answers `404`.
    - **Either mode.** A test key sends to your test endpoint and a live key
      to your live one. The live endpoint does receive the test event.
    - **Thirty an hour per mode.** The thirty-first is
      `429 test_webhook_limit_reached`, retryable once the hour has moved on.
      `Retry-After` says how many seconds until you can send again.

    A `type` that is not a published event type is `422 validation_failed`
    with `param: "type"`. With no webhook URL configured for the key's mode
    the answer is `409 webhook_endpoint_not_configured`.

    Args:
        body (SendTestWebhookRequest): Which event to send a sample of.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
