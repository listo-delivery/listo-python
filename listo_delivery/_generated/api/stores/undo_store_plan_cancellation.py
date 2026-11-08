from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.store import Store
from ...types import Response


def _get_kwargs(
    store_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/stores/{store_id}/plan_cancellation".format(
            store_id=quote(str(store_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Store | None:
    if response.status_code == 200:
        response_200 = Store.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Store]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Store]:
    """Undo a store's plan cancellation

     Undoes a cancellation before it takes effect. The plan goes back to
    `active` and renews on its usual day, and nothing is charged now. A
    plan that is not being canceled answers `200` with the store as it is,
    so the call is safe to repeat.

    `409 plan_ended` once the cancellation has taken effect: restart the
    plan with `POST /v1/stores/{store_id}/plan` instead. `409
    not_cancellable` while the plan is still paid by a restaurant that
    connected to you, because its cancellation is not yours to undo.

    Args:
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Store | None:
    """Undo a store's plan cancellation

     Undoes a cancellation before it takes effect. The plan goes back to
    `active` and renews on its usual day, and nothing is charged now. A
    plan that is not being canceled answers `200` with the store as it is,
    so the call is safe to repeat.

    `409 plan_ended` once the cancellation has taken effect: restart the
    plan with `POST /v1/stores/{store_id}/plan` instead. `409
    not_cancellable` while the plan is still paid by a restaurant that
    connected to you, because its cancellation is not yours to undo.

    Args:
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Store]:
    """Undo a store's plan cancellation

     Undoes a cancellation before it takes effect. The plan goes back to
    `active` and renews on its usual day, and nothing is charged now. A
    plan that is not being canceled answers `200` with the store as it is,
    so the call is safe to repeat.

    `409 plan_ended` once the cancellation has taken effect: restart the
    plan with `POST /v1/stores/{store_id}/plan` instead. `409
    not_cancellable` while the plan is still paid by a restaurant that
    connected to you, because its cancellation is not yours to undo.

    Args:
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Store | None:
    """Undo a store's plan cancellation

     Undoes a cancellation before it takes effect. The plan goes back to
    `active` and renews on its usual day, and nothing is charged now. A
    plan that is not being canceled answers `200` with the store as it is,
    so the call is safe to repeat.

    `409 plan_ended` once the cancellation has taken effect: restart the
    plan with `POST /v1/stores/{store_id}/plan` instead. `409
    not_cancellable` while the plan is still paid by a restaurant that
    connected to you, because its cancellation is not yours to undo.

    Args:
        store_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
        )
    ).parsed
