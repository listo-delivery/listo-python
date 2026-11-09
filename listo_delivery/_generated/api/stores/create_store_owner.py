from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_store_owner_request import CreateStoreOwnerRequest
from ...models.error_response import ErrorResponse
from ...models.owner_invitation import OwnerInvitation
from ...types import Response


def _get_kwargs(
    store_id: str,
    *,
    body: CreateStoreOwnerRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/stores/{store_id}/owner".format(
            store_id=quote(str(store_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | OwnerInvitation | None:
    if response.status_code == 201:
        response_201 = OwnerInvitation.from_dict(response.json())

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

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | OwnerInvitation]:
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
    body: CreateStoreOwnerRequest,
) -> Response[ErrorResponse | OwnerInvitation]:
    """Invite a store owner

     Gives the person who runs the store a login to its Listo console. We
    create the login and email them a link to choose their own password.
    The response carries the address the link went to and when it was
    sent, and never a password or a token, so there is nothing in it to
    store.

    Repeating the call is safe. The same address gets a fresh link rather
    than a second login, so a retry after a timeout does no harm, and it is
    also how you send the link again when the first one has expired.
    The link lasts seven days.

    An address that already has a Listo login somewhere else is fine. That
    person gets a separate login for this store, with its own password, and
    the account they already had is left as it was. Somebody who runs two of
    your locations can use the same address for both.

    Three refusals:

    - `422 console_access_required` on a store whose `access_tier` is
      `api_only` and that holds no balance to withdraw. That store has no
      console to sign in to, so there is nothing to invite anybody to. Give
      the store a tier first (on a store of an account that buys add-ons,
      switch on its Restaurant balance or Full console add-on), then call
      this again.
    - `422 validation_failed` with `param: "email"` when the store already
      has an owner at a different address. The `message` names that owner.
      A store has one owner, and this endpoint cannot change who it is. To
      send the owner a fresh link, call it with the address the `message`
      names.
    - `422 validation_failed` with `param: "email"` when another request is
      setting up the same address for this store at the same moment. Repeat
      the call: by then the first one has finished, and yours sends the link
      again.

    Args:
        store_id (str):
        body (CreateStoreOwnerRequest): The person to invite as the store's owner.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OwnerInvitation]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateStoreOwnerRequest,
) -> ErrorResponse | OwnerInvitation | None:
    """Invite a store owner

     Gives the person who runs the store a login to its Listo console. We
    create the login and email them a link to choose their own password.
    The response carries the address the link went to and when it was
    sent, and never a password or a token, so there is nothing in it to
    store.

    Repeating the call is safe. The same address gets a fresh link rather
    than a second login, so a retry after a timeout does no harm, and it is
    also how you send the link again when the first one has expired.
    The link lasts seven days.

    An address that already has a Listo login somewhere else is fine. That
    person gets a separate login for this store, with its own password, and
    the account they already had is left as it was. Somebody who runs two of
    your locations can use the same address for both.

    Three refusals:

    - `422 console_access_required` on a store whose `access_tier` is
      `api_only` and that holds no balance to withdraw. That store has no
      console to sign in to, so there is nothing to invite anybody to. Give
      the store a tier first (on a store of an account that buys add-ons,
      switch on its Restaurant balance or Full console add-on), then call
      this again.
    - `422 validation_failed` with `param: "email"` when the store already
      has an owner at a different address. The `message` names that owner.
      A store has one owner, and this endpoint cannot change who it is. To
      send the owner a fresh link, call it with the address the `message`
      names.
    - `422 validation_failed` with `param: "email"` when another request is
      setting up the same address for this store at the same moment. Repeat
      the call: by then the first one has finished, and yours sends the link
      again.

    Args:
        store_id (str):
        body (CreateStoreOwnerRequest): The person to invite as the store's owner.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OwnerInvitation
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateStoreOwnerRequest,
) -> Response[ErrorResponse | OwnerInvitation]:
    """Invite a store owner

     Gives the person who runs the store a login to its Listo console. We
    create the login and email them a link to choose their own password.
    The response carries the address the link went to and when it was
    sent, and never a password or a token, so there is nothing in it to
    store.

    Repeating the call is safe. The same address gets a fresh link rather
    than a second login, so a retry after a timeout does no harm, and it is
    also how you send the link again when the first one has expired.
    The link lasts seven days.

    An address that already has a Listo login somewhere else is fine. That
    person gets a separate login for this store, with its own password, and
    the account they already had is left as it was. Somebody who runs two of
    your locations can use the same address for both.

    Three refusals:

    - `422 console_access_required` on a store whose `access_tier` is
      `api_only` and that holds no balance to withdraw. That store has no
      console to sign in to, so there is nothing to invite anybody to. Give
      the store a tier first (on a store of an account that buys add-ons,
      switch on its Restaurant balance or Full console add-on), then call
      this again.
    - `422 validation_failed` with `param: "email"` when the store already
      has an owner at a different address. The `message` names that owner.
      A store has one owner, and this endpoint cannot change who it is. To
      send the owner a fresh link, call it with the address the `message`
      names.
    - `422 validation_failed` with `param: "email"` when another request is
      setting up the same address for this store at the same moment. Repeat
      the call: by then the first one has finished, and yours sends the link
      again.

    Args:
        store_id (str):
        body (CreateStoreOwnerRequest): The person to invite as the store's owner.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | OwnerInvitation]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateStoreOwnerRequest,
) -> ErrorResponse | OwnerInvitation | None:
    """Invite a store owner

     Gives the person who runs the store a login to its Listo console. We
    create the login and email them a link to choose their own password.
    The response carries the address the link went to and when it was
    sent, and never a password or a token, so there is nothing in it to
    store.

    Repeating the call is safe. The same address gets a fresh link rather
    than a second login, so a retry after a timeout does no harm, and it is
    also how you send the link again when the first one has expired.
    The link lasts seven days.

    An address that already has a Listo login somewhere else is fine. That
    person gets a separate login for this store, with its own password, and
    the account they already had is left as it was. Somebody who runs two of
    your locations can use the same address for both.

    Three refusals:

    - `422 console_access_required` on a store whose `access_tier` is
      `api_only` and that holds no balance to withdraw. That store has no
      console to sign in to, so there is nothing to invite anybody to. Give
      the store a tier first (on a store of an account that buys add-ons,
      switch on its Restaurant balance or Full console add-on), then call
      this again.
    - `422 validation_failed` with `param: "email"` when the store already
      has an owner at a different address. The `message` names that owner.
      A store has one owner, and this endpoint cannot change who it is. To
      send the owner a fresh link, call it with the address the `message`
      names.
    - `422 validation_failed` with `param: "email"` when another request is
      setting up the same address for this store at the same moment. Repeat
      the call: by then the first one has finished, and yours sends the link
      again.

    Args:
        store_id (str):
        body (CreateStoreOwnerRequest): The person to invite as the store's owner.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | OwnerInvitation
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            body=body,
        )
    ).parsed
