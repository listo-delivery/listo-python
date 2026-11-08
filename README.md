# listo-delivery (Python)

The official Python client for the [Listo Delivery API](https://docs.listo.delivery).
Models are generated from the published OpenAPI schema, so every response is a typed
object that matches the schema. Needs Python 3.11 or newer (the generated models
use `typing.Self` and `StrEnum`); its only dependencies are `httpx` and `attrs`.

## Install

```bash
pip install listo-delivery
```

## Quickstart

Quote a delivery, book it in test mode and check a webhook:

```python
import os
from listo_delivery import Listo

listo = Listo(os.environ["LISTO_API_KEY"])      # lst_test_... acts in test mode
print(listo.mode)                               # "test"

dropoff = {
    "name": "Ana",
    "phone": "+523312345678",
    "street": "Av. Vallarta 1234, Guadalajara",
}

quote = listo.quotes.create({"store_id": "st_...", "dropoff": dropoff, "order_value_cents": 25000})

delivery = listo.deliveries.create(
    {
        "store_id": "st_...",
        "quote_id": quote.id,
        "external_id": "order-1042",
        "payment_method": "prepaid",
        "order_value_cents": 25000,
        "dropoff": dropoff,
    },
    idempotency_key="order-1042",               # key it on your own order id
)
print(delivery.id, delivery.status)
```

The ids are placeholders; the schema is the reference for every field
(`listo_delivery.models.CreateQuoteRequest`, `CreateDeliveryRequest`).

Verify a webhook in your receiver (no API key needed). Pass the body exactly as
it arrived on the wire, never a parsed and re-serialized one:

```python
from listo_delivery import ListoError, webhooks
from listo_delivery.models import DeliveryStatusChangedEvent

try:
    event = webhooks.construct_event(
        raw_body,                                   # bytes or str, as received
        headers["X-Listo-Signature"],
        [os.environ["LISTO_WEBHOOK_SECRET"]],       # two secrets while rotating
    )
except ListoError:                                  # invalid_signature or invalid_payload
    ...                                             # answer 400

if isinstance(event, DeliveryStatusChangedEvent):
    print(event.data.id, event.data.status)
```

`webhooks.verify(raw_body, header, secrets)` returns a boolean instead of raising,
and both are also on the client (`listo.webhooks.verify`, `listo.webhooks.construct_event`).
The rule is the server's own: `t=<unix seconds>,v1=<lowercase hex>` signed over
`"<t>.<raw body>"` with HMAC-SHA256, a 300 second tolerance in both directions
(`tolerance=300`, `now=None` are arguments), blank secrets ignored, and `False`
rather than an exception for anything malformed. An event whose `type` this SDK
version does not know comes back as `listo_delivery.UnknownEvent` (`id`, `type`,
`type_`, `created_at`, `data`, `raw`), never as an error, and every event, known or
not, has `type_`. A known `type` whose body the models cannot read raises `ListoError`
with `code="invalid_payload"` (a delivery event must never be ignored silently).

## Calling convention

```python
listo.deliveries.retrieve(delivery_id)              # path parameters are positional
listo.deliveries.cancel(delivery_id, {"reason": "customer_canceled"})   # then the body
listo.deliveries.list({"status": "delivered"})      # or the query, for a read
listo.deliveries.create(body, idempotency_key=...)  # then keyword options
listo.ping()                                        # a few calls live on the client itself
```

Bodies and queries are plain dicts keyed by the wire names (`order_value_cents`);
a generated model (anything with `.to_dict()`) is accepted for a body too.
Responses are the generated attrs models: `delivery.status`, `delivery.to_dict()`.
A field the server adds later is kept (`delivery["new_field"]`, `to_dict()`), and an
enum value it adds later parses as a member carrying that string (every enum but an
event's own `type`, which stays strict so the event union can tell its members apart). Because `type`
and similar names are Python builtins, the generator spells those attributes with a
trailing underscore (`event.type_`). Every operation of the API is a method, named after it; the API reference at
[docs.listo.delivery](https://docs.listo.delivery) lists them all.

## Errors

Every refusal raises `listo_delivery.ListoError`, built from the API's `error`
envelope: `code` (the one field to branch on), `message`, `param`, `retryable`,
`status`, `request_id`, `doc_url` and the raw `body`.

```python
from listo_delivery import ListoConnectionError, ListoError

try:
    listo.deliveries.create(body)
except ListoConnectionError:
    ...        # no response arrived; a write may have happened, repeat it with the same idempotency key
except ListoError as error:
    if error.code == "insufficient_balance": ...
```

A body that is not the envelope (a proxy's HTML page) still raises `ListoError`, with
`code="http_<status>"`, `message="Unexpected response with status <status>"` and
`retryable` true for 429, 502, 503 and 504. `ListoConnectionError` (a subclass, code
`connection_error`, `status=None`, `retryable=False`) covers DNS, refused connections and
timeouts. A 2xx the SDK cannot read raises `code="invalid_response"` (the Python SDK checks
required fields, so a response missing one raises it). The API key is
never part of an error message.

## Idempotency

The operations whose schema declares the `Idempotency-Key` header (create and refund a
delivery, create a store, reactivate and cancel a store plan) always send it: yours when
you pass `idempotency_key=`, otherwise a fresh UUID v4 for that call, reused only by that
call's own retries. A key that is empty or only whitespace raises `ValueError`, and one
that is not a `str` raises `TypeError`, both before any request. No other operation
sends the header.

## Pagination

List calls return the page as the schema has it: `page.data`, `page.has_more` and
`page.cursor`. Pass the cursor back for the next page:

```python
cursor = None
while True:
    page = listo.deliveries.list({"cursor": cursor})
    for delivery in page.data:
        handle(delivery)
    if not page.has_more:
        break
    cursor = page.cursor
```

There is no auto-paging iterator in this SDK.

## Retries and timeouts

Nothing is retried by default. `Listo(key, max_retries=2)` retries a 429, and only a
429, after its `Retry-After` (seconds or an HTTP date; one second when missing or
unreadable; at most 60), with the same idempotency key. 5xx answers and network
errors are never retried for you. `timeout` (seconds, default 30) applies to each request.

## Options

```python
Listo(api_key, base_url=None, max_retries=0, timeout=30.0, *, http_client=None)
```

`base_url` defaults to `https://api.listo.delivery`. The key must start with `lst_test_` or
`lst_live_`, and the SDK reads no environment variables. Every request sends
`User-Agent` and `X-Listo-Client` as `listo-python/<sdk version> api/<API version>`.
Use the client as a context manager (`with Listo(key) as listo:`) or call `listo.close()`.
`http_client` takes your own `httpx.Client` (a proxy, a mock transport in your tests).

## About this repository

This code is generated from Listo's API definition. Issues and questions are
welcome in this repository. Changes are made upstream by Listo and released
here, so a pull request cannot be merged as it stands: open an issue and the
change is made at the source.
