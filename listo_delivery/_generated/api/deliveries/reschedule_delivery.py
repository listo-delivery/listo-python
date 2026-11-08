from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery import Delivery
from ...models.error_response import ErrorResponse
from ...models.reschedule_delivery_request import RescheduleDeliveryRequest
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: RescheduleDeliveryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/deliveries/{id}".format(
            id=quote(str(id), safe=""),
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

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

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
    body: RescheduleDeliveryRequest,
) -> Response[Delivery | ErrorResponse]:
    """Update a delivery

     Changes a delivery. It accepts exactly two fields, independently or
    together: `pickup_ready_at`, which moves a scheduled pickup, and
    `dropoff.notes`, which corrects what the courier is told about the
    drop-off. A body naming neither is a `422` on `pickup_ready_at`.

    `pickup_ready_at` is valid only while the delivery is still
    `scheduled`, and passing the literal string `now` dispatches
    immediately. Once the delivery has left that status the window is fixed
    and this is a `409 not_reschedulable`.

    `dropoff.notes` is the one thing you can still tell a courier after the
    order is out: a corrected phone number, a gate they will not find. Up
    to 280 characters, the same ceiling the create enforces; a longer one
    is refused rather than truncated, because a courier reading half an
    instruction is worse than you being asked to shorten it.

    Its window is much wider. The note stays editable while the delivery is
    `scheduled`, `awaiting_payment`, `dispatching`, `picking_up` or
    `en_route` and the courier has not yet begun arriving at the customer.
    From the moment they are about to reach the drop-off, and on any
    delivery that has finished, it is `409 not_editable`. A delivery held
    for a drop-off location is outside the window too: what it needs is the
    location, not a note about a door nobody has found.

    Omitting `dropoff.notes` leaves the note exactly as it is and says
    nothing to the courier about it, so moving a pickup window never
    re-issues drop-off instructions. Sending `null` is the opposite
    request: it clears the note, and the delivery reads back a `null`
    note afterwards. An empty or whitespace-only string means the same
    thing as `null`.

    A body carrying BOTH fields is decided together. Both state checks run
    before anything is sent or written, so if either change is refused the
    whole request is refused and this delivery's record is left untouched.
    You get one error code back, and `not_reschedulable` is the one
    returned when both are refused; repeating the same body is the complete
    request again.

    One caveat worth knowing, because you cannot see it in the response: a
    combined body reaches the courier as two changes, the pickup window
    first and the note second. If the note is refused, the request errors
    and this delivery's record still changes nothing, but the pickup window
    has already moved. Re-read the delivery after a refused PATCH that
    named `pickup_ready_at`, or send the two fields as two requests if you
    want no ambiguity at all.

    Args:
        id (str):
        body (RescheduleDeliveryRequest): What to change on an order. Send at least one of the two
            fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RescheduleDeliveryRequest,
) -> Delivery | ErrorResponse | None:
    """Update a delivery

     Changes a delivery. It accepts exactly two fields, independently or
    together: `pickup_ready_at`, which moves a scheduled pickup, and
    `dropoff.notes`, which corrects what the courier is told about the
    drop-off. A body naming neither is a `422` on `pickup_ready_at`.

    `pickup_ready_at` is valid only while the delivery is still
    `scheduled`, and passing the literal string `now` dispatches
    immediately. Once the delivery has left that status the window is fixed
    and this is a `409 not_reschedulable`.

    `dropoff.notes` is the one thing you can still tell a courier after the
    order is out: a corrected phone number, a gate they will not find. Up
    to 280 characters, the same ceiling the create enforces; a longer one
    is refused rather than truncated, because a courier reading half an
    instruction is worse than you being asked to shorten it.

    Its window is much wider. The note stays editable while the delivery is
    `scheduled`, `awaiting_payment`, `dispatching`, `picking_up` or
    `en_route` and the courier has not yet begun arriving at the customer.
    From the moment they are about to reach the drop-off, and on any
    delivery that has finished, it is `409 not_editable`. A delivery held
    for a drop-off location is outside the window too: what it needs is the
    location, not a note about a door nobody has found.

    Omitting `dropoff.notes` leaves the note exactly as it is and says
    nothing to the courier about it, so moving a pickup window never
    re-issues drop-off instructions. Sending `null` is the opposite
    request: it clears the note, and the delivery reads back a `null`
    note afterwards. An empty or whitespace-only string means the same
    thing as `null`.

    A body carrying BOTH fields is decided together. Both state checks run
    before anything is sent or written, so if either change is refused the
    whole request is refused and this delivery's record is left untouched.
    You get one error code back, and `not_reschedulable` is the one
    returned when both are refused; repeating the same body is the complete
    request again.

    One caveat worth knowing, because you cannot see it in the response: a
    combined body reaches the courier as two changes, the pickup window
    first and the note second. If the note is refused, the request errors
    and this delivery's record still changes nothing, but the pickup window
    has already moved. Re-read the delivery after a refused PATCH that
    named `pickup_ready_at`, or send the two fields as two requests if you
    want no ambiguity at all.

    Args:
        id (str):
        body (RescheduleDeliveryRequest): What to change on an order. Send at least one of the two
            fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RescheduleDeliveryRequest,
) -> Response[Delivery | ErrorResponse]:
    """Update a delivery

     Changes a delivery. It accepts exactly two fields, independently or
    together: `pickup_ready_at`, which moves a scheduled pickup, and
    `dropoff.notes`, which corrects what the courier is told about the
    drop-off. A body naming neither is a `422` on `pickup_ready_at`.

    `pickup_ready_at` is valid only while the delivery is still
    `scheduled`, and passing the literal string `now` dispatches
    immediately. Once the delivery has left that status the window is fixed
    and this is a `409 not_reschedulable`.

    `dropoff.notes` is the one thing you can still tell a courier after the
    order is out: a corrected phone number, a gate they will not find. Up
    to 280 characters, the same ceiling the create enforces; a longer one
    is refused rather than truncated, because a courier reading half an
    instruction is worse than you being asked to shorten it.

    Its window is much wider. The note stays editable while the delivery is
    `scheduled`, `awaiting_payment`, `dispatching`, `picking_up` or
    `en_route` and the courier has not yet begun arriving at the customer.
    From the moment they are about to reach the drop-off, and on any
    delivery that has finished, it is `409 not_editable`. A delivery held
    for a drop-off location is outside the window too: what it needs is the
    location, not a note about a door nobody has found.

    Omitting `dropoff.notes` leaves the note exactly as it is and says
    nothing to the courier about it, so moving a pickup window never
    re-issues drop-off instructions. Sending `null` is the opposite
    request: it clears the note, and the delivery reads back a `null`
    note afterwards. An empty or whitespace-only string means the same
    thing as `null`.

    A body carrying BOTH fields is decided together. Both state checks run
    before anything is sent or written, so if either change is refused the
    whole request is refused and this delivery's record is left untouched.
    You get one error code back, and `not_reschedulable` is the one
    returned when both are refused; repeating the same body is the complete
    request again.

    One caveat worth knowing, because you cannot see it in the response: a
    combined body reaches the courier as two changes, the pickup window
    first and the note second. If the note is refused, the request errors
    and this delivery's record still changes nothing, but the pickup window
    has already moved. Re-read the delivery after a refused PATCH that
    named `pickup_ready_at`, or send the two fields as two requests if you
    want no ambiguity at all.

    Args:
        id (str):
        body (RescheduleDeliveryRequest): What to change on an order. Send at least one of the two
            fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RescheduleDeliveryRequest,
) -> Delivery | ErrorResponse | None:
    """Update a delivery

     Changes a delivery. It accepts exactly two fields, independently or
    together: `pickup_ready_at`, which moves a scheduled pickup, and
    `dropoff.notes`, which corrects what the courier is told about the
    drop-off. A body naming neither is a `422` on `pickup_ready_at`.

    `pickup_ready_at` is valid only while the delivery is still
    `scheduled`, and passing the literal string `now` dispatches
    immediately. Once the delivery has left that status the window is fixed
    and this is a `409 not_reschedulable`.

    `dropoff.notes` is the one thing you can still tell a courier after the
    order is out: a corrected phone number, a gate they will not find. Up
    to 280 characters, the same ceiling the create enforces; a longer one
    is refused rather than truncated, because a courier reading half an
    instruction is worse than you being asked to shorten it.

    Its window is much wider. The note stays editable while the delivery is
    `scheduled`, `awaiting_payment`, `dispatching`, `picking_up` or
    `en_route` and the courier has not yet begun arriving at the customer.
    From the moment they are about to reach the drop-off, and on any
    delivery that has finished, it is `409 not_editable`. A delivery held
    for a drop-off location is outside the window too: what it needs is the
    location, not a note about a door nobody has found.

    Omitting `dropoff.notes` leaves the note exactly as it is and says
    nothing to the courier about it, so moving a pickup window never
    re-issues drop-off instructions. Sending `null` is the opposite
    request: it clears the note, and the delivery reads back a `null`
    note afterwards. An empty or whitespace-only string means the same
    thing as `null`.

    A body carrying BOTH fields is decided together. Both state checks run
    before anything is sent or written, so if either change is refused the
    whole request is refused and this delivery's record is left untouched.
    You get one error code back, and `not_reschedulable` is the one
    returned when both are refused; repeating the same body is the complete
    request again.

    One caveat worth knowing, because you cannot see it in the response: a
    combined body reaches the courier as two changes, the pickup window
    first and the note second. If the note is refused, the request errors
    and this delivery's record still changes nothing, but the pickup window
    has already moved. Re-read the delivery after a refused PATCH that
    named `pickup_ready_at`, or send the two fields as two requests if you
    want no ambiguity at all.

    Args:
        id (str):
        body (RescheduleDeliveryRequest): What to change on an order. Send at least one of the two
            fields.

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
            body=body,
        )
    ).parsed
