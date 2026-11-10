from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_quote_request import CreateQuoteRequest
from ...models.error_response import ErrorResponse
from ...models.quote import Quote
from ...types import Response


def _get_kwargs(
    *,
    body: CreateQuoteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/quotes",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Quote | None:
    if response.status_code == 201:
        response_201 = Quote.from_dict(response.json())

        return response_201

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
) -> Response[ErrorResponse | Quote]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateQuoteRequest,
) -> Response[ErrorResponse | Quote]:
    """Price a delivery

     Prices a trip and holds that price for you to bind. The price is set at
    the moment you ask for the quote: bind its `id` on the delivery create
    and the order is charged the `fee_cents` and the split you were shown.

    The courier network books the trip when the delivery is created, and
    what it books can differ slightly from the price quoted. We book the
    very quote you were shown whenever it is still valid, so this is rare.
    When it happens, the difference appears on your ledger as its own line
    (`requote_adjustment`, see `GET /v1/ledger`), negative when the booked
    trip cost more and positive when it cost less. It never changes the
    `fee_cents`, the split or the total of the order your customer sees.

    Quotes expire, and `expires_at` tells you when. Binding an expired or
    already-spent quote is a `400`; request a new one. Binding is optional,
    and a create without one is priced inline at whatever the price is then.

    `cash_to_collect_cents` is what the courier collects at the door on a
    cash order: the goods value plus the customer's share of the fee.

    `business_fee_share` and `business_fee_cap_cents` say how the delivery
    fee is split between you and your customer. A `prepaid` quote is
    different: you have already collected from your customer, so the whole
    fee is yours and the split is fixed at 100 with no ceiling. A quote
    that names no `payment_method` is priced the same way, because the only
    delivery that can bind it is a `prepaid` one. On either, a
    `business_fee_share` other than 100 is refused with `422
    validation_failed` naming `business_fee_share`, a valid
    `business_fee_cap_cents` is ignored (one that is not a number is refused
    as a shape error first), and a quote that sends neither is priced at
    100, whatever your store's default split is. That is the split a
    `prepaid` delivery create books, so a quote you want to bind to a
    `prepaid` delivery either names `payment_method: prepaid` or names no
    method. To split the fee with your customer, name `cash` or `card`.

    `vehicle` is `moto` (the default) or `car`. A car is a sedan: we can
    guarantee a car, never a van, and there are fewer cars than motorcycles,
    so one can take longer to assign. A car adds a surcharge that is INSIDE
    `fee_cents` and split like the rest of the fee, so the number you are
    quoted is the whole price; there is no separate line for it.

    `manifest.items` is optional and takes the same `{name, quantity,
    size}` items the delivery create does. `size` is one of `small` (the
    default), `medium`, `large` or `xlarge`, and it is the one field on an
    item that can change the price: an item sized `xlarge` makes the trip
    a car even when `vehicle` says `moto`. Nothing else does, weight
    included. The response's `vehicle` says which trip the fee is for,
    whatever made it one. Send the quote the same cart you will create
    with: the create is held to the vehicle this quote was priced as.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, before anything is priced.
    Split it across two deliveries.

    Listo prices in Mexican pesos and delivers in Mexico. A store that turns
    out to be somewhere else is refused here with `422
    unsupported_country`, which is final: it is not the retryable
    `provider_unavailable`, and no retry of the same store can succeed. You
    will only meet it on a store you positioned yourself, with `lat`/`lng`,
    since a store we located is refused when you create it.

    A dropoff beyond the store's 15 km service area, or one the courier
    network does not serve at all, whatever its distance from the store, is
    refused with `422 out_of_service_area`, which is final: send the order
    to another address.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, because until it is confirmed a courier
    could be sent to the wrong place. Usually the store's address has just
    changed and the confirmation has not landed yet, but not always, so do
    not read it as "the merchant moved". This one IS retryable: nothing
    about your request is wrong, and the identical call succeeds once the
    pickup point is confirmed. It refuses the store rather than the trip, so
    a different dropoff will not help.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. The restaurant can also unblock it themselves
    from their own Listo console, which is usually the faster of the two.

    When every courier near the trip is busy, the quote is refused with
    `409 no_couriers_available` and nothing is priced. It is not an outage
    and nothing about your request is wrong: it IS retryable, and the
    identical call is priced once a courier is free, usually within
    minutes. Retry it after a few minutes, for a bounded number of
    attempts, and then tell whoever is waiting for the order rather than
    keep polling. It is the same word a delivery that ended without a
    courier carries in `failure_reason`.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, because the create would refuse the delivery this
    quote prices. `error.message` names the reason: no active plan, a
    charge that is pending, a plan that ended on a given date, a plan whose
    included deliveries for the cycle are all used, or a store that cannot
    request couriers right now. It is not `retryable`: the identical call
    fails until the plan is paid or restarted, or the cycle renews. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A `prepaid` or `card` order, or a quote with no `payment_method` (which
    is judged as `prepaid`, because only a prepaid delivery can book it),
    whose `order_value_cents` is above the store's limit for that payment
    type is refused with `422 order_value_over_cap`, with `error.param`
    `order_value_cents`, and nothing is created. The delivery fee does not
    count toward the limit, and a value equal to it is accepted. The limits
    are on the store, in `order_value_limits`. It is not `retryable`: send a
    smaller order, or contact Listo to raise the store's limit. A `cash`
    quote has its own limit and is refused with `cash_over_cap`.

    Args:
        body (CreateQuoteRequest): The trip to price.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Quote]
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
    body: CreateQuoteRequest,
) -> ErrorResponse | Quote | None:
    """Price a delivery

     Prices a trip and holds that price for you to bind. The price is set at
    the moment you ask for the quote: bind its `id` on the delivery create
    and the order is charged the `fee_cents` and the split you were shown.

    The courier network books the trip when the delivery is created, and
    what it books can differ slightly from the price quoted. We book the
    very quote you were shown whenever it is still valid, so this is rare.
    When it happens, the difference appears on your ledger as its own line
    (`requote_adjustment`, see `GET /v1/ledger`), negative when the booked
    trip cost more and positive when it cost less. It never changes the
    `fee_cents`, the split or the total of the order your customer sees.

    Quotes expire, and `expires_at` tells you when. Binding an expired or
    already-spent quote is a `400`; request a new one. Binding is optional,
    and a create without one is priced inline at whatever the price is then.

    `cash_to_collect_cents` is what the courier collects at the door on a
    cash order: the goods value plus the customer's share of the fee.

    `business_fee_share` and `business_fee_cap_cents` say how the delivery
    fee is split between you and your customer. A `prepaid` quote is
    different: you have already collected from your customer, so the whole
    fee is yours and the split is fixed at 100 with no ceiling. A quote
    that names no `payment_method` is priced the same way, because the only
    delivery that can bind it is a `prepaid` one. On either, a
    `business_fee_share` other than 100 is refused with `422
    validation_failed` naming `business_fee_share`, a valid
    `business_fee_cap_cents` is ignored (one that is not a number is refused
    as a shape error first), and a quote that sends neither is priced at
    100, whatever your store's default split is. That is the split a
    `prepaid` delivery create books, so a quote you want to bind to a
    `prepaid` delivery either names `payment_method: prepaid` or names no
    method. To split the fee with your customer, name `cash` or `card`.

    `vehicle` is `moto` (the default) or `car`. A car is a sedan: we can
    guarantee a car, never a van, and there are fewer cars than motorcycles,
    so one can take longer to assign. A car adds a surcharge that is INSIDE
    `fee_cents` and split like the rest of the fee, so the number you are
    quoted is the whole price; there is no separate line for it.

    `manifest.items` is optional and takes the same `{name, quantity,
    size}` items the delivery create does. `size` is one of `small` (the
    default), `medium`, `large` or `xlarge`, and it is the one field on an
    item that can change the price: an item sized `xlarge` makes the trip
    a car even when `vehicle` says `moto`. Nothing else does, weight
    included. The response's `vehicle` says which trip the fee is for,
    whatever made it one. Send the quote the same cart you will create
    with: the create is held to the vehicle this quote was priced as.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, before anything is priced.
    Split it across two deliveries.

    Listo prices in Mexican pesos and delivers in Mexico. A store that turns
    out to be somewhere else is refused here with `422
    unsupported_country`, which is final: it is not the retryable
    `provider_unavailable`, and no retry of the same store can succeed. You
    will only meet it on a store you positioned yourself, with `lat`/`lng`,
    since a store we located is refused when you create it.

    A dropoff beyond the store's 15 km service area, or one the courier
    network does not serve at all, whatever its distance from the store, is
    refused with `422 out_of_service_area`, which is final: send the order
    to another address.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, because until it is confirmed a courier
    could be sent to the wrong place. Usually the store's address has just
    changed and the confirmation has not landed yet, but not always, so do
    not read it as "the merchant moved". This one IS retryable: nothing
    about your request is wrong, and the identical call succeeds once the
    pickup point is confirmed. It refuses the store rather than the trip, so
    a different dropoff will not help.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. The restaurant can also unblock it themselves
    from their own Listo console, which is usually the faster of the two.

    When every courier near the trip is busy, the quote is refused with
    `409 no_couriers_available` and nothing is priced. It is not an outage
    and nothing about your request is wrong: it IS retryable, and the
    identical call is priced once a courier is free, usually within
    minutes. Retry it after a few minutes, for a bounded number of
    attempts, and then tell whoever is waiting for the order rather than
    keep polling. It is the same word a delivery that ended without a
    courier carries in `failure_reason`.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, because the create would refuse the delivery this
    quote prices. `error.message` names the reason: no active plan, a
    charge that is pending, a plan that ended on a given date, a plan whose
    included deliveries for the cycle are all used, or a store that cannot
    request couriers right now. It is not `retryable`: the identical call
    fails until the plan is paid or restarted, or the cycle renews. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A `prepaid` or `card` order, or a quote with no `payment_method` (which
    is judged as `prepaid`, because only a prepaid delivery can book it),
    whose `order_value_cents` is above the store's limit for that payment
    type is refused with `422 order_value_over_cap`, with `error.param`
    `order_value_cents`, and nothing is created. The delivery fee does not
    count toward the limit, and a value equal to it is accepted. The limits
    are on the store, in `order_value_limits`. It is not `retryable`: send a
    smaller order, or contact Listo to raise the store's limit. A `cash`
    quote has its own limit and is refused with `cash_over_cap`.

    Args:
        body (CreateQuoteRequest): The trip to price.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Quote
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateQuoteRequest,
) -> Response[ErrorResponse | Quote]:
    """Price a delivery

     Prices a trip and holds that price for you to bind. The price is set at
    the moment you ask for the quote: bind its `id` on the delivery create
    and the order is charged the `fee_cents` and the split you were shown.

    The courier network books the trip when the delivery is created, and
    what it books can differ slightly from the price quoted. We book the
    very quote you were shown whenever it is still valid, so this is rare.
    When it happens, the difference appears on your ledger as its own line
    (`requote_adjustment`, see `GET /v1/ledger`), negative when the booked
    trip cost more and positive when it cost less. It never changes the
    `fee_cents`, the split or the total of the order your customer sees.

    Quotes expire, and `expires_at` tells you when. Binding an expired or
    already-spent quote is a `400`; request a new one. Binding is optional,
    and a create without one is priced inline at whatever the price is then.

    `cash_to_collect_cents` is what the courier collects at the door on a
    cash order: the goods value plus the customer's share of the fee.

    `business_fee_share` and `business_fee_cap_cents` say how the delivery
    fee is split between you and your customer. A `prepaid` quote is
    different: you have already collected from your customer, so the whole
    fee is yours and the split is fixed at 100 with no ceiling. A quote
    that names no `payment_method` is priced the same way, because the only
    delivery that can bind it is a `prepaid` one. On either, a
    `business_fee_share` other than 100 is refused with `422
    validation_failed` naming `business_fee_share`, a valid
    `business_fee_cap_cents` is ignored (one that is not a number is refused
    as a shape error first), and a quote that sends neither is priced at
    100, whatever your store's default split is. That is the split a
    `prepaid` delivery create books, so a quote you want to bind to a
    `prepaid` delivery either names `payment_method: prepaid` or names no
    method. To split the fee with your customer, name `cash` or `card`.

    `vehicle` is `moto` (the default) or `car`. A car is a sedan: we can
    guarantee a car, never a van, and there are fewer cars than motorcycles,
    so one can take longer to assign. A car adds a surcharge that is INSIDE
    `fee_cents` and split like the rest of the fee, so the number you are
    quoted is the whole price; there is no separate line for it.

    `manifest.items` is optional and takes the same `{name, quantity,
    size}` items the delivery create does. `size` is one of `small` (the
    default), `medium`, `large` or `xlarge`, and it is the one field on an
    item that can change the price: an item sized `xlarge` makes the trip
    a car even when `vehicle` says `moto`. Nothing else does, weight
    included. The response's `vehicle` says which trip the fee is for,
    whatever made it one. Send the quote the same cart you will create
    with: the create is held to the vehicle this quote was priced as.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, before anything is priced.
    Split it across two deliveries.

    Listo prices in Mexican pesos and delivers in Mexico. A store that turns
    out to be somewhere else is refused here with `422
    unsupported_country`, which is final: it is not the retryable
    `provider_unavailable`, and no retry of the same store can succeed. You
    will only meet it on a store you positioned yourself, with `lat`/`lng`,
    since a store we located is refused when you create it.

    A dropoff beyond the store's 15 km service area, or one the courier
    network does not serve at all, whatever its distance from the store, is
    refused with `422 out_of_service_area`, which is final: send the order
    to another address.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, because until it is confirmed a courier
    could be sent to the wrong place. Usually the store's address has just
    changed and the confirmation has not landed yet, but not always, so do
    not read it as "the merchant moved". This one IS retryable: nothing
    about your request is wrong, and the identical call succeeds once the
    pickup point is confirmed. It refuses the store rather than the trip, so
    a different dropoff will not help.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. The restaurant can also unblock it themselves
    from their own Listo console, which is usually the faster of the two.

    When every courier near the trip is busy, the quote is refused with
    `409 no_couriers_available` and nothing is priced. It is not an outage
    and nothing about your request is wrong: it IS retryable, and the
    identical call is priced once a courier is free, usually within
    minutes. Retry it after a few minutes, for a bounded number of
    attempts, and then tell whoever is waiting for the order rather than
    keep polling. It is the same word a delivery that ended without a
    courier carries in `failure_reason`.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, because the create would refuse the delivery this
    quote prices. `error.message` names the reason: no active plan, a
    charge that is pending, a plan that ended on a given date, a plan whose
    included deliveries for the cycle are all used, or a store that cannot
    request couriers right now. It is not `retryable`: the identical call
    fails until the plan is paid or restarted, or the cycle renews. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A `prepaid` or `card` order, or a quote with no `payment_method` (which
    is judged as `prepaid`, because only a prepaid delivery can book it),
    whose `order_value_cents` is above the store's limit for that payment
    type is refused with `422 order_value_over_cap`, with `error.param`
    `order_value_cents`, and nothing is created. The delivery fee does not
    count toward the limit, and a value equal to it is accepted. The limits
    are on the store, in `order_value_limits`. It is not `retryable`: send a
    smaller order, or contact Listo to raise the store's limit. A `cash`
    quote has its own limit and is refused with `cash_over_cap`.

    Args:
        body (CreateQuoteRequest): The trip to price.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Quote]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateQuoteRequest,
) -> ErrorResponse | Quote | None:
    """Price a delivery

     Prices a trip and holds that price for you to bind. The price is set at
    the moment you ask for the quote: bind its `id` on the delivery create
    and the order is charged the `fee_cents` and the split you were shown.

    The courier network books the trip when the delivery is created, and
    what it books can differ slightly from the price quoted. We book the
    very quote you were shown whenever it is still valid, so this is rare.
    When it happens, the difference appears on your ledger as its own line
    (`requote_adjustment`, see `GET /v1/ledger`), negative when the booked
    trip cost more and positive when it cost less. It never changes the
    `fee_cents`, the split or the total of the order your customer sees.

    Quotes expire, and `expires_at` tells you when. Binding an expired or
    already-spent quote is a `400`; request a new one. Binding is optional,
    and a create without one is priced inline at whatever the price is then.

    `cash_to_collect_cents` is what the courier collects at the door on a
    cash order: the goods value plus the customer's share of the fee.

    `business_fee_share` and `business_fee_cap_cents` say how the delivery
    fee is split between you and your customer. A `prepaid` quote is
    different: you have already collected from your customer, so the whole
    fee is yours and the split is fixed at 100 with no ceiling. A quote
    that names no `payment_method` is priced the same way, because the only
    delivery that can bind it is a `prepaid` one. On either, a
    `business_fee_share` other than 100 is refused with `422
    validation_failed` naming `business_fee_share`, a valid
    `business_fee_cap_cents` is ignored (one that is not a number is refused
    as a shape error first), and a quote that sends neither is priced at
    100, whatever your store's default split is. That is the split a
    `prepaid` delivery create books, so a quote you want to bind to a
    `prepaid` delivery either names `payment_method: prepaid` or names no
    method. To split the fee with your customer, name `cash` or `card`.

    `vehicle` is `moto` (the default) or `car`. A car is a sedan: we can
    guarantee a car, never a van, and there are fewer cars than motorcycles,
    so one can take longer to assign. A car adds a surcharge that is INSIDE
    `fee_cents` and split like the rest of the fee, so the number you are
    quoted is the whole price; there is no separate line for it.

    `manifest.items` is optional and takes the same `{name, quantity,
    size}` items the delivery create does. `size` is one of `small` (the
    default), `medium`, `large` or `xlarge`, and it is the one field on an
    item that can change the price: an item sized `xlarge` makes the trip
    a car even when `vehicle` says `moto`. Nothing else does, weight
    included. The response's `vehicle` says which trip the fee is for,
    whatever made it one. Send the quote the same cart you will create
    with: the create is held to the vehicle this quote was priced as.

    A cart too large for one courier trip is refused with `422
    order_too_large`, naming `manifest.items`, before anything is priced.
    Split it across two deliveries.

    Listo prices in Mexican pesos and delivers in Mexico. A store that turns
    out to be somewhere else is refused here with `422
    unsupported_country`, which is final: it is not the retryable
    `provider_unavailable`, and no retry of the same store can succeed. You
    will only meet it on a store you positioned yourself, with `lat`/`lng`,
    since a store we located is refused when you create it.

    A dropoff beyond the store's 15 km service area, or one the courier
    network does not serve at all, whatever its distance from the store, is
    refused with `422 out_of_service_area`, which is final: send the order
    to another address.

    A store whose pickup point we cannot currently vouch for is refused
    with `409 pickup_point_pending`, because until it is confirmed a courier
    could be sent to the wrong place. Usually the store's address has just
    changed and the confirmation has not landed yet, but not always, so do
    not read it as "the merchant moved". This one IS retryable: nothing
    about your request is wrong, and the identical call succeeds once the
    pickup point is confirmed. It refuses the store rather than the trip, so
    a different dropoff will not help.

    Retry it on a minutes-scale backoff, for a bounded number of attempts,
    and then put it in front of a human rather than keep polling. Most moves
    land within minutes on their own; a few are held up by something only
    our staff can clear and take considerably longer, and this response does
    not tell the two apart. The restaurant can also unblock it themselves
    from their own Listo console, which is usually the faster of the two.

    When every courier near the trip is busy, the quote is refused with
    `409 no_couriers_available` and nothing is priced. It is not an outage
    and nothing about your request is wrong: it IS retryable, and the
    identical call is priced once a courier is free, usually within
    minutes. Retry it after a few minutes, for a bounded number of
    attempts, and then tell whoever is waiting for the order rather than
    keep polling. It is the same word a delivery that ended without a
    courier carries in `failure_reason`.

    A live store whose Plan Listo is not paid up is refused with `402
    plan_required`, because the create would refuse the delivery this
    quote prices. `error.message` names the reason: no active plan, a
    charge that is pending, a plan that ended on a given date, a plan whose
    included deliveries for the cycle are all used, or a store that cannot
    request couriers right now. It is not `retryable`: the identical call
    fails until the plan is paid or restarted, or the cycle renews. See
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing).

    A `prepaid` or `card` order, or a quote with no `payment_method` (which
    is judged as `prepaid`, because only a prepaid delivery can book it),
    whose `order_value_cents` is above the store's limit for that payment
    type is refused with `422 order_value_over_cap`, with `error.param`
    `order_value_cents`, and nothing is created. The delivery fee does not
    count toward the limit, and a value equal to it is accepted. The limits
    are on the store, in `order_value_limits`. It is not `retryable`: send a
    smaller order, or contact Listo to raise the store's limit. A `cash`
    quote has its own limit and is refused with `cash_over_cap`.

    Args:
        body (CreateQuoteRequest): The trip to price.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Quote
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
