from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_store_request import CreateStoreRequest
from ...models.error_response import ErrorResponse
from ...models.store import Store
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreateStoreRequest,
    idempotency_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/stores",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Store | None:
    if response.status_code == 201:
        response_201 = Store.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

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
    *,
    client: AuthenticatedClient,
    body: CreateStoreRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Store]:
    """Create a store

     Registers a pickup location. `lat`/`lng` are optional; send them when
    you have them and we take them as given, otherwise we geocode `street`.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `timezone` is derived from the store's position, and you do not have to
    send one. Mexico spans five zones, and the store's own position is what
    decides which one it keeps its hours in: its scheduled pickup windows,
    its delivery timestamps and its settlement week are all read in it.

    A `timezone` you do send is used only when the position cannot answer:
    a store with no coordinates, or a position no zone claims. One that
    disagrees with the position does not change the store and is not an
    error: the store is created, everything else you sent is applied, and
    the zone the position gives is what comes back.

    We would rather correct that quietly than refuse it, because we cannot
    tell the two cases apart from here: a zone sent by default out of a form
    that never asked its user arrives looking exactly like a zone somebody
    chose, and the first store provisioned against the old rule landed an
    hour ahead of itself for a year of opening hours, delivery timestamps
    and settlement weeks. Your store's position is evidence about where it
    is. If a store's clock looks wrong, its coordinates are what to fix.

    `default_business_fee_share` is the share of the delivery fee this store
    covers by default, 0 to 100, with the rest charged to the customer.
    Every `cash` or `card` delivery from the store inherits it unless the
    create overrides it. A `prepaid` delivery, and a quote that names no
    `payment_method`, always carry share 100 instead: the whole fee is yours.

    A store can also split the fee by a fixed peso amount instead of a
    percentage, which `default_fee_split_mode` on the store object tells you
    and `default_fee_split_amount_cents` carries. Both are read-only: the
    restaurant chooses the shape in its own Listo console, and there is no
    field here to set one. Read the mode before you read the share, because
    in an amount mode the share is not the split in force. Sending
    `default_business_fee_share` moves the store back to `percent`, on this
    endpoint and on the update.

    `owner_email` is optional, and it is a precondition rather than an
    attribute: send the address of whoever runs the location and we check it
    against the restaurants that already have a Listo account of their own.
    If one exists, nothing is created and you get `409 account_exists`,
    because a second account for a kitchen that already has one would split
    its balance, its console and its history in two. Ask its owner to
    connect the account they have instead, with `POST /v1/connect_requests`,
    as [Connect a restaurant that already uses Listo](https://docs.listo.delivery/en/guides/connect-
    existing-account)
    describes.

    Nothing stores the address and no store object echoes it. It does not
    create a login either; that is `POST /v1/stores/{id}/owner`.

    Listo delivers in Mexico, and a `street` that resolves to another
    country is refused with `422 unsupported_country`: nothing is created,
    and no other address in that country will work either. An address we
    cannot resolve at all is not refused. It is stored as you sent it and
    located on the first delivery.

    What a live create does about the store's Plan Listo depends on who
    pays it on your account (see
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing)).

    If you pay your stores' plans, the store starts its Plan Listo and its
    first month is charged to you in this same request, from your live
    balance or from the card saved on your account. Fund one of them first,
    and send an `Idempotency-Key` on every live create: a create that timed
    out and is repeated without one makes a second store, and the second
    store starts a second plan. A store whose first charge fails is still
    created and still answers `201`, with `plan.status` `awaiting_payment`:
    it has no plan yet, nothing is past due, and its deliveries are refused
    with `402 plan_required` until your balance or card covers the month,
    which Listo then charges by itself.

    If your account is set up so that each restaurant pays its own plan,
    nothing is charged to you: the store is created with no plan (`plan` is
    `null`) and the restaurant buys its own Plan Listo in its Listo console.
    Its deliveries are refused with `402 plan_required` until it does.

    If your account is on Listo's self-serve pricing, the store you create
    carries no Plan Listo: it is created with no plan (`plan` is `null`),
    nothing is charged for a plan, and its deliveries are not refused for
    lack of one. You pay for each trip and for the add-ons you switch on.

    A test store has no plan.

    Args:
        idempotency_key (str | Unset):
        body (CreateStoreRequest): The pickup location to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
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
    body: CreateStoreRequest,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Store | None:
    """Create a store

     Registers a pickup location. `lat`/`lng` are optional; send them when
    you have them and we take them as given, otherwise we geocode `street`.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `timezone` is derived from the store's position, and you do not have to
    send one. Mexico spans five zones, and the store's own position is what
    decides which one it keeps its hours in: its scheduled pickup windows,
    its delivery timestamps and its settlement week are all read in it.

    A `timezone` you do send is used only when the position cannot answer:
    a store with no coordinates, or a position no zone claims. One that
    disagrees with the position does not change the store and is not an
    error: the store is created, everything else you sent is applied, and
    the zone the position gives is what comes back.

    We would rather correct that quietly than refuse it, because we cannot
    tell the two cases apart from here: a zone sent by default out of a form
    that never asked its user arrives looking exactly like a zone somebody
    chose, and the first store provisioned against the old rule landed an
    hour ahead of itself for a year of opening hours, delivery timestamps
    and settlement weeks. Your store's position is evidence about where it
    is. If a store's clock looks wrong, its coordinates are what to fix.

    `default_business_fee_share` is the share of the delivery fee this store
    covers by default, 0 to 100, with the rest charged to the customer.
    Every `cash` or `card` delivery from the store inherits it unless the
    create overrides it. A `prepaid` delivery, and a quote that names no
    `payment_method`, always carry share 100 instead: the whole fee is yours.

    A store can also split the fee by a fixed peso amount instead of a
    percentage, which `default_fee_split_mode` on the store object tells you
    and `default_fee_split_amount_cents` carries. Both are read-only: the
    restaurant chooses the shape in its own Listo console, and there is no
    field here to set one. Read the mode before you read the share, because
    in an amount mode the share is not the split in force. Sending
    `default_business_fee_share` moves the store back to `percent`, on this
    endpoint and on the update.

    `owner_email` is optional, and it is a precondition rather than an
    attribute: send the address of whoever runs the location and we check it
    against the restaurants that already have a Listo account of their own.
    If one exists, nothing is created and you get `409 account_exists`,
    because a second account for a kitchen that already has one would split
    its balance, its console and its history in two. Ask its owner to
    connect the account they have instead, with `POST /v1/connect_requests`,
    as [Connect a restaurant that already uses Listo](https://docs.listo.delivery/en/guides/connect-
    existing-account)
    describes.

    Nothing stores the address and no store object echoes it. It does not
    create a login either; that is `POST /v1/stores/{id}/owner`.

    Listo delivers in Mexico, and a `street` that resolves to another
    country is refused with `422 unsupported_country`: nothing is created,
    and no other address in that country will work either. An address we
    cannot resolve at all is not refused. It is stored as you sent it and
    located on the first delivery.

    What a live create does about the store's Plan Listo depends on who
    pays it on your account (see
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing)).

    If you pay your stores' plans, the store starts its Plan Listo and its
    first month is charged to you in this same request, from your live
    balance or from the card saved on your account. Fund one of them first,
    and send an `Idempotency-Key` on every live create: a create that timed
    out and is repeated without one makes a second store, and the second
    store starts a second plan. A store whose first charge fails is still
    created and still answers `201`, with `plan.status` `awaiting_payment`:
    it has no plan yet, nothing is past due, and its deliveries are refused
    with `402 plan_required` until your balance or card covers the month,
    which Listo then charges by itself.

    If your account is set up so that each restaurant pays its own plan,
    nothing is charged to you: the store is created with no plan (`plan` is
    `null`) and the restaurant buys its own Plan Listo in its Listo console.
    Its deliveries are refused with `402 plan_required` until it does.

    If your account is on Listo's self-serve pricing, the store you create
    carries no Plan Listo: it is created with no plan (`plan` is `null`),
    nothing is charged for a plan, and its deliveries are not refused for
    lack of one. You pay for each trip and for the add-ons you switch on.

    A test store has no plan.

    Args:
        idempotency_key (str | Unset):
        body (CreateStoreRequest): The pickup location to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateStoreRequest,
    idempotency_key: str | Unset = UNSET,
) -> Response[ErrorResponse | Store]:
    """Create a store

     Registers a pickup location. `lat`/`lng` are optional; send them when
    you have them and we take them as given, otherwise we geocode `street`.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `timezone` is derived from the store's position, and you do not have to
    send one. Mexico spans five zones, and the store's own position is what
    decides which one it keeps its hours in: its scheduled pickup windows,
    its delivery timestamps and its settlement week are all read in it.

    A `timezone` you do send is used only when the position cannot answer:
    a store with no coordinates, or a position no zone claims. One that
    disagrees with the position does not change the store and is not an
    error: the store is created, everything else you sent is applied, and
    the zone the position gives is what comes back.

    We would rather correct that quietly than refuse it, because we cannot
    tell the two cases apart from here: a zone sent by default out of a form
    that never asked its user arrives looking exactly like a zone somebody
    chose, and the first store provisioned against the old rule landed an
    hour ahead of itself for a year of opening hours, delivery timestamps
    and settlement weeks. Your store's position is evidence about where it
    is. If a store's clock looks wrong, its coordinates are what to fix.

    `default_business_fee_share` is the share of the delivery fee this store
    covers by default, 0 to 100, with the rest charged to the customer.
    Every `cash` or `card` delivery from the store inherits it unless the
    create overrides it. A `prepaid` delivery, and a quote that names no
    `payment_method`, always carry share 100 instead: the whole fee is yours.

    A store can also split the fee by a fixed peso amount instead of a
    percentage, which `default_fee_split_mode` on the store object tells you
    and `default_fee_split_amount_cents` carries. Both are read-only: the
    restaurant chooses the shape in its own Listo console, and there is no
    field here to set one. Read the mode before you read the share, because
    in an amount mode the share is not the split in force. Sending
    `default_business_fee_share` moves the store back to `percent`, on this
    endpoint and on the update.

    `owner_email` is optional, and it is a precondition rather than an
    attribute: send the address of whoever runs the location and we check it
    against the restaurants that already have a Listo account of their own.
    If one exists, nothing is created and you get `409 account_exists`,
    because a second account for a kitchen that already has one would split
    its balance, its console and its history in two. Ask its owner to
    connect the account they have instead, with `POST /v1/connect_requests`,
    as [Connect a restaurant that already uses Listo](https://docs.listo.delivery/en/guides/connect-
    existing-account)
    describes.

    Nothing stores the address and no store object echoes it. It does not
    create a login either; that is `POST /v1/stores/{id}/owner`.

    Listo delivers in Mexico, and a `street` that resolves to another
    country is refused with `422 unsupported_country`: nothing is created,
    and no other address in that country will work either. An address we
    cannot resolve at all is not refused. It is stored as you sent it and
    located on the first delivery.

    What a live create does about the store's Plan Listo depends on who
    pays it on your account (see
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing)).

    If you pay your stores' plans, the store starts its Plan Listo and its
    first month is charged to you in this same request, from your live
    balance or from the card saved on your account. Fund one of them first,
    and send an `Idempotency-Key` on every live create: a create that timed
    out and is repeated without one makes a second store, and the second
    store starts a second plan. A store whose first charge fails is still
    created and still answers `201`, with `plan.status` `awaiting_payment`:
    it has no plan yet, nothing is past due, and its deliveries are refused
    with `402 plan_required` until your balance or card covers the month,
    which Listo then charges by itself.

    If your account is set up so that each restaurant pays its own plan,
    nothing is charged to you: the store is created with no plan (`plan` is
    `null`) and the restaurant buys its own Plan Listo in its Listo console.
    Its deliveries are refused with `402 plan_required` until it does.

    If your account is on Listo's self-serve pricing, the store you create
    carries no Plan Listo: it is created with no plan (`plan` is `null`),
    nothing is charged for a plan, and its deliveries are not refused for
    lack of one. You pay for each trip and for the add-ons you switch on.

    A test store has no plan.

    Args:
        idempotency_key (str | Unset):
        body (CreateStoreRequest): The pickup location to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
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
    body: CreateStoreRequest,
    idempotency_key: str | Unset = UNSET,
) -> ErrorResponse | Store | None:
    """Create a store

     Registers a pickup location. `lat`/`lng` are optional; send them when
    you have them and we take them as given, otherwise we geocode `street`.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    `timezone` is derived from the store's position, and you do not have to
    send one. Mexico spans five zones, and the store's own position is what
    decides which one it keeps its hours in: its scheduled pickup windows,
    its delivery timestamps and its settlement week are all read in it.

    A `timezone` you do send is used only when the position cannot answer:
    a store with no coordinates, or a position no zone claims. One that
    disagrees with the position does not change the store and is not an
    error: the store is created, everything else you sent is applied, and
    the zone the position gives is what comes back.

    We would rather correct that quietly than refuse it, because we cannot
    tell the two cases apart from here: a zone sent by default out of a form
    that never asked its user arrives looking exactly like a zone somebody
    chose, and the first store provisioned against the old rule landed an
    hour ahead of itself for a year of opening hours, delivery timestamps
    and settlement weeks. Your store's position is evidence about where it
    is. If a store's clock looks wrong, its coordinates are what to fix.

    `default_business_fee_share` is the share of the delivery fee this store
    covers by default, 0 to 100, with the rest charged to the customer.
    Every `cash` or `card` delivery from the store inherits it unless the
    create overrides it. A `prepaid` delivery, and a quote that names no
    `payment_method`, always carry share 100 instead: the whole fee is yours.

    A store can also split the fee by a fixed peso amount instead of a
    percentage, which `default_fee_split_mode` on the store object tells you
    and `default_fee_split_amount_cents` carries. Both are read-only: the
    restaurant chooses the shape in its own Listo console, and there is no
    field here to set one. Read the mode before you read the share, because
    in an amount mode the share is not the split in force. Sending
    `default_business_fee_share` moves the store back to `percent`, on this
    endpoint and on the update.

    `owner_email` is optional, and it is a precondition rather than an
    attribute: send the address of whoever runs the location and we check it
    against the restaurants that already have a Listo account of their own.
    If one exists, nothing is created and you get `409 account_exists`,
    because a second account for a kitchen that already has one would split
    its balance, its console and its history in two. Ask its owner to
    connect the account they have instead, with `POST /v1/connect_requests`,
    as [Connect a restaurant that already uses Listo](https://docs.listo.delivery/en/guides/connect-
    existing-account)
    describes.

    Nothing stores the address and no store object echoes it. It does not
    create a login either; that is `POST /v1/stores/{id}/owner`.

    Listo delivers in Mexico, and a `street` that resolves to another
    country is refused with `422 unsupported_country`: nothing is created,
    and no other address in that country will work either. An address we
    cannot resolve at all is not refused. It is stored as you sent it and
    located on the first delivery.

    What a live create does about the store's Plan Listo depends on who
    pays it on your account (see
    [Plan and billing](https://docs.listo.delivery/en/guides/plan-and-billing)).

    If you pay your stores' plans, the store starts its Plan Listo and its
    first month is charged to you in this same request, from your live
    balance or from the card saved on your account. Fund one of them first,
    and send an `Idempotency-Key` on every live create: a create that timed
    out and is repeated without one makes a second store, and the second
    store starts a second plan. A store whose first charge fails is still
    created and still answers `201`, with `plan.status` `awaiting_payment`:
    it has no plan yet, nothing is past due, and its deliveries are refused
    with `402 plan_required` until your balance or card covers the month,
    which Listo then charges by itself.

    If your account is set up so that each restaurant pays its own plan,
    nothing is charged to you: the store is created with no plan (`plan` is
    `null`) and the restaurant buys its own Plan Listo in its Listo console.
    Its deliveries are refused with `402 plan_required` until it does.

    If your account is on Listo's self-serve pricing, the store you create
    carries no Plan Listo: it is created with no plan (`plan` is `null`),
    nothing is charged for a plan, and its deliveries are not refused for
    lack of one. You pay for each trip and for the add-ons you switch on.

    A test store has no plan.

    Args:
        idempotency_key (str | Unset):
        body (CreateStoreRequest): The pickup location to create.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
        )
    ).parsed
