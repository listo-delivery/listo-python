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
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/stores/{store_id}/plan".format(
            store_id=quote(str(store_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Store | None:
    if response.status_code == 200:
        response_200 = Store.from_dict(response.json())

        return response_200

    if response.status_code == 402:
        response_402 = ErrorResponse.from_dict(response.json())

        return response_402

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
    idempotency_key: str,
) -> Response[ErrorResponse | Store]:
    """Reactivate a store's plan

     Restarts a plan that ended. The first month is charged in this request,
    from your live balance or your saved card, and the response is the
    store with `plan.status` `active`.

    `Idempotency-Key` is required, and a repeat with the same key answers
    the original response. Live keys only: a test key gets `404 not_found`.

    `402 insufficient_balance` when neither your balance nor your saved card
    can pay the month: nothing was charged and the plan stays ended, and the
    `message` gives what is available and what is due. `409
    not_reactivatable` when the plan has not ended: a `canceling` plan is
    undone with `DELETE /v1/stores/{store_id}/plan_cancellation`, and a
    `past_due` one starts again when its charge goes through, and a store
    whose first month is still `awaiting_payment` is charged by itself as
    soon as your balance or card covers it. It also
    answers when the restaurant pays its own plan, which it buys in its own
    console and is not yours to reactivate. `409
    charge_in_progress`, which is `retryable`, while a card charge for the
    plan is still with the bank: nothing new was charged, so read the store
    again shortly.

    Args:
        store_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: str,
) -> ErrorResponse | Store | None:
    """Reactivate a store's plan

     Restarts a plan that ended. The first month is charged in this request,
    from your live balance or your saved card, and the response is the
    store with `plan.status` `active`.

    `Idempotency-Key` is required, and a repeat with the same key answers
    the original response. Live keys only: a test key gets `404 not_found`.

    `402 insufficient_balance` when neither your balance nor your saved card
    can pay the month: nothing was charged and the plan stays ended, and the
    `message` gives what is available and what is due. `409
    not_reactivatable` when the plan has not ended: a `canceling` plan is
    undone with `DELETE /v1/stores/{store_id}/plan_cancellation`, and a
    `past_due` one starts again when its charge goes through, and a store
    whose first month is still `awaiting_payment` is charged by itself as
    soon as your balance or card covers it. It also
    answers when the restaurant pays its own plan, which it buys in its own
    console and is not yours to reactivate. `409
    charge_in_progress`, which is `retryable`, while a card charge for the
    plan is still with the bank: nothing new was charged, so read the store
    again shortly.

    Args:
        store_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: str,
) -> Response[ErrorResponse | Store]:
    """Reactivate a store's plan

     Restarts a plan that ended. The first month is charged in this request,
    from your live balance or your saved card, and the response is the
    store with `plan.status` `active`.

    `Idempotency-Key` is required, and a repeat with the same key answers
    the original response. Live keys only: a test key gets `404 not_found`.

    `402 insufficient_balance` when neither your balance nor your saved card
    can pay the month: nothing was charged and the plan stays ended, and the
    `message` gives what is available and what is due. `409
    not_reactivatable` when the plan has not ended: a `canceling` plan is
    undone with `DELETE /v1/stores/{store_id}/plan_cancellation`, and a
    `past_due` one starts again when its charge goes through, and a store
    whose first month is still `awaiting_payment` is charged by itself as
    soon as your balance or card covers it. It also
    answers when the restaurant pays its own plan, which it buys in its own
    console and is not yours to reactivate. `409
    charge_in_progress`, which is `retryable`, while a card charge for the
    plan is still with the bank: nothing new was charged, so read the store
    again shortly.

    Args:
        store_id (str):
        idempotency_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    idempotency_key: str,
) -> ErrorResponse | Store | None:
    """Reactivate a store's plan

     Restarts a plan that ended. The first month is charged in this request,
    from your live balance or your saved card, and the response is the
    store with `plan.status` `active`.

    `Idempotency-Key` is required, and a repeat with the same key answers
    the original response. Live keys only: a test key gets `404 not_found`.

    `402 insufficient_balance` when neither your balance nor your saved card
    can pay the month: nothing was charged and the plan stays ended, and the
    `message` gives what is available and what is due. `409
    not_reactivatable` when the plan has not ended: a `canceling` plan is
    undone with `DELETE /v1/stores/{store_id}/plan_cancellation`, and a
    `past_due` one starts again when its charge goes through, and a store
    whose first month is still `awaiting_payment` is charged by itself as
    soon as your balance or card covers it. It also
    answers when the restaurant pays its own plan, which it buys in its own
    console and is not yours to reactivate. `409
    charge_in_progress`, which is `retryable`, while a card charge for the
    plan is still with the bank: nothing new was charged, so read the store
    again shortly.

    Args:
        store_id (str):
        idempotency_key (str):

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
            idempotency_key=idempotency_key,
        )
    ).parsed
