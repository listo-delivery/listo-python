from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.store import Store
from ...models.update_store_request import UpdateStoreRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    body: UpdateStoreRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/stores/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateStoreRequest | Unset = UNSET,
) -> Response[ErrorResponse | Store]:
    """Update a store

     Updates a store. Send only the fields you are changing. Existing
    deliveries are unaffected: the pickup name, street and coordinates are
    snapshotted onto each delivery when it is created, so a rename or a move
    never rewrites where a past courier actually went.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    Moving a store re-derives its `timezone` from its new position, so a
    location that moves to another zone is corrected by the same request
    that moves it, and a request that does not move the store leaves the
    zone alone.

    A `timezone` you send follows the create's rule: it is used only when
    the store's position cannot answer, never in place of a zone the
    position does answer. Sending one that disagrees changes nothing, and it
    is not an error.

    A `street` that moves the store to another country is refused with
    `422 unsupported_country`, exactly as on the create, and the store keeps
    the address it had.

    `add_ons` switches the store's paid add-ons on and off. On Listo's
    self-serve pricing, the stores your account created itself can hold
    add-ons; any other store answers `422 add_ons_unavailable`. Send only the keys you are changing; a
    key you
    leave out is untouched. Switching a pay-per-use add-on on or off
    (`customer_whatsapp`, `card_payments`) is free and immediate, and it is
    charged afterwards, per use. Switching the monthly add-on `ratings` on
    charges its first month now, from your balance, or from your saved card
    if you chose card, and the add-on is on only once that month is paid. If
    it cannot be paid the request is refused with `402
    insufficient_balance`, nothing is charged, the add-on stays off and none
    of the other fields in the same request is saved. Switching a monthly
    add-on off keeps it
    running until the end of the month already paid. A card payment the bank
    has not answered yet answers `409 charge_in_flight`; repeat the request
    shortly. `wallet` and `full_console` cannot be switched on: they read
    `available: false`, and asking to switch either on is refused with `422
    validation_failed` and `param: "add_ons.wallet"` or
    `"add_ons.full_console"`, before anything is changed or charged.
    Switching them off is accepted. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    Args:
        id (str):
        body (UpdateStoreRequest | Unset): The fields to change. Send only the ones you are
            changing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
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
    body: UpdateStoreRequest | Unset = UNSET,
) -> ErrorResponse | Store | None:
    """Update a store

     Updates a store. Send only the fields you are changing. Existing
    deliveries are unaffected: the pickup name, street and coordinates are
    snapshotted onto each delivery when it is created, so a rename or a move
    never rewrites where a past courier actually went.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    Moving a store re-derives its `timezone` from its new position, so a
    location that moves to another zone is corrected by the same request
    that moves it, and a request that does not move the store leaves the
    zone alone.

    A `timezone` you send follows the create's rule: it is used only when
    the store's position cannot answer, never in place of a zone the
    position does answer. Sending one that disagrees changes nothing, and it
    is not an error.

    A `street` that moves the store to another country is refused with
    `422 unsupported_country`, exactly as on the create, and the store keeps
    the address it had.

    `add_ons` switches the store's paid add-ons on and off. On Listo's
    self-serve pricing, the stores your account created itself can hold
    add-ons; any other store answers `422 add_ons_unavailable`. Send only the keys you are changing; a
    key you
    leave out is untouched. Switching a pay-per-use add-on on or off
    (`customer_whatsapp`, `card_payments`) is free and immediate, and it is
    charged afterwards, per use. Switching the monthly add-on `ratings` on
    charges its first month now, from your balance, or from your saved card
    if you chose card, and the add-on is on only once that month is paid. If
    it cannot be paid the request is refused with `402
    insufficient_balance`, nothing is charged, the add-on stays off and none
    of the other fields in the same request is saved. Switching a monthly
    add-on off keeps it
    running until the end of the month already paid. A card payment the bank
    has not answered yet answers `409 charge_in_flight`; repeat the request
    shortly. `wallet` and `full_console` cannot be switched on: they read
    `available: false`, and asking to switch either on is refused with `422
    validation_failed` and `param: "add_ons.wallet"` or
    `"add_ons.full_console"`, before anything is changed or charged.
    Switching them off is accepted. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    Args:
        id (str):
        body (UpdateStoreRequest | Unset): The fields to change. Send only the ones you are
            changing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
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
    body: UpdateStoreRequest | Unset = UNSET,
) -> Response[ErrorResponse | Store]:
    """Update a store

     Updates a store. Send only the fields you are changing. Existing
    deliveries are unaffected: the pickup name, street and coordinates are
    snapshotted onto each delivery when it is created, so a rename or a move
    never rewrites where a past courier actually went.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    Moving a store re-derives its `timezone` from its new position, so a
    location that moves to another zone is corrected by the same request
    that moves it, and a request that does not move the store leaves the
    zone alone.

    A `timezone` you send follows the create's rule: it is used only when
    the store's position cannot answer, never in place of a zone the
    position does answer. Sending one that disagrees changes nothing, and it
    is not an error.

    A `street` that moves the store to another country is refused with
    `422 unsupported_country`, exactly as on the create, and the store keeps
    the address it had.

    `add_ons` switches the store's paid add-ons on and off. On Listo's
    self-serve pricing, the stores your account created itself can hold
    add-ons; any other store answers `422 add_ons_unavailable`. Send only the keys you are changing; a
    key you
    leave out is untouched. Switching a pay-per-use add-on on or off
    (`customer_whatsapp`, `card_payments`) is free and immediate, and it is
    charged afterwards, per use. Switching the monthly add-on `ratings` on
    charges its first month now, from your balance, or from your saved card
    if you chose card, and the add-on is on only once that month is paid. If
    it cannot be paid the request is refused with `402
    insufficient_balance`, nothing is charged, the add-on stays off and none
    of the other fields in the same request is saved. Switching a monthly
    add-on off keeps it
    running until the end of the month already paid. A card payment the bank
    has not answered yet answers `409 charge_in_flight`; repeat the request
    shortly. `wallet` and `full_console` cannot be switched on: they read
    `available: false`, and asking to switch either on is refused with `422
    validation_failed` and `param: "add_ons.wallet"` or
    `"add_ons.full_console"`, before anything is changed or charged.
    Switching them off is accepted. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    Args:
        id (str):
        body (UpdateStoreRequest | Unset): The fields to change. Send only the ones you are
            changing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Store]
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
    body: UpdateStoreRequest | Unset = UNSET,
) -> ErrorResponse | Store | None:
    """Update a store

     Updates a store. Send only the fields you are changing. Existing
    deliveries are unaffected: the pickup name, street and coordinates are
    snapshotted onto each delivery when it is created, so a rename or a move
    never rewrites where a past courier actually went.

    `phone` is E.164. A Mexican number is +52 followed by its 10 digits (+52 1 followed by 10 is
    accepted as WhatsApp writes it); a US or Canadian number is +1 followed by its 10 digits; a number
    from any other country is accepted with 8 to 15 digits in total. Anything else is refused with
    `validation_failed`.

    Moving a store re-derives its `timezone` from its new position, so a
    location that moves to another zone is corrected by the same request
    that moves it, and a request that does not move the store leaves the
    zone alone.

    A `timezone` you send follows the create's rule: it is used only when
    the store's position cannot answer, never in place of a zone the
    position does answer. Sending one that disagrees changes nothing, and it
    is not an error.

    A `street` that moves the store to another country is refused with
    `422 unsupported_country`, exactly as on the create, and the store keeps
    the address it had.

    `add_ons` switches the store's paid add-ons on and off. On Listo's
    self-serve pricing, the stores your account created itself can hold
    add-ons; any other store answers `422 add_ons_unavailable`. Send only the keys you are changing; a
    key you
    leave out is untouched. Switching a pay-per-use add-on on or off
    (`customer_whatsapp`, `card_payments`) is free and immediate, and it is
    charged afterwards, per use. Switching the monthly add-on `ratings` on
    charges its first month now, from your balance, or from your saved card
    if you chose card, and the add-on is on only once that month is paid. If
    it cannot be paid the request is refused with `402
    insufficient_balance`, nothing is charged, the add-on stays off and none
    of the other fields in the same request is saved. Switching a monthly
    add-on off keeps it
    running until the end of the month already paid. A card payment the bank
    has not answered yet answers `409 charge_in_flight`; repeat the request
    shortly. `wallet` and `full_console` cannot be switched on: they read
    `available: false`, and asking to switch either on is refused with `422
    validation_failed` and `param: "add_ons.wallet"` or
    `"add_ons.full_console"`, before anything is changed or charged.
    Switching them off is accepted. See
    [Store add-ons](https://docs.listo.delivery/en/guides/store-add-ons).

    Args:
        id (str):
        body (UpdateStoreRequest | Unset): The fields to change. Send only the ones you are
            changing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Store
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
