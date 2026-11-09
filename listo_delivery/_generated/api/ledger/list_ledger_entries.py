from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.ledger_entry_list import LedgerEntryList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["delivery_id"] = delivery_id

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/ledger",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | LedgerEntryList | None:
    if response.status_code == 200:
        response_200 = LedgerEntryList.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | LedgerEntryList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> Response[ErrorResponse | LedgerEntryList]:
    """List your ledger entries

     Every movement on your balance, newest first, keyset-paginated. This is
    the reconciliation surface: close a period by walking it rather than by
    adding up webhook events, so an event you missed, or one you had resent,
    changes nothing about what you can rebuild.

    `amount_cents` is signed, credits positive and debits negative, which is
    what lets a page sum to the movement in your balance across it. Read the
    direction off that sign and never off `type`.

    `type` says where a movement came from. The pair worth knowing is the
    one a wasted trip produces:

    - `provider_charge` is the delivery fee billed for a late cancellation
      or a return trip, one fee per leg that was driven, less your own
      store markup. Negative, and tied to the order that caused it. **This
      amount changed on 2026-08-29**: it used to be what the wasted trip
      cost Listo, so expect larger values on the same orders from that date
      onward. The row itself is unchanged.
    - `provider_charge_reversal` is that charge credited back in full, when
      the cost turns out not to have been owed. Positive, and posted as its
      own row against the same `delivery_id` rather than as a reduction of
      the original charge, so what you were billed and what came back are
      both still readable. It can arrive weeks after the charge. Pair the
      two by `delivery_id` and expect equal and opposite amounts.

    A third value can appear on the same order and is a different amount
    under a different heading:

    - `order_value_reimbursement` is the value of an order a courier
      collected that reached nobody, credited after we claim it. Positive,
      tied to the order it belongs to, and NOT paired with any debit on this
      ledger: the order's value never moved through your balance, so there
      is nothing to net it against. It is decided case by case and is not
      guaranteed, so never derive it from the order total or expect one per
      incident.
    - `listo_charge_correction` is a charge Listo made in error and gave
      back: a `provider_charge` that turned out not to be yours to pay.
      Positive, tied to the order it corrects, and posted as its own row
      beside the original charge, never as a reduction of it. Pair it with
      the charge by `delivery_id`; it can be less than the charge, and an
      order can carry more than one. It is decided case by case, so never
      derive it from a charge or expect one per charge.
    - `requote_adjustment` is the difference between the fee your order was
      charged and the fee the courier network booked for its trip, when the
      two are not the same. Signed: negative when the booked trip cost more
      than you were charged, positive when it cost less. Tied to the order,
      posted as its own row beside the order's own charge and never as a
      rewrite of it, and a retry of the same order trues it up to the trip
      finally booked rather than adding another. It is not paired with any
      other row, and it is uncommon.

    Two more are a store's Plan Listo, paid from your balance:

    - `plan_charge` is one month of a store's plan, IVA included. Negative.
      A month paid by card writes no row, because it never touched the
      balance.
    - `plan_extra_charge` is the WhatsApp assistant's conversations past
      what a `full` store's plan includes, charged to you with that store's
      plan. Negative.

    Three more are a store's add-ons, paid from your balance:

    - `add_on_charge` is one month of the Food rating add-on (`ratings`),
      IVA included. Negative, and tied to the
      store. A month paid by card writes no row, because it never touched
      the balance.
    - `customer_whatsapp_use` is the WhatsApp updates add-on's charge for
      one delivered trip. Negative, and tied to the order it belongs to.
    - `card_payments_use` is the card payments add-on's charge for one
      paid card payment. Negative, and tied to the order it belongs to.

    `store_id` names the store a movement belongs to, on every row: the
    store of the order, or the store whose plan was paid. It is `null` when
    a movement belongs to no single store, such as a top-up or a withdrawal.

    This vocabulary GROWS. New values can appear in any release, because v1
    changes additively and a movement you cannot yet name is still money
    that moved. So branch on the values you know and let the rest fall
    through: count an unfamiliar `type` toward the balance, show it, and do
    not drop it or reject it. Rows you discard are the difference between
    your books and `GET /v1/balance`.

    Args:
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LedgerEntryList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> ErrorResponse | LedgerEntryList | None:
    """List your ledger entries

     Every movement on your balance, newest first, keyset-paginated. This is
    the reconciliation surface: close a period by walking it rather than by
    adding up webhook events, so an event you missed, or one you had resent,
    changes nothing about what you can rebuild.

    `amount_cents` is signed, credits positive and debits negative, which is
    what lets a page sum to the movement in your balance across it. Read the
    direction off that sign and never off `type`.

    `type` says where a movement came from. The pair worth knowing is the
    one a wasted trip produces:

    - `provider_charge` is the delivery fee billed for a late cancellation
      or a return trip, one fee per leg that was driven, less your own
      store markup. Negative, and tied to the order that caused it. **This
      amount changed on 2026-08-29**: it used to be what the wasted trip
      cost Listo, so expect larger values on the same orders from that date
      onward. The row itself is unchanged.
    - `provider_charge_reversal` is that charge credited back in full, when
      the cost turns out not to have been owed. Positive, and posted as its
      own row against the same `delivery_id` rather than as a reduction of
      the original charge, so what you were billed and what came back are
      both still readable. It can arrive weeks after the charge. Pair the
      two by `delivery_id` and expect equal and opposite amounts.

    A third value can appear on the same order and is a different amount
    under a different heading:

    - `order_value_reimbursement` is the value of an order a courier
      collected that reached nobody, credited after we claim it. Positive,
      tied to the order it belongs to, and NOT paired with any debit on this
      ledger: the order's value never moved through your balance, so there
      is nothing to net it against. It is decided case by case and is not
      guaranteed, so never derive it from the order total or expect one per
      incident.
    - `listo_charge_correction` is a charge Listo made in error and gave
      back: a `provider_charge` that turned out not to be yours to pay.
      Positive, tied to the order it corrects, and posted as its own row
      beside the original charge, never as a reduction of it. Pair it with
      the charge by `delivery_id`; it can be less than the charge, and an
      order can carry more than one. It is decided case by case, so never
      derive it from a charge or expect one per charge.
    - `requote_adjustment` is the difference between the fee your order was
      charged and the fee the courier network booked for its trip, when the
      two are not the same. Signed: negative when the booked trip cost more
      than you were charged, positive when it cost less. Tied to the order,
      posted as its own row beside the order's own charge and never as a
      rewrite of it, and a retry of the same order trues it up to the trip
      finally booked rather than adding another. It is not paired with any
      other row, and it is uncommon.

    Two more are a store's Plan Listo, paid from your balance:

    - `plan_charge` is one month of a store's plan, IVA included. Negative.
      A month paid by card writes no row, because it never touched the
      balance.
    - `plan_extra_charge` is the WhatsApp assistant's conversations past
      what a `full` store's plan includes, charged to you with that store's
      plan. Negative.

    Three more are a store's add-ons, paid from your balance:

    - `add_on_charge` is one month of the Food rating add-on (`ratings`),
      IVA included. Negative, and tied to the
      store. A month paid by card writes no row, because it never touched
      the balance.
    - `customer_whatsapp_use` is the WhatsApp updates add-on's charge for
      one delivered trip. Negative, and tied to the order it belongs to.
    - `card_payments_use` is the card payments add-on's charge for one
      paid card payment. Negative, and tied to the order it belongs to.

    `store_id` names the store a movement belongs to, on every row: the
    store of the order, or the store whose plan was paid. It is `null` when
    a movement belongs to no single store, such as a top-up or a withdrawal.

    This vocabulary GROWS. New values can appear in any release, because v1
    changes additively and a movement you cannot yet name is still money
    that moved. So branch on the values you know and let the rest fall
    through: count an unfamiliar `type` toward the balance, show it, and do
    not drop it or reject it. Rows you discard are the difference between
    your books and `GET /v1/balance`.

    Args:
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LedgerEntryList
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> Response[ErrorResponse | LedgerEntryList]:
    """List your ledger entries

     Every movement on your balance, newest first, keyset-paginated. This is
    the reconciliation surface: close a period by walking it rather than by
    adding up webhook events, so an event you missed, or one you had resent,
    changes nothing about what you can rebuild.

    `amount_cents` is signed, credits positive and debits negative, which is
    what lets a page sum to the movement in your balance across it. Read the
    direction off that sign and never off `type`.

    `type` says where a movement came from. The pair worth knowing is the
    one a wasted trip produces:

    - `provider_charge` is the delivery fee billed for a late cancellation
      or a return trip, one fee per leg that was driven, less your own
      store markup. Negative, and tied to the order that caused it. **This
      amount changed on 2026-08-29**: it used to be what the wasted trip
      cost Listo, so expect larger values on the same orders from that date
      onward. The row itself is unchanged.
    - `provider_charge_reversal` is that charge credited back in full, when
      the cost turns out not to have been owed. Positive, and posted as its
      own row against the same `delivery_id` rather than as a reduction of
      the original charge, so what you were billed and what came back are
      both still readable. It can arrive weeks after the charge. Pair the
      two by `delivery_id` and expect equal and opposite amounts.

    A third value can appear on the same order and is a different amount
    under a different heading:

    - `order_value_reimbursement` is the value of an order a courier
      collected that reached nobody, credited after we claim it. Positive,
      tied to the order it belongs to, and NOT paired with any debit on this
      ledger: the order's value never moved through your balance, so there
      is nothing to net it against. It is decided case by case and is not
      guaranteed, so never derive it from the order total or expect one per
      incident.
    - `listo_charge_correction` is a charge Listo made in error and gave
      back: a `provider_charge` that turned out not to be yours to pay.
      Positive, tied to the order it corrects, and posted as its own row
      beside the original charge, never as a reduction of it. Pair it with
      the charge by `delivery_id`; it can be less than the charge, and an
      order can carry more than one. It is decided case by case, so never
      derive it from a charge or expect one per charge.
    - `requote_adjustment` is the difference between the fee your order was
      charged and the fee the courier network booked for its trip, when the
      two are not the same. Signed: negative when the booked trip cost more
      than you were charged, positive when it cost less. Tied to the order,
      posted as its own row beside the order's own charge and never as a
      rewrite of it, and a retry of the same order trues it up to the trip
      finally booked rather than adding another. It is not paired with any
      other row, and it is uncommon.

    Two more are a store's Plan Listo, paid from your balance:

    - `plan_charge` is one month of a store's plan, IVA included. Negative.
      A month paid by card writes no row, because it never touched the
      balance.
    - `plan_extra_charge` is the WhatsApp assistant's conversations past
      what a `full` store's plan includes, charged to you with that store's
      plan. Negative.

    Three more are a store's add-ons, paid from your balance:

    - `add_on_charge` is one month of the Food rating add-on (`ratings`),
      IVA included. Negative, and tied to the
      store. A month paid by card writes no row, because it never touched
      the balance.
    - `customer_whatsapp_use` is the WhatsApp updates add-on's charge for
      one delivered trip. Negative, and tied to the order it belongs to.
    - `card_payments_use` is the card payments add-on's charge for one
      paid card payment. Negative, and tied to the order it belongs to.

    `store_id` names the store a movement belongs to, on every row: the
    store of the order, or the store whose plan was paid. It is `null` when
    a movement belongs to no single store, such as a top-up or a withdrawal.

    This vocabulary GROWS. New values can appear in any release, because v1
    changes additively and a movement you cannot yet name is still money
    that moved. So branch on the values you know and let the rest fall
    through: count an unfamiliar `type` toward the balance, show it, and do
    not drop it or reject it. Rows you discard are the difference between
    your books and `GET /v1/balance`.

    Args:
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LedgerEntryList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        delivery_id=delivery_id,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    delivery_id: str | Unset = UNSET,
    type_: str | Unset = UNSET,
) -> ErrorResponse | LedgerEntryList | None:
    """List your ledger entries

     Every movement on your balance, newest first, keyset-paginated. This is
    the reconciliation surface: close a period by walking it rather than by
    adding up webhook events, so an event you missed, or one you had resent,
    changes nothing about what you can rebuild.

    `amount_cents` is signed, credits positive and debits negative, which is
    what lets a page sum to the movement in your balance across it. Read the
    direction off that sign and never off `type`.

    `type` says where a movement came from. The pair worth knowing is the
    one a wasted trip produces:

    - `provider_charge` is the delivery fee billed for a late cancellation
      or a return trip, one fee per leg that was driven, less your own
      store markup. Negative, and tied to the order that caused it. **This
      amount changed on 2026-08-29**: it used to be what the wasted trip
      cost Listo, so expect larger values on the same orders from that date
      onward. The row itself is unchanged.
    - `provider_charge_reversal` is that charge credited back in full, when
      the cost turns out not to have been owed. Positive, and posted as its
      own row against the same `delivery_id` rather than as a reduction of
      the original charge, so what you were billed and what came back are
      both still readable. It can arrive weeks after the charge. Pair the
      two by `delivery_id` and expect equal and opposite amounts.

    A third value can appear on the same order and is a different amount
    under a different heading:

    - `order_value_reimbursement` is the value of an order a courier
      collected that reached nobody, credited after we claim it. Positive,
      tied to the order it belongs to, and NOT paired with any debit on this
      ledger: the order's value never moved through your balance, so there
      is nothing to net it against. It is decided case by case and is not
      guaranteed, so never derive it from the order total or expect one per
      incident.
    - `listo_charge_correction` is a charge Listo made in error and gave
      back: a `provider_charge` that turned out not to be yours to pay.
      Positive, tied to the order it corrects, and posted as its own row
      beside the original charge, never as a reduction of it. Pair it with
      the charge by `delivery_id`; it can be less than the charge, and an
      order can carry more than one. It is decided case by case, so never
      derive it from a charge or expect one per charge.
    - `requote_adjustment` is the difference between the fee your order was
      charged and the fee the courier network booked for its trip, when the
      two are not the same. Signed: negative when the booked trip cost more
      than you were charged, positive when it cost less. Tied to the order,
      posted as its own row beside the order's own charge and never as a
      rewrite of it, and a retry of the same order trues it up to the trip
      finally booked rather than adding another. It is not paired with any
      other row, and it is uncommon.

    Two more are a store's Plan Listo, paid from your balance:

    - `plan_charge` is one month of a store's plan, IVA included. Negative.
      A month paid by card writes no row, because it never touched the
      balance.
    - `plan_extra_charge` is the WhatsApp assistant's conversations past
      what a `full` store's plan includes, charged to you with that store's
      plan. Negative.

    Three more are a store's add-ons, paid from your balance:

    - `add_on_charge` is one month of the Food rating add-on (`ratings`),
      IVA included. Negative, and tied to the
      store. A month paid by card writes no row, because it never touched
      the balance.
    - `customer_whatsapp_use` is the WhatsApp updates add-on's charge for
      one delivered trip. Negative, and tied to the order it belongs to.
    - `card_payments_use` is the card payments add-on's charge for one
      paid card payment. Negative, and tied to the order it belongs to.

    `store_id` names the store a movement belongs to, on every row: the
    store of the order, or the store whose plan was paid. It is `null` when
    a movement belongs to no single store, such as a top-up or a withdrawal.

    This vocabulary GROWS. New values can appear in any release, because v1
    changes additively and a movement you cannot yet name is still money
    that moved. So branch on the values you know and let the rest fall
    through: count an unfamiliar `type` toward the balance, show it, and do
    not drop it or reject it. Rows you discard are the difference between
    your books and `GET /v1/balance`.

    Args:
        cursor (str | Unset):
        delivery_id (str | Unset):
        type_ (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LedgerEntryList
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            delivery_id=delivery_id,
            type_=type_,
        )
    ).parsed
