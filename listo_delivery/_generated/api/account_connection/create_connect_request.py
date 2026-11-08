from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_request import ConnectRequest
from ...models.create_connect_request_request import CreateConnectRequestRequest
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CreateConnectRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/connect_requests",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConnectRequest | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = ConnectRequest.from_dict(response.json())

        return response_201

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
) -> Response[ConnectRequest | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateConnectRequestRequest,
) -> Response[ConnectRequest | ErrorResponse]:
    """Ask a restaurant to connect its account

     Starts the flow that connects a restaurant's EXISTING Listo account to
    you, and returns the link to put in front of its owner.

    Send the owner's email address and one of the redirect URIs registered
    for your account. We resolve the restaurant ourselves and tell you
    nothing about it: the response is a link and a deadline, and you learn
    which account you connected only if the owner approves.

    Send them to `url`. They sign in with the Listo credentials they already
    have, see who is asking and what it grants, and either approve or
    cancel. We then send their browser back to your `redirect_uri`:

      approved  `?code=pcc_...&state=...`     exchange the code at
                `POST /v1/connections`
      cancelled `?error=access_denied&state=...`

    `state` is your own opaque value, echoed back untouched. Use it to tie
    the browser that comes back to the session that left; a redirect with no
    `state` you recognise is one you should not act on.

    The link is good for 30 minutes. Minting another is free, so treat an
    expired one as a button to render again rather than an error to handle.

    This endpoint is live-mode only. A test key gets `404`: there is no test
    version of a real restaurant's real account.

    Args:
        body (CreateConnectRequestRequest): The restaurant owner to ask, and where to send them
            back.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectRequest | ErrorResponse]
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
    body: CreateConnectRequestRequest,
) -> ConnectRequest | ErrorResponse | None:
    """Ask a restaurant to connect its account

     Starts the flow that connects a restaurant's EXISTING Listo account to
    you, and returns the link to put in front of its owner.

    Send the owner's email address and one of the redirect URIs registered
    for your account. We resolve the restaurant ourselves and tell you
    nothing about it: the response is a link and a deadline, and you learn
    which account you connected only if the owner approves.

    Send them to `url`. They sign in with the Listo credentials they already
    have, see who is asking and what it grants, and either approve or
    cancel. We then send their browser back to your `redirect_uri`:

      approved  `?code=pcc_...&state=...`     exchange the code at
                `POST /v1/connections`
      cancelled `?error=access_denied&state=...`

    `state` is your own opaque value, echoed back untouched. Use it to tie
    the browser that comes back to the session that left; a redirect with no
    `state` you recognise is one you should not act on.

    The link is good for 30 minutes. Minting another is free, so treat an
    expired one as a button to render again rather than an error to handle.

    This endpoint is live-mode only. A test key gets `404`: there is no test
    version of a real restaurant's real account.

    Args:
        body (CreateConnectRequestRequest): The restaurant owner to ask, and where to send them
            back.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectRequest | ErrorResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateConnectRequestRequest,
) -> Response[ConnectRequest | ErrorResponse]:
    """Ask a restaurant to connect its account

     Starts the flow that connects a restaurant's EXISTING Listo account to
    you, and returns the link to put in front of its owner.

    Send the owner's email address and one of the redirect URIs registered
    for your account. We resolve the restaurant ourselves and tell you
    nothing about it: the response is a link and a deadline, and you learn
    which account you connected only if the owner approves.

    Send them to `url`. They sign in with the Listo credentials they already
    have, see who is asking and what it grants, and either approve or
    cancel. We then send their browser back to your `redirect_uri`:

      approved  `?code=pcc_...&state=...`     exchange the code at
                `POST /v1/connections`
      cancelled `?error=access_denied&state=...`

    `state` is your own opaque value, echoed back untouched. Use it to tie
    the browser that comes back to the session that left; a redirect with no
    `state` you recognise is one you should not act on.

    The link is good for 30 minutes. Minting another is free, so treat an
    expired one as a button to render again rather than an error to handle.

    This endpoint is live-mode only. A test key gets `404`: there is no test
    version of a real restaurant's real account.

    Args:
        body (CreateConnectRequestRequest): The restaurant owner to ask, and where to send them
            back.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectRequest | ErrorResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateConnectRequestRequest,
) -> ConnectRequest | ErrorResponse | None:
    """Ask a restaurant to connect its account

     Starts the flow that connects a restaurant's EXISTING Listo account to
    you, and returns the link to put in front of its owner.

    Send the owner's email address and one of the redirect URIs registered
    for your account. We resolve the restaurant ourselves and tell you
    nothing about it: the response is a link and a deadline, and you learn
    which account you connected only if the owner approves.

    Send them to `url`. They sign in with the Listo credentials they already
    have, see who is asking and what it grants, and either approve or
    cancel. We then send their browser back to your `redirect_uri`:

      approved  `?code=pcc_...&state=...`     exchange the code at
                `POST /v1/connections`
      cancelled `?error=access_denied&state=...`

    `state` is your own opaque value, echoed back untouched. Use it to tie
    the browser that comes back to the session that left; a redirect with no
    `state` you recognise is one you should not act on.

    The link is good for 30 minutes. Minting another is free, so treat an
    expired one as a button to render again rather than an error to handle.

    This endpoint is live-mode only. A test key gets `404`: there is no test
    version of a real restaurant's real account.

    Args:
        body (CreateConnectRequestRequest): The restaurant owner to ask, and where to send them
            back.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectRequest | ErrorResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
