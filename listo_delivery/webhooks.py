"""Checking that a webhook really came from Listo.

Mirrors the server's own rule line for line (the server's signature code is the
reference, and the signature test cases shared by every SDK and the server are
the authority):

    X-Listo-Signature: t=<unix seconds>,v1=<lowercase hex hmac-sha256>

signed over ``"<t>.<raw body>"``. Use the bytes exactly as they arrived, never a
parsed and re-serialized body.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import time
from collections.abc import Iterable
from typing import Any

from .errors import ListoError, ListoSignatureError
from .events import UnknownEvent, WebhookEvent, parse_event

__all__ = ["HEADER", "TOLERANCE", "construct_event", "verify"]

HEADER = "X-Listo-Signature"
TOLERANCE = 300

# Digits and hex are spelled out: `\d` would accept non-ASCII digits.
_HEADER_FORMAT = re.compile(r"t=([0-9]+),v1=([0-9a-fA-F]+)")

# A real timestamp has ten digits. A far longer one is out of every tolerance
# anyone would set, and refusing it before int() keeps Python's own limit on
# integer size (a ValueError past 4300 digits) from escaping verify().
_MAX_TIMESTAMP_DIGITS = 20


def _to_bytes(value: str | bytes | bytearray | memoryview) -> bytes:
    if isinstance(value, str):
        return value.encode("utf-8")
    return bytes(value)


def _usable_secrets(secrets: str | bytes | Iterable[str | bytes] | None) -> list[bytes]:
    if secrets is None:
        return []
    if isinstance(secrets, (str, bytes)):
        secrets = [secrets]
    usable = []
    for secret in secrets:
        if secret is None:
            continue
        # Blank is judged on the text (Unicode whitespace, as the server does),
        # but the key stays exactly as given.
        if (secret.strip() if isinstance(secret, str) else bytes(secret).strip()) in ("", b""):
            continue
        usable.append(_to_bytes(secret))
    return usable


def verify(
    raw_body: str | bytes,
    signature_header: str | None,
    secrets: str | bytes | Iterable[str | bytes],
    tolerance: int = TOLERANCE,
    now: int | float | None = None,
) -> bool:
    """True only for a well-formed signature over ``raw_body`` made within
    ``tolerance`` seconds of ``now`` (either direction) under any of ``secrets``.

    ``secrets`` is one secret or a list (two are active during a rotation).
    Never raises on a malformed header: the answer is False.
    """
    usable = _usable_secrets(secrets)
    if not usable:
        return False
    if isinstance(signature_header, bytes):
        try:
            signature_header = signature_header.decode("ascii")
        except UnicodeDecodeError:
            return False
    if not isinstance(signature_header, str):
        return False
    match = _HEADER_FORMAT.fullmatch(signature_header)
    if match is None:
        return False
    if len(match.group(1)) > _MAX_TIMESTAMP_DIGITS:
        return False
    timestamp = int(match.group(1))
    given = match.group(2).encode("ascii")

    current = int(time.time() if now is None else now)
    if abs(current - timestamp) > int(tolerance):
        return False

    signed = str(timestamp).encode("ascii") + b"." + _to_bytes(raw_body)
    for secret in usable:
        expected = hmac.new(secret, signed, hashlib.sha256).hexdigest().encode("ascii")
        # Byte-for-byte against the lowercase digest, as the server does; an
        # uppercase signature does not match. The length check comes first so
        # compare_digest only ever sees equal-length values.
        if len(expected) == len(given) and hmac.compare_digest(expected, given):
            return True
    return False


def construct_event(
    raw_body: str | bytes,
    signature_header: str | None,
    secrets: str | bytes | Iterable[str | bytes],
    tolerance: int = TOLERANCE,
    now: int | float | None = None,
) -> WebhookEvent | UnknownEvent:
    """Verify the signature, then parse the body into its typed event.

    Raises ListoSignatureError when the signature is not valid. An event type
    this version does not know comes back as an UnknownEvent.
    """
    if not verify(raw_body, signature_header, secrets, tolerance, now):
        raise ListoSignatureError()
    try:
        payload: Any = json.loads(_to_bytes(raw_body))
    except ValueError as error:
        raise ListoError(
            "The signed webhook body is not valid JSON.", code="invalid_payload"
        ) from error
    return parse_event(payload)
