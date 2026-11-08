from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.balance import Balance
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/balance",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Balance | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Balance.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Balance | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Balance | ErrorResponse]:
    """Read your prepaid balance

     Your prepaid balance for the world the key acts in.

    `balance_cents` is everything in the account. `available_cents` is what
    you can withdraw today, which is lower whenever cash collected at
    customers' doors has not reached us yet. Spending is not gated on
    `available_cents`; withdrawing is.

    `in_review_cents` is the part of `balance_cents` that is cash from an
    order we are still reviewing. It is always present, `0` when nothing is
    under review, and it is already left out of `available_cents`. It can
    not be advanced, and a delivery cannot be paid from it, so a create can
    answer `402 insufficient_balance` while `balance_cents` alone looks like
    enough: `balance_cents` minus `in_review_cents` is what deliveries can
    draw on. It moves when we have an answer, not on a date.

    ### The same-day offer

    `same_day` describes what a `same_day` withdrawal
    (`POST /v1/withdrawals`) would cost you right now and how large a one
    you could ask for, so you can render the choice instead of discovering
    it from a refusal. Every field is always present.

    `ceiling_cents` is the largest `amount_cents` a same-day request would
    be accepted for at this moment. **It is not another name for
    `available_cents`**: the ceiling is already net of `fee_cents` and
    already clamped to what is left of the day, and it can reach cash still
    on hold that `available_cents` excludes by definition. On one account it
    is the larger of the two and on another the smaller, so neither is
    derivable from the other.

    `reach_cents` is everything the request could draw on before the fee,
    and `advanceable_cents` is the part of that which is still-held cash.
    `cap_cents`, `cap_used_cents` and `cap_remaining_cents` are the daily
    maximum per account and today's position against it, and
    `minimum_cents` is the floor per request.

    `window_open` says whether staff are sending right now. `due_at` is the
    deadline a request made at the moment you read this WOULD carry, and
    `next_window_opens_at` is the next time sending resumes; the deadline
    your request actually carries is the `due_at` on the withdrawal object
    it returns. Requests are accepted at any hour either way.

    `offerable` is false when no same-day request would be accepted at all,
    and `unavailable_reason` says which of the two states you are in:
    `cap_reached` (today's maximum is spent, and it returns tomorrow
    morning) or `below_minimum` (the reach is too small to clear the floor
    plus the fee). It is null whenever `offerable` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Balance | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Balance | ErrorResponse | None:
    """Read your prepaid balance

     Your prepaid balance for the world the key acts in.

    `balance_cents` is everything in the account. `available_cents` is what
    you can withdraw today, which is lower whenever cash collected at
    customers' doors has not reached us yet. Spending is not gated on
    `available_cents`; withdrawing is.

    `in_review_cents` is the part of `balance_cents` that is cash from an
    order we are still reviewing. It is always present, `0` when nothing is
    under review, and it is already left out of `available_cents`. It can
    not be advanced, and a delivery cannot be paid from it, so a create can
    answer `402 insufficient_balance` while `balance_cents` alone looks like
    enough: `balance_cents` minus `in_review_cents` is what deliveries can
    draw on. It moves when we have an answer, not on a date.

    ### The same-day offer

    `same_day` describes what a `same_day` withdrawal
    (`POST /v1/withdrawals`) would cost you right now and how large a one
    you could ask for, so you can render the choice instead of discovering
    it from a refusal. Every field is always present.

    `ceiling_cents` is the largest `amount_cents` a same-day request would
    be accepted for at this moment. **It is not another name for
    `available_cents`**: the ceiling is already net of `fee_cents` and
    already clamped to what is left of the day, and it can reach cash still
    on hold that `available_cents` excludes by definition. On one account it
    is the larger of the two and on another the smaller, so neither is
    derivable from the other.

    `reach_cents` is everything the request could draw on before the fee,
    and `advanceable_cents` is the part of that which is still-held cash.
    `cap_cents`, `cap_used_cents` and `cap_remaining_cents` are the daily
    maximum per account and today's position against it, and
    `minimum_cents` is the floor per request.

    `window_open` says whether staff are sending right now. `due_at` is the
    deadline a request made at the moment you read this WOULD carry, and
    `next_window_opens_at` is the next time sending resumes; the deadline
    your request actually carries is the `due_at` on the withdrawal object
    it returns. Requests are accepted at any hour either way.

    `offerable` is false when no same-day request would be accepted at all,
    and `unavailable_reason` says which of the two states you are in:
    `cap_reached` (today's maximum is spent, and it returns tomorrow
    morning) or `below_minimum` (the reach is too small to clear the floor
    plus the fee). It is null whenever `offerable` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Balance | ErrorResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Balance | ErrorResponse]:
    """Read your prepaid balance

     Your prepaid balance for the world the key acts in.

    `balance_cents` is everything in the account. `available_cents` is what
    you can withdraw today, which is lower whenever cash collected at
    customers' doors has not reached us yet. Spending is not gated on
    `available_cents`; withdrawing is.

    `in_review_cents` is the part of `balance_cents` that is cash from an
    order we are still reviewing. It is always present, `0` when nothing is
    under review, and it is already left out of `available_cents`. It can
    not be advanced, and a delivery cannot be paid from it, so a create can
    answer `402 insufficient_balance` while `balance_cents` alone looks like
    enough: `balance_cents` minus `in_review_cents` is what deliveries can
    draw on. It moves when we have an answer, not on a date.

    ### The same-day offer

    `same_day` describes what a `same_day` withdrawal
    (`POST /v1/withdrawals`) would cost you right now and how large a one
    you could ask for, so you can render the choice instead of discovering
    it from a refusal. Every field is always present.

    `ceiling_cents` is the largest `amount_cents` a same-day request would
    be accepted for at this moment. **It is not another name for
    `available_cents`**: the ceiling is already net of `fee_cents` and
    already clamped to what is left of the day, and it can reach cash still
    on hold that `available_cents` excludes by definition. On one account it
    is the larger of the two and on another the smaller, so neither is
    derivable from the other.

    `reach_cents` is everything the request could draw on before the fee,
    and `advanceable_cents` is the part of that which is still-held cash.
    `cap_cents`, `cap_used_cents` and `cap_remaining_cents` are the daily
    maximum per account and today's position against it, and
    `minimum_cents` is the floor per request.

    `window_open` says whether staff are sending right now. `due_at` is the
    deadline a request made at the moment you read this WOULD carry, and
    `next_window_opens_at` is the next time sending resumes; the deadline
    your request actually carries is the `due_at` on the withdrawal object
    it returns. Requests are accepted at any hour either way.

    `offerable` is false when no same-day request would be accepted at all,
    and `unavailable_reason` says which of the two states you are in:
    `cap_reached` (today's maximum is spent, and it returns tomorrow
    morning) or `below_minimum` (the reach is too small to clear the floor
    plus the fee). It is null whenever `offerable` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Balance | ErrorResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Balance | ErrorResponse | None:
    """Read your prepaid balance

     Your prepaid balance for the world the key acts in.

    `balance_cents` is everything in the account. `available_cents` is what
    you can withdraw today, which is lower whenever cash collected at
    customers' doors has not reached us yet. Spending is not gated on
    `available_cents`; withdrawing is.

    `in_review_cents` is the part of `balance_cents` that is cash from an
    order we are still reviewing. It is always present, `0` when nothing is
    under review, and it is already left out of `available_cents`. It can
    not be advanced, and a delivery cannot be paid from it, so a create can
    answer `402 insufficient_balance` while `balance_cents` alone looks like
    enough: `balance_cents` minus `in_review_cents` is what deliveries can
    draw on. It moves when we have an answer, not on a date.

    ### The same-day offer

    `same_day` describes what a `same_day` withdrawal
    (`POST /v1/withdrawals`) would cost you right now and how large a one
    you could ask for, so you can render the choice instead of discovering
    it from a refusal. Every field is always present.

    `ceiling_cents` is the largest `amount_cents` a same-day request would
    be accepted for at this moment. **It is not another name for
    `available_cents`**: the ceiling is already net of `fee_cents` and
    already clamped to what is left of the day, and it can reach cash still
    on hold that `available_cents` excludes by definition. On one account it
    is the larger of the two and on another the smaller, so neither is
    derivable from the other.

    `reach_cents` is everything the request could draw on before the fee,
    and `advanceable_cents` is the part of that which is still-held cash.
    `cap_cents`, `cap_used_cents` and `cap_remaining_cents` are the daily
    maximum per account and today's position against it, and
    `minimum_cents` is the floor per request.

    `window_open` says whether staff are sending right now. `due_at` is the
    deadline a request made at the moment you read this WOULD carry, and
    `next_window_opens_at` is the next time sending resumes; the deadline
    your request actually carries is the `due_at` on the withdrawal object
    it returns. Requests are accepted at any hour either way.

    `offerable` is false when no same-day request would be accepted at all,
    and `unavailable_reason` says which of the two states you are in:
    `cap_reached` (today's maximum is spent, and it returns tomorrow
    morning) or `below_minimum` (the reach is too small to clear the floor
    plus the fee). It is null whenever `offerable` is true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Balance | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
