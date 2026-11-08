from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_withdrawal_request import CreateWithdrawalRequest
from ...models.error_response import ErrorResponse
from ...models.withdrawal import Withdrawal
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWithdrawalRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/withdrawals",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Withdrawal | None:
    if response.status_code == 201:
        response_201 = Withdrawal.from_dict(response.json())

        return response_201

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = ErrorResponse.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Withdrawal]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWithdrawalRequest,
) -> Response[ErrorResponse | Withdrawal]:
    """Request a withdrawal

     Requests a transfer of `amount_cents` out of your balance to your
    registered bank account. The money is reserved the moment the request is
    accepted, so a second request cannot spend it twice.

    The request is settled by a human, usually within a business day, and
    the outcome arrives as a `withdrawal.updated` webhook rather than in
    this response. Asking for more than `available_cents` is a `402`.

    You need a bank account registered before your first withdrawal, from
    the [dashboard](https://partners.listo.delivery) rather than from this
    API. Without one this call is `422 payout_account_not_ready` and nothing
    is reserved. The same refusal covers the day after you CHANGE the
    account: a moved destination cannot receive money for 24 hours, and the
    `message` names the instant it can again.

    ### Same-day withdrawals

    `kind` is optional and `standard` when you leave it out, which is the
    free path above and is unchanged. Send `"kind": "same_day"` to have it
    sent TODAY instead:

    - It costs a flat fee, IVA included, which the response reports as
      `fee_cents`. The fee is a SECOND debit and never a deduction, so your
      bank still receives the whole `amount_cents` and your balance loses
      the two together.
    - It can draw on cash that is still on hold, which the free path cannot,
      so `available_cents` is not the bound here.
    - Requests are accepted around the clock. One made between 8 am and
      8 pm Mexico City is sent within 3 hours; one made outside those hours
      goes out the next morning. `due_at` on the response is the deadline
      your request actually carries, stamped when you made it.
    - There is a minimum per request and a daily maximum per account.

    Three refusals are specific to it and each names its bound in `message`:
    `402 insufficient_balance` when the amount plus its fee is more than can
    be withdrawn today, `422 same_day_cap_exceeded` when the day's maximum
    has no room for it, and `422 same_day_below_minimum` when the amount is
    under the floor. A `kind` that is neither word is
    `422 validation_failed` with `param: "kind"`, never a quiet fallback to
    the free path.

    Args:
        body (CreateWithdrawalRequest): How much to move out of your balance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Withdrawal]
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
    body: CreateWithdrawalRequest,
) -> ErrorResponse | Withdrawal | None:
    """Request a withdrawal

     Requests a transfer of `amount_cents` out of your balance to your
    registered bank account. The money is reserved the moment the request is
    accepted, so a second request cannot spend it twice.

    The request is settled by a human, usually within a business day, and
    the outcome arrives as a `withdrawal.updated` webhook rather than in
    this response. Asking for more than `available_cents` is a `402`.

    You need a bank account registered before your first withdrawal, from
    the [dashboard](https://partners.listo.delivery) rather than from this
    API. Without one this call is `422 payout_account_not_ready` and nothing
    is reserved. The same refusal covers the day after you CHANGE the
    account: a moved destination cannot receive money for 24 hours, and the
    `message` names the instant it can again.

    ### Same-day withdrawals

    `kind` is optional and `standard` when you leave it out, which is the
    free path above and is unchanged. Send `"kind": "same_day"` to have it
    sent TODAY instead:

    - It costs a flat fee, IVA included, which the response reports as
      `fee_cents`. The fee is a SECOND debit and never a deduction, so your
      bank still receives the whole `amount_cents` and your balance loses
      the two together.
    - It can draw on cash that is still on hold, which the free path cannot,
      so `available_cents` is not the bound here.
    - Requests are accepted around the clock. One made between 8 am and
      8 pm Mexico City is sent within 3 hours; one made outside those hours
      goes out the next morning. `due_at` on the response is the deadline
      your request actually carries, stamped when you made it.
    - There is a minimum per request and a daily maximum per account.

    Three refusals are specific to it and each names its bound in `message`:
    `402 insufficient_balance` when the amount plus its fee is more than can
    be withdrawn today, `422 same_day_cap_exceeded` when the day's maximum
    has no room for it, and `422 same_day_below_minimum` when the amount is
    under the floor. A `kind` that is neither word is
    `422 validation_failed` with `param: "kind"`, never a quiet fallback to
    the free path.

    Args:
        body (CreateWithdrawalRequest): How much to move out of your balance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Withdrawal
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWithdrawalRequest,
) -> Response[ErrorResponse | Withdrawal]:
    """Request a withdrawal

     Requests a transfer of `amount_cents` out of your balance to your
    registered bank account. The money is reserved the moment the request is
    accepted, so a second request cannot spend it twice.

    The request is settled by a human, usually within a business day, and
    the outcome arrives as a `withdrawal.updated` webhook rather than in
    this response. Asking for more than `available_cents` is a `402`.

    You need a bank account registered before your first withdrawal, from
    the [dashboard](https://partners.listo.delivery) rather than from this
    API. Without one this call is `422 payout_account_not_ready` and nothing
    is reserved. The same refusal covers the day after you CHANGE the
    account: a moved destination cannot receive money for 24 hours, and the
    `message` names the instant it can again.

    ### Same-day withdrawals

    `kind` is optional and `standard` when you leave it out, which is the
    free path above and is unchanged. Send `"kind": "same_day"` to have it
    sent TODAY instead:

    - It costs a flat fee, IVA included, which the response reports as
      `fee_cents`. The fee is a SECOND debit and never a deduction, so your
      bank still receives the whole `amount_cents` and your balance loses
      the two together.
    - It can draw on cash that is still on hold, which the free path cannot,
      so `available_cents` is not the bound here.
    - Requests are accepted around the clock. One made between 8 am and
      8 pm Mexico City is sent within 3 hours; one made outside those hours
      goes out the next morning. `due_at` on the response is the deadline
      your request actually carries, stamped when you made it.
    - There is a minimum per request and a daily maximum per account.

    Three refusals are specific to it and each names its bound in `message`:
    `402 insufficient_balance` when the amount plus its fee is more than can
    be withdrawn today, `422 same_day_cap_exceeded` when the day's maximum
    has no room for it, and `422 same_day_below_minimum` when the amount is
    under the floor. A `kind` that is neither word is
    `422 validation_failed` with `param: "kind"`, never a quiet fallback to
    the free path.

    Args:
        body (CreateWithdrawalRequest): How much to move out of your balance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Withdrawal]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateWithdrawalRequest,
) -> ErrorResponse | Withdrawal | None:
    """Request a withdrawal

     Requests a transfer of `amount_cents` out of your balance to your
    registered bank account. The money is reserved the moment the request is
    accepted, so a second request cannot spend it twice.

    The request is settled by a human, usually within a business day, and
    the outcome arrives as a `withdrawal.updated` webhook rather than in
    this response. Asking for more than `available_cents` is a `402`.

    You need a bank account registered before your first withdrawal, from
    the [dashboard](https://partners.listo.delivery) rather than from this
    API. Without one this call is `422 payout_account_not_ready` and nothing
    is reserved. The same refusal covers the day after you CHANGE the
    account: a moved destination cannot receive money for 24 hours, and the
    `message` names the instant it can again.

    ### Same-day withdrawals

    `kind` is optional and `standard` when you leave it out, which is the
    free path above and is unchanged. Send `"kind": "same_day"` to have it
    sent TODAY instead:

    - It costs a flat fee, IVA included, which the response reports as
      `fee_cents`. The fee is a SECOND debit and never a deduction, so your
      bank still receives the whole `amount_cents` and your balance loses
      the two together.
    - It can draw on cash that is still on hold, which the free path cannot,
      so `available_cents` is not the bound here.
    - Requests are accepted around the clock. One made between 8 am and
      8 pm Mexico City is sent within 3 hours; one made outside those hours
      goes out the next morning. `due_at` on the response is the deadline
      your request actually carries, stamped when you made it.
    - There is a minimum per request and a daily maximum per account.

    Three refusals are specific to it and each names its bound in `message`:
    `402 insufficient_balance` when the amount plus its fee is more than can
    be withdrawn today, `422 same_day_cap_exceeded` when the day's maximum
    has no room for it, and `422 same_day_below_minimum` when the amount is
    under the floor. A `kind` that is neither word is
    `422 validation_failed` with `param: "kind"`, never a quiet fallback to
    the free path.

    Args:
        body (CreateWithdrawalRequest): How much to move out of your balance.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Withdrawal
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
