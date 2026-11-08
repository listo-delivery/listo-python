from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_request_logs_status import ListRequestLogsStatus
from ...models.request_log_list import RequestLogList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: ListRequestLogsStatus | Unset = UNSET,
    endpoint: str | Unset = UNSET,
    request_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["endpoint"] = endpoint

    params["request_id"] = request_id

    params["created_after"] = created_after

    params["created_before"] = created_before

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/request_logs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RequestLogList | None:
    if response.status_code == 200:
        response_200 = RequestLogList.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RequestLogList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    status: ListRequestLogsStatus | Unset = UNSET,
    endpoint: str | Unset = UNSET,
    request_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[RequestLogList]:
    """List your request log

     Every call your keys made to this API, newest first, keyset-paginated
    like every list here. Use it to answer "what did my code send, and what
    did Listo say?" without asking anyone.

    A key only ever sees the calls of its own world: a live key reads live
    calls and a test key reads test calls, and neither can read the other's.

    Filter by `status` (`failed` is every answer of 400 or more),
    `endpoint`, `created_after` and `created_before`. A filter narrows the
    whole history, never only the page you are on.

    What is recorded: calls that identified a key. A call with no key or a
    wrong one is not yours and is not here, and neither is a call refused for
    rate limiting. Calls are kept indefinitely. Reading this list, one entry
    or your events or webhook deliveries is itself logged, but without
    bodies, so the log does not copy itself every time you read it.

    The list carries no bodies. `GET /v1/request_logs/{id}` returns the call
    with them.

    Args:
        status (ListRequestLogsStatus | Unset):
        endpoint (str | Unset):
        request_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestLogList]
    """

    kwargs = _get_kwargs(
        status=status,
        endpoint=endpoint,
        request_id=request_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    status: ListRequestLogsStatus | Unset = UNSET,
    endpoint: str | Unset = UNSET,
    request_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> RequestLogList | None:
    """List your request log

     Every call your keys made to this API, newest first, keyset-paginated
    like every list here. Use it to answer "what did my code send, and what
    did Listo say?" without asking anyone.

    A key only ever sees the calls of its own world: a live key reads live
    calls and a test key reads test calls, and neither can read the other's.

    Filter by `status` (`failed` is every answer of 400 or more),
    `endpoint`, `created_after` and `created_before`. A filter narrows the
    whole history, never only the page you are on.

    What is recorded: calls that identified a key. A call with no key or a
    wrong one is not yours and is not here, and neither is a call refused for
    rate limiting. Calls are kept indefinitely. Reading this list, one entry
    or your events or webhook deliveries is itself logged, but without
    bodies, so the log does not copy itself every time you read it.

    The list carries no bodies. `GET /v1/request_logs/{id}` returns the call
    with them.

    Args:
        status (ListRequestLogsStatus | Unset):
        endpoint (str | Unset):
        request_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestLogList
    """

    return sync_detailed(
        client=client,
        status=status,
        endpoint=endpoint,
        request_id=request_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    status: ListRequestLogsStatus | Unset = UNSET,
    endpoint: str | Unset = UNSET,
    request_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[RequestLogList]:
    """List your request log

     Every call your keys made to this API, newest first, keyset-paginated
    like every list here. Use it to answer "what did my code send, and what
    did Listo say?" without asking anyone.

    A key only ever sees the calls of its own world: a live key reads live
    calls and a test key reads test calls, and neither can read the other's.

    Filter by `status` (`failed` is every answer of 400 or more),
    `endpoint`, `created_after` and `created_before`. A filter narrows the
    whole history, never only the page you are on.

    What is recorded: calls that identified a key. A call with no key or a
    wrong one is not yours and is not here, and neither is a call refused for
    rate limiting. Calls are kept indefinitely. Reading this list, one entry
    or your events or webhook deliveries is itself logged, but without
    bodies, so the log does not copy itself every time you read it.

    The list carries no bodies. `GET /v1/request_logs/{id}` returns the call
    with them.

    Args:
        status (ListRequestLogsStatus | Unset):
        endpoint (str | Unset):
        request_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestLogList]
    """

    kwargs = _get_kwargs(
        status=status,
        endpoint=endpoint,
        request_id=request_id,
        created_after=created_after,
        created_before=created_before,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    status: ListRequestLogsStatus | Unset = UNSET,
    endpoint: str | Unset = UNSET,
    request_id: str | Unset = UNSET,
    created_after: str | Unset = UNSET,
    created_before: str | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> RequestLogList | None:
    """List your request log

     Every call your keys made to this API, newest first, keyset-paginated
    like every list here. Use it to answer "what did my code send, and what
    did Listo say?" without asking anyone.

    A key only ever sees the calls of its own world: a live key reads live
    calls and a test key reads test calls, and neither can read the other's.

    Filter by `status` (`failed` is every answer of 400 or more),
    `endpoint`, `created_after` and `created_before`. A filter narrows the
    whole history, never only the page you are on.

    What is recorded: calls that identified a key. A call with no key or a
    wrong one is not yours and is not here, and neither is a call refused for
    rate limiting. Calls are kept indefinitely. Reading this list, one entry
    or your events or webhook deliveries is itself logged, but without
    bodies, so the log does not copy itself every time you read it.

    The list carries no bodies. `GET /v1/request_logs/{id}` returns the call
    with them.

    Args:
        status (ListRequestLogsStatus | Unset):
        endpoint (str | Unset):
        request_id (str | Unset):
        created_after (str | Unset):
        created_before (str | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestLogList
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            endpoint=endpoint,
            request_id=request_id,
            created_after=created_after,
            created_before=created_before,
            cursor=cursor,
        )
    ).parsed
