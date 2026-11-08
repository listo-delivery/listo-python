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
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/deliveries/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Delivery | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Delivery.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Delivery | ErrorResponse]:
    """Fetch a delivery

     Fetches one delivery by its `dlv_` id.

    `charges` carries what a trip that was driven but wasted was billed
    at: the delivery fee for each leg driven, less your own store markup.
    It is empty on almost every delivery. Each entry's
    `type` is one of exactly two values, and they are the ones to branch on
    when you bill it back to your own merchant:

    - `cancellation_fee`, for a cancellation late enough that a courier was
      already working on the order. One leg, so one delivery fee.
    - `return_fee`, for a return trip after a failed dropoff. A return
      bills as ONE entry covering both legs of the journey, not two, so it
      is twice what a cancellation on the same order would have been.

    `amount_cents` is positive here, because it states what you were
    charged. The same movement on `GET /v1/ledger` is a signed row, so it
    reads negative there.

    **This amount changed on 2026-08-29.** It used to be what the wasted
    trip cost Listo; it is now the delivery fee for the legs that were
    driven, which is a larger number on the same orders. Nothing about the
    shape of this field moved, so anything that reads the amount rather
    than assuming it keeps working unchanged.

    A charge can arrive on the delivery's final `delivery.status_changed`
    event or, when the cost settles afterwards, on a later
    `delivery.updated`. You cannot assume which, so read `charges` on both:
    billing the moment a delivery reaches its terminal status bills short
    on every order whose cost landed late.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
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
) -> Delivery | ErrorResponse | None:
    """Fetch a delivery

     Fetches one delivery by its `dlv_` id.

    `charges` carries what a trip that was driven but wasted was billed
    at: the delivery fee for each leg driven, less your own store markup.
    It is empty on almost every delivery. Each entry's
    `type` is one of exactly two values, and they are the ones to branch on
    when you bill it back to your own merchant:

    - `cancellation_fee`, for a cancellation late enough that a courier was
      already working on the order. One leg, so one delivery fee.
    - `return_fee`, for a return trip after a failed dropoff. A return
      bills as ONE entry covering both legs of the journey, not two, so it
      is twice what a cancellation on the same order would have been.

    `amount_cents` is positive here, because it states what you were
    charged. The same movement on `GET /v1/ledger` is a signed row, so it
    reads negative there.

    **This amount changed on 2026-08-29.** It used to be what the wasted
    trip cost Listo; it is now the delivery fee for the legs that were
    driven, which is a larger number on the same orders. Nothing about the
    shape of this field moved, so anything that reads the amount rather
    than assuming it keeps working unchanged.

    A charge can arrive on the delivery's final `delivery.status_changed`
    event or, when the cost settles afterwards, on a later
    `delivery.updated`. You cannot assume which, so read `charges` on both:
    billing the moment a delivery reaches its terminal status bills short
    on every order whose cost landed late.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Delivery | ErrorResponse]:
    """Fetch a delivery

     Fetches one delivery by its `dlv_` id.

    `charges` carries what a trip that was driven but wasted was billed
    at: the delivery fee for each leg driven, less your own store markup.
    It is empty on almost every delivery. Each entry's
    `type` is one of exactly two values, and they are the ones to branch on
    when you bill it back to your own merchant:

    - `cancellation_fee`, for a cancellation late enough that a courier was
      already working on the order. One leg, so one delivery fee.
    - `return_fee`, for a return trip after a failed dropoff. A return
      bills as ONE entry covering both legs of the journey, not two, so it
      is twice what a cancellation on the same order would have been.

    `amount_cents` is positive here, because it states what you were
    charged. The same movement on `GET /v1/ledger` is a signed row, so it
    reads negative there.

    **This amount changed on 2026-08-29.** It used to be what the wasted
    trip cost Listo; it is now the delivery fee for the legs that were
    driven, which is a larger number on the same orders. Nothing about the
    shape of this field moved, so anything that reads the amount rather
    than assuming it keeps working unchanged.

    A charge can arrive on the delivery's final `delivery.status_changed`
    event or, when the cost settles afterwards, on a later
    `delivery.updated`. You cannot assume which, so read `charges` on both:
    billing the moment a delivery reaches its terminal status bills short
    on every order whose cost landed late.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
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
) -> Delivery | ErrorResponse | None:
    """Fetch a delivery

     Fetches one delivery by its `dlv_` id.

    `charges` carries what a trip that was driven but wasted was billed
    at: the delivery fee for each leg driven, less your own store markup.
    It is empty on almost every delivery. Each entry's
    `type` is one of exactly two values, and they are the ones to branch on
    when you bill it back to your own merchant:

    - `cancellation_fee`, for a cancellation late enough that a courier was
      already working on the order. One leg, so one delivery fee.
    - `return_fee`, for a return trip after a failed dropoff. A return
      bills as ONE entry covering both legs of the journey, not two, so it
      is twice what a cancellation on the same order would have been.

    `amount_cents` is positive here, because it states what you were
    charged. The same movement on `GET /v1/ledger` is a signed row, so it
    reads negative there.

    **This amount changed on 2026-08-29.** It used to be what the wasted
    trip cost Listo; it is now the delivery fee for the legs that were
    driven, which is a larger number on the same orders. Nothing about the
    shape of this field moved, so anything that reads the amount rather
    than assuming it keeps working unchanged.

    A charge can arrive on the delivery's final `delivery.status_changed`
    event or, when the cost settles afterwards, on a later
    `delivery.updated`. You cannot assume which, so read `charges` on both:
    billing the moment a delivery reaches its terminal status bills short
    on every order whose cost landed late.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
