from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_courier_location_event import DeliveryCourierLocationEvent
from ...models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
from ...models.delivery_rated_event import DeliveryRatedEvent
from ...models.delivery_status_changed_event import DeliveryStatusChangedEvent
from ...models.delivery_updated_event import DeliveryUpdatedEvent
from ...models.error_response import ErrorResponse
from ...models.store_connected_event import StoreConnectedEvent
from ...models.store_updated_event import StoreUpdatedEvent
from ...models.withdrawal_updated_event import WithdrawalUpdatedEvent
from ...types import Response


def _get_kwargs(
    event_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/events/{event_id}/resend".format(
            event_id=quote(str(event_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
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
            | DeliveryRatedEvent
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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_6 = (
                    DeliveryMessageSkippedEvent.from_dict(data)
                )

                return componentsschemas_webhook_event_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_webhook_event_type_7 = DeliveryRatedEvent.from_dict(data)

            return componentsschemas_webhook_event_type_7

        response_202 = _parse_response_202(response.json())

        return response_202

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

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
    | DeliveryRatedEvent
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
    event_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
]:
    """Send a webhook event again

     Sends one event to your webhook URL again. No request body. The answer is
    `202` with the event's envelope: the send happens right after, and its
    outcome is a new row on `GET /v1/webhook_deliveries` with `resent: true`,
    numbered after the event's last attempt.

    - **Same event, same bytes.** The `id` and the body are the original, so a
      receiver that deduplicates on `id` treats it as the event it already
      saw.
    - **Signed now.** The `X-Listo-Signature` carries the time of the send
      and your current secret, so it verifies however old the event is.
    - **Sent to the current URL** of the key's mode, not the one the event
      was first sent to.
    - **Once.** There is no retry behind a resend; if your endpoint fails you
      see one failed attempt.
    - **Five times an hour per event, and sixty an hour for your whole
      account.** The sixth resend of one event is `429 resend_limit_reached`.
      Your sixty-first resend of any event, in the same mode (a live key and
      a test key count apart, and the API and the dashboard count together),
      is `429 partner_resend_limit_reached`. Both are retryable once the hour
      has moved on, and `Retry-After` says how many seconds until you can
      send again.
    - **Never a courier position.** `delivery.courier_location` events are
      superseded within seconds and are refused with `409 event_not_resendable`.
    - **Needs an endpoint.** With no webhook URL configured for the key's
      mode the answer is `409 webhook_endpoint_not_configured`.

    A resent body is the snapshot from when the event happened. It is meant
    for debugging an endpoint, or for recovering one event you know you
    dropped. To recover where things stand after an outage, re-read
    `GET /v1/deliveries`.

    Args:
        event_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryRatedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
    | None
):
    """Send a webhook event again

     Sends one event to your webhook URL again. No request body. The answer is
    `202` with the event's envelope: the send happens right after, and its
    outcome is a new row on `GET /v1/webhook_deliveries` with `resent: true`,
    numbered after the event's last attempt.

    - **Same event, same bytes.** The `id` and the body are the original, so a
      receiver that deduplicates on `id` treats it as the event it already
      saw.
    - **Signed now.** The `X-Listo-Signature` carries the time of the send
      and your current secret, so it verifies however old the event is.
    - **Sent to the current URL** of the key's mode, not the one the event
      was first sent to.
    - **Once.** There is no retry behind a resend; if your endpoint fails you
      see one failed attempt.
    - **Five times an hour per event, and sixty an hour for your whole
      account.** The sixth resend of one event is `429 resend_limit_reached`.
      Your sixty-first resend of any event, in the same mode (a live key and
      a test key count apart, and the API and the dashboard count together),
      is `429 partner_resend_limit_reached`. Both are retryable once the hour
      has moved on, and `Retry-After` says how many seconds until you can
      send again.
    - **Never a courier position.** `delivery.courier_location` events are
      superseded within seconds and are refused with `409 event_not_resendable`.
    - **Needs an endpoint.** With no webhook URL configured for the key's
      mode the answer is `409 webhook_endpoint_not_configured`.

    A resent body is the snapshot from when the event happened. It is meant
    for debugging an endpoint, or for recovering one event you know you
    dropped. To recover where things stand after an outage, re-read
    `GET /v1/deliveries`.

    Args:
        event_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryRatedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
]:
    """Send a webhook event again

     Sends one event to your webhook URL again. No request body. The answer is
    `202` with the event's envelope: the send happens right after, and its
    outcome is a new row on `GET /v1/webhook_deliveries` with `resent: true`,
    numbered after the event's last attempt.

    - **Same event, same bytes.** The `id` and the body are the original, so a
      receiver that deduplicates on `id` treats it as the event it already
      saw.
    - **Signed now.** The `X-Listo-Signature` carries the time of the send
      and your current secret, so it verifies however old the event is.
    - **Sent to the current URL** of the key's mode, not the one the event
      was first sent to.
    - **Once.** There is no retry behind a resend; if your endpoint fails you
      see one failed attempt.
    - **Five times an hour per event, and sixty an hour for your whole
      account.** The sixth resend of one event is `429 resend_limit_reached`.
      Your sixty-first resend of any event, in the same mode (a live key and
      a test key count apart, and the API and the dashboard count together),
      is `429 partner_resend_limit_reached`. Both are retryable once the hour
      has moved on, and `Retry-After` says how many seconds until you can
      send again.
    - **Never a courier position.** `delivery.courier_location` events are
      superseded within seconds and are refused with `409 event_not_resendable`.
    - **Needs an endpoint.** With no webhook URL configured for the key's
      mode the answer is `409 webhook_endpoint_not_configured`.

    A resent body is the snapshot from when the event happened. It is meant
    for debugging an endpoint, or for recovering one event you know you
    dropped. To recover where things stand after an outage, re-read
    `GET /v1/deliveries`.

    Args:
        event_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryRatedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | ErrorResponse
    | None
):
    """Send a webhook event again

     Sends one event to your webhook URL again. No request body. The answer is
    `202` with the event's envelope: the send happens right after, and its
    outcome is a new row on `GET /v1/webhook_deliveries` with `resent: true`,
    numbered after the event's last attempt.

    - **Same event, same bytes.** The `id` and the body are the original, so a
      receiver that deduplicates on `id` treats it as the event it already
      saw.
    - **Signed now.** The `X-Listo-Signature` carries the time of the send
      and your current secret, so it verifies however old the event is.
    - **Sent to the current URL** of the key's mode, not the one the event
      was first sent to.
    - **Once.** There is no retry behind a resend; if your endpoint fails you
      see one failed attempt.
    - **Five times an hour per event, and sixty an hour for your whole
      account.** The sixth resend of one event is `429 resend_limit_reached`.
      Your sixty-first resend of any event, in the same mode (a live key and
      a test key count apart, and the API and the dashboard count together),
      is `429 partner_resend_limit_reached`. Both are retryable once the hour
      has moved on, and `Retry-After` says how many seconds until you can
      send again.
    - **Never a courier position.** `delivery.courier_location` events are
      superseded within seconds and are refused with `409 event_not_resendable`.
    - **Needs an endpoint.** With no webhook URL configured for the key's
      mode the answer is `409 webhook_endpoint_not_configured`.

    A resent body is the snapshot from when the event happened. It is meant
    for debugging an endpoint, or for recovering one event you know you
    dropped. To recover where things stand after an outage, re-read
    `GET /v1/deliveries`.

    Args:
        event_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryRatedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent | ErrorResponse
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
        )
    ).parsed
