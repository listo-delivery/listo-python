from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_courier_location_event import DeliveryCourierLocationEvent
from ...models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
from ...models.delivery_status_changed_event import DeliveryStatusChangedEvent
from ...models.delivery_updated_event import DeliveryUpdatedEvent
from ...models.store_connected_event import StoreConnectedEvent
from ...models.store_updated_event import StoreUpdatedEvent
from ...models.withdrawal_updated_event import WithdrawalUpdatedEvent
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/events/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

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
    | None
):
    if response.status_code == 200:

        def _parse_response_200(
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

        response_200 = _parse_response_200(response.json())

        return response_200

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
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
]:
    """Retrieve a webhook event

     One event, as the envelope your endpoint is sent. An event that is not
    yours, or belongs to the other mode, is `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | None
):
    """Retrieve a webhook event

     One event, as the envelope your endpoint is sent. An event that is not
    yours, or belongs to the other mode, is `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
]:
    """Retrieve a webhook event

     One event, as the envelope your endpoint is sent. An event that is not
    yours, or belongs to the other mode, is `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
    | None
):
    """Retrieve a webhook event

     One event, as the envelope your endpoint is sent. An event that is not
    yours, or belongs to the other mode, is `404 not_found`.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent | WithdrawalUpdatedEvent
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
