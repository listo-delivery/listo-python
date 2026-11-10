from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_delivery_request import CreateDeliveryRequest
from ...models.delivery import Delivery
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CreateDeliveryRequest,
    idempotency_key: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/deliveries",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Delivery | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = Delivery.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

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
    *,
    client: AuthenticatedClient,
    body: CreateDeliveryRequest,
    idempotency_key: str,
) -> Response[Delivery | ErrorResponse]:
    """Create a delivery

     Dispatches a delivery.

    `Idempotency-Key` is required. Send a value you generate per order, and
    retry the same call with the same key if you never saw a response: a
    replay within 24 hours returns the original response, status code
    included, without dispatching a second courier or debiting a second
    time. The same key with a different body is a `409`, and so is a
    repeat sent while the original request is still being processed
    (`idempotency_conflict` both times). That repeat created nothing and
    does not mean the original failed: once the original has answered,
    the same request with the same key replays its answer.

    `dropoff.phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `external_id` is your own order reference. It is unique per key world,
    echoed in every payload and webhook, and filterable on the list, so you
    can reconcile without ever storing our ids.

    `pickup_ready_at` schedules the pickup for a future moment, between 10
    minutes and 29 days out. Absent, the order dispatches now.

    How the customer pays is `payment_method`. `cash` has the courier
    collect at the door, up to a cap. `card` mints a branded payment link
    in `payment.url`, which Listo sends your customer itself by WhatsApp
    (and by SMS when the WhatsApp does not reach them), so you do not need
    to send it; the order holds at `awaiting_payment` until the customer
    pays. `prepaid` means you have
    already been paid and the order dispatches immediately.

    On a `prepaid` create that binds no quote, `business_fee_share` is
    forced to 100 and `business_fee_cap_cents` is ignored, whatever you
    send: you have already collected from your customer, so the whole fee
    is yours. A create that binds a quote is held to the split the quote
    was priced with, so request the quote with `payment_method: prepaid`
    or with no `payment_method`: either is always priced at share 100 and
    binds a `prepaid` create. Any other quote is refused with `422
    validation_failed`, and the first thing that does not match is the one
    named. A quote requested with another `payment_method` (`cash` or
    `card`) is refused naming `payment_method`. A quote whose split is not
    the one a `prepaid` order has (share 100, no ceiling) is refused naming
    `business_fee_share` or `business_fee_cap_cents`, and `error.message`
    says why and what to send instead: a new quote requested with
    `payment_method: prepaid`.

    `vehicle` is `moto` (the default) or `car`, and `manifest.items[].size`
    is `small` (the default), `medium`, `large` or `xlarge`. A trip goes by
    car when you ask for one or when any item is sized `xlarge`, and for no
    other reason. A car is a sedan, never a van, can take longer to assign,
    and adds a surcharge inside `fee_cents`. The delivery's `vehicle` says
    what the trip was priced and dispatched as; `courier.vehicle_type` is
    what actually arrived, which can be a car on a `moto` trip without the
    fee changing.

    A create that binds a quote is held to the vehicle the quote was priced
    as. Leave `vehicle` out and it inherits the quote's. Say `moto` against
    a car quote, `car` against a moto quote, or send an item sized `xlarge`
    against a moto quote, and it is refused with `422 validation_failed`
    naming `vehicle` (or `manifest.items` when the sizes are what
    disagree). Re-quote with the cart you mean to send.

    `simulate` rehearses what goes wrong, and it works on a test key only.
    A live key that sends it is refused with `422 validation_failed`
    naming `simulate`, and so is a value that is not one of the four
    below. Leave it out and the delivery plays the normal happy path.

    - `returned`: the courier reaches the door, cannot hand the order
      over and brings it back. The delivery goes to `returning` and ends
      at `returned` with `failure_reason: customer_unavailable`, and the
      return is billed as a live one is: one `return_fee` entry in
      `charges` covers both legs (see `charges`).
    - `no_courier`: the create answers the same `409
      no_couriers_available` a live create answers when every courier is
      busy, and nothing is created, charged or recorded under your
      `Idempotency-Key`. There is no delivery to retry; repeat the call.
    - `delayed_pickup`: the courier is late. Pickup happens about 25
      minutes after the create and the drop-off about 5 minutes after
      that, counted from `pickup_ready_at` instead when you sent one (the
      delivery waits in `scheduled` until then). It goes through the
      same statuses as the normal run.
    - `courier_reassigned`: the first courier leaves before picking the
      order up and another courier takes the trip, which then completes
      normally. You see the courier on the delivery change while its
      status stays `picking_up`, and the delivery ends `delivered`. It
      plays once the delivery is dispatched and before a courier reaches
      the restaurant, so it may not play if the network assigns a courier
      first.

    In test mode a delivery may go from `dispatching` straight to
    `picking_up` without ever showing a `courier_assigned` status, in
    every scenario. Do not wait for it: `courier_assigned_at` and the
    courier object are filled in.

    There is no scenario that ends a delivery because a courier cancelled:
    a courier who gives up before pickup is a handover, which is what
    `courier_reassigned` plays. The
    same `Idempotency-Key` with a different `simulate` is a `409
    idempotency_conflict`, like any other changed body, once a request has
    used the key (it created a delivery, or it is still being processed).
    A request refused before it created anything, such as the `no_courier`
    409, leaves the key free: send it again with a different `simulate`,
    or none, and it is a new request. A `returned` delivery cannot be
    retried (`409 not_retriable`): its order ended.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, and nothing is dispatched or
    debited. Split it across two deliveries.

    Listo delivers in Mexico. A store that turns out to be somewhere else is
    refused with `422 unsupported_country` and nothing is dispatched or
    debited; it is final rather than retryable, and the same store will be
    refused every time.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, and nothing is dispatched or debited:
    until it is confirmed a courier could be sent to the wrong place.
    Usually the store's address has just changed and the confirmation has
    not landed yet, but not always, so do not read it as "the merchant
    moved". Unlike the refusal above it this one IS retryable, because
    nothing about your request is wrong and the identical call succeeds once
    the pickup point is confirmed.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. There is no `Retry-After` on it for that reason:
    we would be inventing the number. The restaurant can also unblock it
    themselves from their own Listo console, which is usually the faster of
    the two.

    When every courier near the trip is busy as the create prices it, the
    create is refused with `409 no_couriers_available`, and nothing is
    dispatched or debited. It is retryable: repeat the identical request,
    with the same `Idempotency-Key`, after a few minutes, for a bounded
    number of attempts. Nothing was recorded under that key, so the repeat
    creates the order once a courier is free rather than replaying the
    refusal.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, and nothing is dispatched or debited. It is a different
    refusal from `402 insufficient_balance`, which is about your balance:
    read `error.code`, never the status alone. `error.message` names the
    reason (no active plan, a charge that is pending, a plan that ended on a
    given date, a plan whose included deliveries for the cycle are all used,
    or a store that cannot request couriers right now), and it
    is not `retryable`. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A card create (`payment_method: card`) at a store of an account on
    self-serve pricing whose `card_payments` add-on is off is refused with
    `402 add_on_required`, `error.param` `payment_method`, and nothing is
    created or debited. It is not `retryable`: the identical request fails
    until `PATCH /v1/stores/{id}` switches the add-on on, and then the same
    `Idempotency-Key` creates the order. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    A `prepaid` or `card` order whose `order_value_cents` is above the
    store's limit for that payment type is refused with `422
    order_value_over_cap`, with `error.param` `order_value_cents`, and
    nothing is created or debited. The delivery fee does not count toward
    the limit, and a value equal to it is accepted. The limits are on the
    store, in `order_value_limits`. A quote you bind is checked again, so a
    quote priced under a higher limit can be refused here once that limit
    has ended. It is not `retryable`: send a smaller order, or contact Listo
    to raise the store's limit. A `cash` order has its own limit and is
    refused with `cash_over_cap`.

    A dropoff beyond the store's 15 km service area is refused with `422
    out_of_service_area`, which is final. The courier network can also
    refuse the distance of a dropoff at the very edge of that circle, and
    the answer is the same `422`, whether it refuses on the price or on the
    create itself. On the create it comes after the delivery was recorded,
    so the delivery stays, ended at `no_courier` with `failure_reason:
    delivery_failed` under your `external_id`, its fee debit returned in
    full and nothing else charged; replaying the request answers the same
    `422`. Send that order to another address under a new `external_id`.

    A dropoff the courier network does not serve at all, whatever its
    distance from the store, is refused with the same final `422
    out_of_service_area` whenever the create prices the trip. That includes
    a create that binds a quote but has to price it again (a cash order,
    or a quote whose courier price can no longer be booked as it stands).
    Only a create that books the bound quote's courier price as it stands
    meets that refusal at dispatch, after the delivery was recorded, and
    it answers `201` with the delivery ended at `no_courier`.

    Args:
        idempotency_key (str):
        body (CreateDeliveryRequest): The order to dispatch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateDeliveryRequest,
    idempotency_key: str,
) -> Delivery | ErrorResponse | None:
    """Create a delivery

     Dispatches a delivery.

    `Idempotency-Key` is required. Send a value you generate per order, and
    retry the same call with the same key if you never saw a response: a
    replay within 24 hours returns the original response, status code
    included, without dispatching a second courier or debiting a second
    time. The same key with a different body is a `409`, and so is a
    repeat sent while the original request is still being processed
    (`idempotency_conflict` both times). That repeat created nothing and
    does not mean the original failed: once the original has answered,
    the same request with the same key replays its answer.

    `dropoff.phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `external_id` is your own order reference. It is unique per key world,
    echoed in every payload and webhook, and filterable on the list, so you
    can reconcile without ever storing our ids.

    `pickup_ready_at` schedules the pickup for a future moment, between 10
    minutes and 29 days out. Absent, the order dispatches now.

    How the customer pays is `payment_method`. `cash` has the courier
    collect at the door, up to a cap. `card` mints a branded payment link
    in `payment.url`, which Listo sends your customer itself by WhatsApp
    (and by SMS when the WhatsApp does not reach them), so you do not need
    to send it; the order holds at `awaiting_payment` until the customer
    pays. `prepaid` means you have
    already been paid and the order dispatches immediately.

    On a `prepaid` create that binds no quote, `business_fee_share` is
    forced to 100 and `business_fee_cap_cents` is ignored, whatever you
    send: you have already collected from your customer, so the whole fee
    is yours. A create that binds a quote is held to the split the quote
    was priced with, so request the quote with `payment_method: prepaid`
    or with no `payment_method`: either is always priced at share 100 and
    binds a `prepaid` create. Any other quote is refused with `422
    validation_failed`, and the first thing that does not match is the one
    named. A quote requested with another `payment_method` (`cash` or
    `card`) is refused naming `payment_method`. A quote whose split is not
    the one a `prepaid` order has (share 100, no ceiling) is refused naming
    `business_fee_share` or `business_fee_cap_cents`, and `error.message`
    says why and what to send instead: a new quote requested with
    `payment_method: prepaid`.

    `vehicle` is `moto` (the default) or `car`, and `manifest.items[].size`
    is `small` (the default), `medium`, `large` or `xlarge`. A trip goes by
    car when you ask for one or when any item is sized `xlarge`, and for no
    other reason. A car is a sedan, never a van, can take longer to assign,
    and adds a surcharge inside `fee_cents`. The delivery's `vehicle` says
    what the trip was priced and dispatched as; `courier.vehicle_type` is
    what actually arrived, which can be a car on a `moto` trip without the
    fee changing.

    A create that binds a quote is held to the vehicle the quote was priced
    as. Leave `vehicle` out and it inherits the quote's. Say `moto` against
    a car quote, `car` against a moto quote, or send an item sized `xlarge`
    against a moto quote, and it is refused with `422 validation_failed`
    naming `vehicle` (or `manifest.items` when the sizes are what
    disagree). Re-quote with the cart you mean to send.

    `simulate` rehearses what goes wrong, and it works on a test key only.
    A live key that sends it is refused with `422 validation_failed`
    naming `simulate`, and so is a value that is not one of the four
    below. Leave it out and the delivery plays the normal happy path.

    - `returned`: the courier reaches the door, cannot hand the order
      over and brings it back. The delivery goes to `returning` and ends
      at `returned` with `failure_reason: customer_unavailable`, and the
      return is billed as a live one is: one `return_fee` entry in
      `charges` covers both legs (see `charges`).
    - `no_courier`: the create answers the same `409
      no_couriers_available` a live create answers when every courier is
      busy, and nothing is created, charged or recorded under your
      `Idempotency-Key`. There is no delivery to retry; repeat the call.
    - `delayed_pickup`: the courier is late. Pickup happens about 25
      minutes after the create and the drop-off about 5 minutes after
      that, counted from `pickup_ready_at` instead when you sent one (the
      delivery waits in `scheduled` until then). It goes through the
      same statuses as the normal run.
    - `courier_reassigned`: the first courier leaves before picking the
      order up and another courier takes the trip, which then completes
      normally. You see the courier on the delivery change while its
      status stays `picking_up`, and the delivery ends `delivered`. It
      plays once the delivery is dispatched and before a courier reaches
      the restaurant, so it may not play if the network assigns a courier
      first.

    In test mode a delivery may go from `dispatching` straight to
    `picking_up` without ever showing a `courier_assigned` status, in
    every scenario. Do not wait for it: `courier_assigned_at` and the
    courier object are filled in.

    There is no scenario that ends a delivery because a courier cancelled:
    a courier who gives up before pickup is a handover, which is what
    `courier_reassigned` plays. The
    same `Idempotency-Key` with a different `simulate` is a `409
    idempotency_conflict`, like any other changed body, once a request has
    used the key (it created a delivery, or it is still being processed).
    A request refused before it created anything, such as the `no_courier`
    409, leaves the key free: send it again with a different `simulate`,
    or none, and it is a new request. A `returned` delivery cannot be
    retried (`409 not_retriable`): its order ended.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, and nothing is dispatched or
    debited. Split it across two deliveries.

    Listo delivers in Mexico. A store that turns out to be somewhere else is
    refused with `422 unsupported_country` and nothing is dispatched or
    debited; it is final rather than retryable, and the same store will be
    refused every time.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, and nothing is dispatched or debited:
    until it is confirmed a courier could be sent to the wrong place.
    Usually the store's address has just changed and the confirmation has
    not landed yet, but not always, so do not read it as "the merchant
    moved". Unlike the refusal above it this one IS retryable, because
    nothing about your request is wrong and the identical call succeeds once
    the pickup point is confirmed.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. There is no `Retry-After` on it for that reason:
    we would be inventing the number. The restaurant can also unblock it
    themselves from their own Listo console, which is usually the faster of
    the two.

    When every courier near the trip is busy as the create prices it, the
    create is refused with `409 no_couriers_available`, and nothing is
    dispatched or debited. It is retryable: repeat the identical request,
    with the same `Idempotency-Key`, after a few minutes, for a bounded
    number of attempts. Nothing was recorded under that key, so the repeat
    creates the order once a courier is free rather than replaying the
    refusal.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, and nothing is dispatched or debited. It is a different
    refusal from `402 insufficient_balance`, which is about your balance:
    read `error.code`, never the status alone. `error.message` names the
    reason (no active plan, a charge that is pending, a plan that ended on a
    given date, a plan whose included deliveries for the cycle are all used,
    or a store that cannot request couriers right now), and it
    is not `retryable`. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A card create (`payment_method: card`) at a store of an account on
    self-serve pricing whose `card_payments` add-on is off is refused with
    `402 add_on_required`, `error.param` `payment_method`, and nothing is
    created or debited. It is not `retryable`: the identical request fails
    until `PATCH /v1/stores/{id}` switches the add-on on, and then the same
    `Idempotency-Key` creates the order. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    A `prepaid` or `card` order whose `order_value_cents` is above the
    store's limit for that payment type is refused with `422
    order_value_over_cap`, with `error.param` `order_value_cents`, and
    nothing is created or debited. The delivery fee does not count toward
    the limit, and a value equal to it is accepted. The limits are on the
    store, in `order_value_limits`. A quote you bind is checked again, so a
    quote priced under a higher limit can be refused here once that limit
    has ended. It is not `retryable`: send a smaller order, or contact Listo
    to raise the store's limit. A `cash` order has its own limit and is
    refused with `cash_over_cap`.

    A dropoff beyond the store's 15 km service area is refused with `422
    out_of_service_area`, which is final. The courier network can also
    refuse the distance of a dropoff at the very edge of that circle, and
    the answer is the same `422`, whether it refuses on the price or on the
    create itself. On the create it comes after the delivery was recorded,
    so the delivery stays, ended at `no_courier` with `failure_reason:
    delivery_failed` under your `external_id`, its fee debit returned in
    full and nothing else charged; replaying the request answers the same
    `422`. Send that order to another address under a new `external_id`.

    A dropoff the courier network does not serve at all, whatever its
    distance from the store, is refused with the same final `422
    out_of_service_area` whenever the create prices the trip. That includes
    a create that binds a quote but has to price it again (a cash order,
    or a quote whose courier price can no longer be booked as it stands).
    Only a create that books the bound quote's courier price as it stands
    meets that refusal at dispatch, after the delivery was recorded, and
    it answers `201` with the delivery ended at `no_courier`.

    Args:
        idempotency_key (str):
        body (CreateDeliveryRequest): The order to dispatch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateDeliveryRequest,
    idempotency_key: str,
) -> Response[Delivery | ErrorResponse]:
    """Create a delivery

     Dispatches a delivery.

    `Idempotency-Key` is required. Send a value you generate per order, and
    retry the same call with the same key if you never saw a response: a
    replay within 24 hours returns the original response, status code
    included, without dispatching a second courier or debiting a second
    time. The same key with a different body is a `409`, and so is a
    repeat sent while the original request is still being processed
    (`idempotency_conflict` both times). That repeat created nothing and
    does not mean the original failed: once the original has answered,
    the same request with the same key replays its answer.

    `dropoff.phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `external_id` is your own order reference. It is unique per key world,
    echoed in every payload and webhook, and filterable on the list, so you
    can reconcile without ever storing our ids.

    `pickup_ready_at` schedules the pickup for a future moment, between 10
    minutes and 29 days out. Absent, the order dispatches now.

    How the customer pays is `payment_method`. `cash` has the courier
    collect at the door, up to a cap. `card` mints a branded payment link
    in `payment.url`, which Listo sends your customer itself by WhatsApp
    (and by SMS when the WhatsApp does not reach them), so you do not need
    to send it; the order holds at `awaiting_payment` until the customer
    pays. `prepaid` means you have
    already been paid and the order dispatches immediately.

    On a `prepaid` create that binds no quote, `business_fee_share` is
    forced to 100 and `business_fee_cap_cents` is ignored, whatever you
    send: you have already collected from your customer, so the whole fee
    is yours. A create that binds a quote is held to the split the quote
    was priced with, so request the quote with `payment_method: prepaid`
    or with no `payment_method`: either is always priced at share 100 and
    binds a `prepaid` create. Any other quote is refused with `422
    validation_failed`, and the first thing that does not match is the one
    named. A quote requested with another `payment_method` (`cash` or
    `card`) is refused naming `payment_method`. A quote whose split is not
    the one a `prepaid` order has (share 100, no ceiling) is refused naming
    `business_fee_share` or `business_fee_cap_cents`, and `error.message`
    says why and what to send instead: a new quote requested with
    `payment_method: prepaid`.

    `vehicle` is `moto` (the default) or `car`, and `manifest.items[].size`
    is `small` (the default), `medium`, `large` or `xlarge`. A trip goes by
    car when you ask for one or when any item is sized `xlarge`, and for no
    other reason. A car is a sedan, never a van, can take longer to assign,
    and adds a surcharge inside `fee_cents`. The delivery's `vehicle` says
    what the trip was priced and dispatched as; `courier.vehicle_type` is
    what actually arrived, which can be a car on a `moto` trip without the
    fee changing.

    A create that binds a quote is held to the vehicle the quote was priced
    as. Leave `vehicle` out and it inherits the quote's. Say `moto` against
    a car quote, `car` against a moto quote, or send an item sized `xlarge`
    against a moto quote, and it is refused with `422 validation_failed`
    naming `vehicle` (or `manifest.items` when the sizes are what
    disagree). Re-quote with the cart you mean to send.

    `simulate` rehearses what goes wrong, and it works on a test key only.
    A live key that sends it is refused with `422 validation_failed`
    naming `simulate`, and so is a value that is not one of the four
    below. Leave it out and the delivery plays the normal happy path.

    - `returned`: the courier reaches the door, cannot hand the order
      over and brings it back. The delivery goes to `returning` and ends
      at `returned` with `failure_reason: customer_unavailable`, and the
      return is billed as a live one is: one `return_fee` entry in
      `charges` covers both legs (see `charges`).
    - `no_courier`: the create answers the same `409
      no_couriers_available` a live create answers when every courier is
      busy, and nothing is created, charged or recorded under your
      `Idempotency-Key`. There is no delivery to retry; repeat the call.
    - `delayed_pickup`: the courier is late. Pickup happens about 25
      minutes after the create and the drop-off about 5 minutes after
      that, counted from `pickup_ready_at` instead when you sent one (the
      delivery waits in `scheduled` until then). It goes through the
      same statuses as the normal run.
    - `courier_reassigned`: the first courier leaves before picking the
      order up and another courier takes the trip, which then completes
      normally. You see the courier on the delivery change while its
      status stays `picking_up`, and the delivery ends `delivered`. It
      plays once the delivery is dispatched and before a courier reaches
      the restaurant, so it may not play if the network assigns a courier
      first.

    In test mode a delivery may go from `dispatching` straight to
    `picking_up` without ever showing a `courier_assigned` status, in
    every scenario. Do not wait for it: `courier_assigned_at` and the
    courier object are filled in.

    There is no scenario that ends a delivery because a courier cancelled:
    a courier who gives up before pickup is a handover, which is what
    `courier_reassigned` plays. The
    same `Idempotency-Key` with a different `simulate` is a `409
    idempotency_conflict`, like any other changed body, once a request has
    used the key (it created a delivery, or it is still being processed).
    A request refused before it created anything, such as the `no_courier`
    409, leaves the key free: send it again with a different `simulate`,
    or none, and it is a new request. A `returned` delivery cannot be
    retried (`409 not_retriable`): its order ended.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, and nothing is dispatched or
    debited. Split it across two deliveries.

    Listo delivers in Mexico. A store that turns out to be somewhere else is
    refused with `422 unsupported_country` and nothing is dispatched or
    debited; it is final rather than retryable, and the same store will be
    refused every time.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, and nothing is dispatched or debited:
    until it is confirmed a courier could be sent to the wrong place.
    Usually the store's address has just changed and the confirmation has
    not landed yet, but not always, so do not read it as "the merchant
    moved". Unlike the refusal above it this one IS retryable, because
    nothing about your request is wrong and the identical call succeeds once
    the pickup point is confirmed.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. There is no `Retry-After` on it for that reason:
    we would be inventing the number. The restaurant can also unblock it
    themselves from their own Listo console, which is usually the faster of
    the two.

    When every courier near the trip is busy as the create prices it, the
    create is refused with `409 no_couriers_available`, and nothing is
    dispatched or debited. It is retryable: repeat the identical request,
    with the same `Idempotency-Key`, after a few minutes, for a bounded
    number of attempts. Nothing was recorded under that key, so the repeat
    creates the order once a courier is free rather than replaying the
    refusal.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, and nothing is dispatched or debited. It is a different
    refusal from `402 insufficient_balance`, which is about your balance:
    read `error.code`, never the status alone. `error.message` names the
    reason (no active plan, a charge that is pending, a plan that ended on a
    given date, a plan whose included deliveries for the cycle are all used,
    or a store that cannot request couriers right now), and it
    is not `retryable`. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A card create (`payment_method: card`) at a store of an account on
    self-serve pricing whose `card_payments` add-on is off is refused with
    `402 add_on_required`, `error.param` `payment_method`, and nothing is
    created or debited. It is not `retryable`: the identical request fails
    until `PATCH /v1/stores/{id}` switches the add-on on, and then the same
    `Idempotency-Key` creates the order. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    A `prepaid` or `card` order whose `order_value_cents` is above the
    store's limit for that payment type is refused with `422
    order_value_over_cap`, with `error.param` `order_value_cents`, and
    nothing is created or debited. The delivery fee does not count toward
    the limit, and a value equal to it is accepted. The limits are on the
    store, in `order_value_limits`. A quote you bind is checked again, so a
    quote priced under a higher limit can be refused here once that limit
    has ended. It is not `retryable`: send a smaller order, or contact Listo
    to raise the store's limit. A `cash` order has its own limit and is
    refused with `cash_over_cap`.

    A dropoff beyond the store's 15 km service area is refused with `422
    out_of_service_area`, which is final. The courier network can also
    refuse the distance of a dropoff at the very edge of that circle, and
    the answer is the same `422`, whether it refuses on the price or on the
    create itself. On the create it comes after the delivery was recorded,
    so the delivery stays, ended at `no_courier` with `failure_reason:
    delivery_failed` under your `external_id`, its fee debit returned in
    full and nothing else charged; replaying the request answers the same
    `422`. Send that order to another address under a new `external_id`.

    A dropoff the courier network does not serve at all, whatever its
    distance from the store, is refused with the same final `422
    out_of_service_area` whenever the create prices the trip. That includes
    a create that binds a quote but has to price it again (a cash order,
    or a quote whose courier price can no longer be booked as it stands).
    Only a create that books the bound quote's courier price as it stands
    meets that refusal at dispatch, after the delivery was recorded, and
    it answers `201` with the delivery ended at `no_courier`.

    Args:
        idempotency_key (str):
        body (CreateDeliveryRequest): The order to dispatch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Delivery | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateDeliveryRequest,
    idempotency_key: str,
) -> Delivery | ErrorResponse | None:
    """Create a delivery

     Dispatches a delivery.

    `Idempotency-Key` is required. Send a value you generate per order, and
    retry the same call with the same key if you never saw a response: a
    replay within 24 hours returns the original response, status code
    included, without dispatching a second courier or debiting a second
    time. The same key with a different body is a `409`, and so is a
    repeat sent while the original request is still being processed
    (`idempotency_conflict` both times). That repeat created nothing and
    does not mean the original failed: once the original has answered,
    the same request with the same key replays its answer.

    `dropoff.phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `external_id` is your own order reference. It is unique per key world,
    echoed in every payload and webhook, and filterable on the list, so you
    can reconcile without ever storing our ids.

    `pickup_ready_at` schedules the pickup for a future moment, between 10
    minutes and 29 days out. Absent, the order dispatches now.

    How the customer pays is `payment_method`. `cash` has the courier
    collect at the door, up to a cap. `card` mints a branded payment link
    in `payment.url`, which Listo sends your customer itself by WhatsApp
    (and by SMS when the WhatsApp does not reach them), so you do not need
    to send it; the order holds at `awaiting_payment` until the customer
    pays. `prepaid` means you have
    already been paid and the order dispatches immediately.

    On a `prepaid` create that binds no quote, `business_fee_share` is
    forced to 100 and `business_fee_cap_cents` is ignored, whatever you
    send: you have already collected from your customer, so the whole fee
    is yours. A create that binds a quote is held to the split the quote
    was priced with, so request the quote with `payment_method: prepaid`
    or with no `payment_method`: either is always priced at share 100 and
    binds a `prepaid` create. Any other quote is refused with `422
    validation_failed`, and the first thing that does not match is the one
    named. A quote requested with another `payment_method` (`cash` or
    `card`) is refused naming `payment_method`. A quote whose split is not
    the one a `prepaid` order has (share 100, no ceiling) is refused naming
    `business_fee_share` or `business_fee_cap_cents`, and `error.message`
    says why and what to send instead: a new quote requested with
    `payment_method: prepaid`.

    `vehicle` is `moto` (the default) or `car`, and `manifest.items[].size`
    is `small` (the default), `medium`, `large` or `xlarge`. A trip goes by
    car when you ask for one or when any item is sized `xlarge`, and for no
    other reason. A car is a sedan, never a van, can take longer to assign,
    and adds a surcharge inside `fee_cents`. The delivery's `vehicle` says
    what the trip was priced and dispatched as; `courier.vehicle_type` is
    what actually arrived, which can be a car on a `moto` trip without the
    fee changing.

    A create that binds a quote is held to the vehicle the quote was priced
    as. Leave `vehicle` out and it inherits the quote's. Say `moto` against
    a car quote, `car` against a moto quote, or send an item sized `xlarge`
    against a moto quote, and it is refused with `422 validation_failed`
    naming `vehicle` (or `manifest.items` when the sizes are what
    disagree). Re-quote with the cart you mean to send.

    `simulate` rehearses what goes wrong, and it works on a test key only.
    A live key that sends it is refused with `422 validation_failed`
    naming `simulate`, and so is a value that is not one of the four
    below. Leave it out and the delivery plays the normal happy path.

    - `returned`: the courier reaches the door, cannot hand the order
      over and brings it back. The delivery goes to `returning` and ends
      at `returned` with `failure_reason: customer_unavailable`, and the
      return is billed as a live one is: one `return_fee` entry in
      `charges` covers both legs (see `charges`).
    - `no_courier`: the create answers the same `409
      no_couriers_available` a live create answers when every courier is
      busy, and nothing is created, charged or recorded under your
      `Idempotency-Key`. There is no delivery to retry; repeat the call.
    - `delayed_pickup`: the courier is late. Pickup happens about 25
      minutes after the create and the drop-off about 5 minutes after
      that, counted from `pickup_ready_at` instead when you sent one (the
      delivery waits in `scheduled` until then). It goes through the
      same statuses as the normal run.
    - `courier_reassigned`: the first courier leaves before picking the
      order up and another courier takes the trip, which then completes
      normally. You see the courier on the delivery change while its
      status stays `picking_up`, and the delivery ends `delivered`. It
      plays once the delivery is dispatched and before a courier reaches
      the restaurant, so it may not play if the network assigns a courier
      first.

    In test mode a delivery may go from `dispatching` straight to
    `picking_up` without ever showing a `courier_assigned` status, in
    every scenario. Do not wait for it: `courier_assigned_at` and the
    courier object are filled in.

    There is no scenario that ends a delivery because a courier cancelled:
    a courier who gives up before pickup is a handover, which is what
    `courier_reassigned` plays. The
    same `Idempotency-Key` with a different `simulate` is a `409
    idempotency_conflict`, like any other changed body, once a request has
    used the key (it created a delivery, or it is still being processed).
    A request refused before it created anything, such as the `no_courier`
    409, leaves the key free: send it again with a different `simulate`,
    or none, and it is a new request. A `returned` delivery cannot be
    retried (`409 not_retriable`): its order ended.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, and nothing is dispatched or
    debited. Split it across two deliveries.

    Listo delivers in Mexico. A store that turns out to be somewhere else is
    refused with `422 unsupported_country` and nothing is dispatched or
    debited; it is final rather than retryable, and the same store will be
    refused every time.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, and nothing is dispatched or debited:
    until it is confirmed a courier could be sent to the wrong place.
    Usually the store's address has just changed and the confirmation has
    not landed yet, but not always, so do not read it as "the merchant
    moved". Unlike the refusal above it this one IS retryable, because
    nothing about your request is wrong and the identical call succeeds once
    the pickup point is confirmed.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. There is no `Retry-After` on it for that reason:
    we would be inventing the number. The restaurant can also unblock it
    themselves from their own Listo console, which is usually the faster of
    the two.

    When every courier near the trip is busy as the create prices it, the
    create is refused with `409 no_couriers_available`, and nothing is
    dispatched or debited. It is retryable: repeat the identical request,
    with the same `Idempotency-Key`, after a few minutes, for a bounded
    number of attempts. Nothing was recorded under that key, so the repeat
    creates the order once a courier is free rather than replaying the
    refusal.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, and nothing is dispatched or debited. It is a different
    refusal from `402 insufficient_balance`, which is about your balance:
    read `error.code`, never the status alone. `error.message` names the
    reason (no active plan, a charge that is pending, a plan that ended on a
    given date, a plan whose included deliveries for the cycle are all used,
    or a store that cannot request couriers right now), and it
    is not `retryable`. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A card create (`payment_method: card`) at a store of an account on
    self-serve pricing whose `card_payments` add-on is off is refused with
    `402 add_on_required`, `error.param` `payment_method`, and nothing is
    created or debited. It is not `retryable`: the identical request fails
    until `PATCH /v1/stores/{id}` switches the add-on on, and then the same
    `Idempotency-Key` creates the order. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    A `prepaid` or `card` order whose `order_value_cents` is above the
    store's limit for that payment type is refused with `422
    order_value_over_cap`, with `error.param` `order_value_cents`, and
    nothing is created or debited. The delivery fee does not count toward
    the limit, and a value equal to it is accepted. The limits are on the
    store, in `order_value_limits`. A quote you bind is checked again, so a
    quote priced under a higher limit can be refused here once that limit
    has ended. It is not `retryable`: send a smaller order, or contact Listo
    to raise the store's limit. A `cash` order has its own limit and is
    refused with `cash_over_cap`.

    A dropoff beyond the store's 15 km service area is refused with `422
    out_of_service_area`, which is final. The courier network can also
    refuse the distance of a dropoff at the very edge of that circle, and
    the answer is the same `422`, whether it refuses on the price or on the
    create itself. On the create it comes after the delivery was recorded,
    so the delivery stays, ended at `no_courier` with `failure_reason:
    delivery_failed` under your `external_id`, its fee debit returned in
    full and nothing else charged; replaying the request answers the same
    `422`. Send that order to another address under a new `external_id`.

    A dropoff the courier network does not serve at all, whatever its
    distance from the store, is refused with the same final `422
    out_of_service_area` whenever the create prices the trip. That includes
    a create that binds a quote but has to price it again (a cash order,
    or a quote whose courier price can no longer be booked as it stands).
    Only a create that books the bound quote's courier price as it stands
    meets that refusal at dispatch, after the delivery was recorded, and
    it answers `201` with the delivery ended at `no_courier`.

    Args:
        idempotency_key (str):
        body (CreateDeliveryRequest): The order to dispatch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Delivery | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
