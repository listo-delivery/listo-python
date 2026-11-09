from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.list_webhook_deliveries_status import ListWebhookDeliveriesStatus
from ...models.webhook_delivery_list import WebhookDeliveryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    event_id: str | Unset = UNSET,
    status: ListWebhookDeliveriesStatus | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["event_id"] = event_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/webhook_deliveries",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | WebhookDeliveryList | None:
    if response.status_code == 200:
        response_200 = WebhookDeliveryList.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | WebhookDeliveryList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    event_id: str | Unset = UNSET,
    status: ListWebhookDeliveriesStatus | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | WebhookDeliveryList]:
    """List webhook delivery attempts

     Every attempt Listo made to POST an event to your webhook URL, newest
    first, keyset-paginated: the URL, the status your endpoint answered with,
    the first 500 characters of its body, how long it took and whether it
    counted as a success. An event has one attempt per try: the first send,
    each automatic retry, and each resend you asked for (`resent: true`).

    Filter by `event_id` (the attempts for one event), `status`
    (`failed` or `succeeded`), `created_after` and `created_before`. An
    `event_id` that is not one of yours is `404 not_found`, so an empty page
    always means that event had no attempts.

    A `status_code` of null means nothing answered at all (a timeout, a
    refused connection, a certificate error) and `error_message` says which.
    An event with no attempts has not been sent yet, or had no endpoint configured for its mode
    when it happened.

    Args:
        event_id (str | Unset):
        status (ListWebhookDeliveriesStatus | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WebhookDeliveryList]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        status=status,
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
    event_id: str | Unset = UNSET,
    status: ListWebhookDeliveriesStatus | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | WebhookDeliveryList | None:
    """List webhook delivery attempts

     Every attempt Listo made to POST an event to your webhook URL, newest
    first, keyset-paginated: the URL, the status your endpoint answered with,
    the first 500 characters of its body, how long it took and whether it
    counted as a success. An event has one attempt per try: the first send,
    each automatic retry, and each resend you asked for (`resent: true`).

    Filter by `event_id` (the attempts for one event), `status`
    (`failed` or `succeeded`), `created_after` and `created_before`. An
    `event_id` that is not one of yours is `404 not_found`, so an empty page
    always means that event had no attempts.

    A `status_code` of null means nothing answered at all (a timeout, a
    refused connection, a certificate error) and `error_message` says which.
    An event with no attempts has not been sent yet, or had no endpoint configured for its mode
    when it happened.

    Args:
        event_id (str | Unset):
        status (ListWebhookDeliveriesStatus | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WebhookDeliveryList
    """

    return sync_detailed(
        client=client,
        event_id=event_id,
        status=status,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    event_id: str | Unset = UNSET,
    status: ListWebhookDeliveriesStatus | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ErrorResponse | WebhookDeliveryList]:
    """List webhook delivery attempts

     Every attempt Listo made to POST an event to your webhook URL, newest
    first, keyset-paginated: the URL, the status your endpoint answered with,
    the first 500 characters of its body, how long it took and whether it
    counted as a success. An event has one attempt per try: the first send,
    each automatic retry, and each resend you asked for (`resent: true`).

    Filter by `event_id` (the attempts for one event), `status`
    (`failed` or `succeeded`), `created_after` and `created_before`. An
    `event_id` that is not one of yours is `404 not_found`, so an empty page
    always means that event had no attempts.

    A `status_code` of null means nothing answered at all (a timeout, a
    refused connection, a certificate error) and `error_message` says which.
    An event with no attempts has not been sent yet, or had no endpoint configured for its mode
    when it happened.

    Args:
        event_id (str | Unset):
        status (ListWebhookDeliveriesStatus | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | WebhookDeliveryList]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        status=status,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    event_id: str | Unset = UNSET,
    status: ListWebhookDeliveriesStatus | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ErrorResponse | WebhookDeliveryList | None:
    """List webhook delivery attempts

     Every attempt Listo made to POST an event to your webhook URL, newest
    first, keyset-paginated: the URL, the status your endpoint answered with,
    the first 500 characters of its body, how long it took and whether it
    counted as a success. An event has one attempt per try: the first send,
    each automatic retry, and each resend you asked for (`resent: true`).

    Filter by `event_id` (the attempts for one event), `status`
    (`failed` or `succeeded`), `created_after` and `created_before`. An
    `event_id` that is not one of yours is `404 not_found`, so an empty page
    always means that event had no attempts.

    A `status_code` of null means nothing answered at all (a timeout, a
    refused connection, a certificate error) and `error_message` says which.
    An event with no attempts has not been sent yet, or had no endpoint configured for its mode
    when it happened.

    Args:
        event_id (str | Unset):
        status (ListWebhookDeliveriesStatus | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | WebhookDeliveryList
    """

    return (
        await asyncio_detailed(
            client=client,
            event_id=event_id,
            status=status,
            created_after=created_after,
            created_before=created_before,
            cursor=cursor,
        )
    ).parsed
