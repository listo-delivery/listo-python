"""The two small types the generated resource layer is built from."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Operation:
    """One API operation, as the schema describes it."""

    operation_id: str
    method: str
    path: str
    path_params: tuple[str, ...]
    has_body: bool
    body_required: bool
    idempotent: bool
    parse: Callable[[Any], Any]


class Resource:
    """Base of every ``client.<resource>`` namespace."""

    def __init__(self, client: Any) -> None:
        self._client = client
