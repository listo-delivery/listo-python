from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.withdrawal import Withdrawal
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/withdrawals/{id}".format(
            id=quote(str(id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Withdrawal | None:
    if response.status_code == 200:
        response_200 = Withdrawal.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Withdrawal]:
    """Fetch a withdrawal

     Fetches one withdrawal by its `wd_` id, which is how you check on one
    that has not resolved yet without waiting for its webhook.

    Once it is `paid`, `clave_de_rastreo` carries the SPEI tracking key your
    bank uses to find the deposit, so this is also the endpoint to reconcile
    a payout from if you would rather poll than handle the webhook.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Withdrawal]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Withdrawal | None:
    """Fetch a withdrawal

     Fetches one withdrawal by its `wd_` id, which is how you check on one
    that has not resolved yet without waiting for its webhook.

    Once it is `paid`, `clave_de_rastreo` carries the SPEI tracking key your
    bank uses to find the deposit, so this is also the endpoint to reconcile
    a payout from if you would rather poll than handle the webhook.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Withdrawal
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | Withdrawal]:
    """Fetch a withdrawal

     Fetches one withdrawal by its `wd_` id, which is how you check on one
    that has not resolved yet without waiting for its webhook.

    Once it is `paid`, `clave_de_rastreo` carries the SPEI tracking key your
    bank uses to find the deposit, so this is also the endpoint to reconcile
    a payout from if you would rather poll than handle the webhook.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Withdrawal]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | Withdrawal | None:
    """Fetch a withdrawal

     Fetches one withdrawal by its `wd_` id, which is how you check on one
    that has not resolved yet without waiting for its webhook.

    Once it is `paid`, `clave_de_rastreo` carries the SPEI tracking key your
    bank uses to find the deposit, so this is also the endpoint to reconcile
    a payout from if you would rather poll than handle the webhook.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Withdrawal
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
