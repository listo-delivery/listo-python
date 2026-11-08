"""The errors this SDK raises. One class for anything the API refused."""

from __future__ import annotations

from typing import Any


class ListoError(Exception):
    """The API refused a request, or answered something this SDK cannot read.

    ``code`` is the one field to branch on. ``status`` is the HTTP status, or
    None when no response arrived. ``body`` is the parsed JSON body when there
    was one, otherwise the raw text.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str,
        status: int | None = None,
        param: str | None = None,
        retryable: bool | None = None,
        request_id: str | None = None,
        doc_url: str | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.param = param
        self.retryable = retryable
        self.request_id = request_id
        self.doc_url = doc_url
        self.body = body

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(code={self.code!r}, status={self.status!r}, "
            f"message={self.message!r})"
        )


class ListoConnectionError(ListoError):
    """No response arrived (DNS, refused connection, timeout).

    A write may or may not have happened; the SDK never retries it for you.
    Repeat it with the same idempotency key to find out.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, code="connection_error", status=None, retryable=False)


class ListoSignatureError(ListoError):
    """A webhook body did not carry a valid signature."""

    def __init__(self, message: str = "The webhook signature is not valid.") -> None:
        super().__init__(message, code="invalid_signature", status=None, retryable=False)
