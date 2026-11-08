# Generated from Listo's API definition. Do not edit.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ._generated.models import (
    Balance,
    CancelDeliveryRequest,
    CardOnboardingLink,
    CardStatus,
    ConnectRequest,
    CreateConnectRequestRequest,
    CreateConnectionRequest,
    CreateDeliveryRequest,
    CreateQuoteRequest,
    CreateStoreOwnerRequest,
    CreateStoreRequest,
    CreateWithdrawalRequest,
    Delivery,
    DeliveryList,
    EventList,
    LedgerEntryList,
    OwnerInvitation,
    Ping,
    Quote,
    RefundDeliveryRequest,
    RequestLogDetail,
    RequestLogList,
    RescheduleDeliveryRequest,
    SendTestWebhookRequest,
    Store,
    StoreBalance,
    StoreList,
    UpdateStoreRequest,
    WebhookDeliveryList,
    Withdrawal,
    WithdrawalList,
)
from ._events import WebhookEvent
from ._operation import Operation, Resource
from .events import UnknownEvent, parse_event_page, parse_event_response

OPERATIONS: dict[str, Operation] = {
    "cancelDelivery": Operation(
        operation_id="cancelDelivery",
        method="POST",
        path="/v1/deliveries/{delivery_id}/cancellations",
        path_params=("delivery_id",),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=Delivery.from_dict,
    ),
    "cancelStorePlan": Operation(
        operation_id="cancelStorePlan",
        method="POST",
        path="/v1/stores/{store_id}/plan_cancellation",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=True,
        parse=Store.from_dict,
    ),
    "createCardOnboarding": Operation(
        operation_id="createCardOnboarding",
        method="POST",
        path="/v1/stripe_onboarding",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=CardOnboardingLink.from_dict,
    ),
    "createConnectRequest": Operation(
        operation_id="createConnectRequest",
        method="POST",
        path="/v1/connect_requests",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=ConnectRequest.from_dict,
    ),
    "createConnection": Operation(
        operation_id="createConnection",
        method="POST",
        path="/v1/connections",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=Store.from_dict,
    ),
    "createDelivery": Operation(
        operation_id="createDelivery",
        method="POST",
        path="/v1/deliveries",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=True,
        parse=Delivery.from_dict,
    ),
    "createQuote": Operation(
        operation_id="createQuote",
        method="POST",
        path="/v1/quotes",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=Quote.from_dict,
    ),
    "createStore": Operation(
        operation_id="createStore",
        method="POST",
        path="/v1/stores",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=True,
        parse=Store.from_dict,
    ),
    "createStoreCardOnboarding": Operation(
        operation_id="createStoreCardOnboarding",
        method="POST",
        path="/v1/stores/{store_id}/stripe_onboarding",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=CardOnboardingLink.from_dict,
    ),
    "createStoreOwner": Operation(
        operation_id="createStoreOwner",
        method="POST",
        path="/v1/stores/{store_id}/owner",
        path_params=("store_id",),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=OwnerInvitation.from_dict,
    ),
    "createWithdrawal": Operation(
        operation_id="createWithdrawal",
        method="POST",
        path="/v1/withdrawals",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=Withdrawal.from_dict,
    ),
    "getBalance": Operation(
        operation_id="getBalance",
        method="GET",
        path="/v1/balance",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Balance.from_dict,
    ),
    "getCardStatus": Operation(
        operation_id="getCardStatus",
        method="GET",
        path="/v1/stripe_status",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=CardStatus.from_dict,
    ),
    "getDelivery": Operation(
        operation_id="getDelivery",
        method="GET",
        path="/v1/deliveries/{id}",
        path_params=("id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Delivery.from_dict,
    ),
    "getEvent": Operation(
        operation_id="getEvent",
        method="GET",
        path="/v1/events/{id}",
        path_params=("id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=parse_event_response,
    ),
    "getRequestLog": Operation(
        operation_id="getRequestLog",
        method="GET",
        path="/v1/request_logs/{id}",
        path_params=("id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=RequestLogDetail.from_dict,
    ),
    "getStore": Operation(
        operation_id="getStore",
        method="GET",
        path="/v1/stores/{id}",
        path_params=("id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Store.from_dict,
    ),
    "getStoreBalance": Operation(
        operation_id="getStoreBalance",
        method="GET",
        path="/v1/stores/{store_id}/balance",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=StoreBalance.from_dict,
    ),
    "getStoreCardStatus": Operation(
        operation_id="getStoreCardStatus",
        method="GET",
        path="/v1/stores/{store_id}/stripe_status",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=CardStatus.from_dict,
    ),
    "getWithdrawal": Operation(
        operation_id="getWithdrawal",
        method="GET",
        path="/v1/withdrawals/{id}",
        path_params=("id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Withdrawal.from_dict,
    ),
    "listDeliveries": Operation(
        operation_id="listDeliveries",
        method="GET",
        path="/v1/deliveries",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=DeliveryList.from_dict,
    ),
    "listEvents": Operation(
        operation_id="listEvents",
        method="GET",
        path="/v1/events",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=parse_event_page(EventList),
    ),
    "listLedgerEntries": Operation(
        operation_id="listLedgerEntries",
        method="GET",
        path="/v1/ledger",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=LedgerEntryList.from_dict,
    ),
    "listRequestLogs": Operation(
        operation_id="listRequestLogs",
        method="GET",
        path="/v1/request_logs",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=RequestLogList.from_dict,
    ),
    "listStoreLedgerEntries": Operation(
        operation_id="listStoreLedgerEntries",
        method="GET",
        path="/v1/stores/{store_id}/ledger",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=LedgerEntryList.from_dict,
    ),
    "listStores": Operation(
        operation_id="listStores",
        method="GET",
        path="/v1/stores",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=StoreList.from_dict,
    ),
    "listWebhookDeliveries": Operation(
        operation_id="listWebhookDeliveries",
        method="GET",
        path="/v1/webhook_deliveries",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=WebhookDeliveryList.from_dict,
    ),
    "listWithdrawals": Operation(
        operation_id="listWithdrawals",
        method="GET",
        path="/v1/withdrawals",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=WithdrawalList.from_dict,
    ),
    "ping": Operation(
        operation_id="ping",
        method="GET",
        path="/v1/ping",
        path_params=(),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Ping.from_dict,
    ),
    "reactivateStorePlan": Operation(
        operation_id="reactivateStorePlan",
        method="POST",
        path="/v1/stores/{store_id}/plan",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=True,
        parse=Store.from_dict,
    ),
    "refundDelivery": Operation(
        operation_id="refundDelivery",
        method="POST",
        path="/v1/deliveries/{delivery_id}/refunds",
        path_params=("delivery_id",),
        has_body=True,
        body_required=False,
        idempotent=True,
        parse=Delivery.from_dict,
    ),
    "rescheduleDelivery": Operation(
        operation_id="rescheduleDelivery",
        method="PATCH",
        path="/v1/deliveries/{id}",
        path_params=("id",),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=Delivery.from_dict,
    ),
    "resendEvent": Operation(
        operation_id="resendEvent",
        method="POST",
        path="/v1/events/{event_id}/resend",
        path_params=("event_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=parse_event_response,
    ),
    "retryDelivery": Operation(
        operation_id="retryDelivery",
        method="POST",
        path="/v1/deliveries/{delivery_id}/retries",
        path_params=("delivery_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Delivery.from_dict,
    ),
    "sendTestWebhook": Operation(
        operation_id="sendTestWebhook",
        method="POST",
        path="/v1/test_webhooks",
        path_params=(),
        has_body=True,
        body_required=True,
        idempotent=False,
        parse=parse_event_response,
    ),
    "undoStorePlanCancellation": Operation(
        operation_id="undoStorePlanCancellation",
        method="DELETE",
        path="/v1/stores/{store_id}/plan_cancellation",
        path_params=("store_id",),
        has_body=False,
        body_required=False,
        idempotent=False,
        parse=Store.from_dict,
    ),
    "updateStore": Operation(
        operation_id="updateStore",
        method="PATCH",
        path="/v1/stores/{id}",
        path_params=("id",),
        has_body=True,
        body_required=False,
        idempotent=False,
        parse=Store.from_dict,
    ),
}


class BalanceResource(Resource):
    """Operations under ``client.balance``."""

    def retrieve(self) -> Balance:
        """Read your prepaid balance (``GET /v1/balance``)."""
        return self._client._execute(OPERATIONS["getBalance"], (), None, None, None)

    def retrieve_for_store(self, store_id: str) -> StoreBalance:
        """Read a store's balance (``GET /v1/stores/{store_id}/balance``)."""
        return self._client._execute(
            OPERATIONS["getStoreBalance"], (store_id,), None, None, None
        )


class CardOnboardingResource(Resource):
    """Operations under ``client.card_onboarding``."""

    def create(self) -> CardOnboardingLink:
        """Start card onboarding for your company (``POST /v1/stripe_onboarding``)."""
        return self._client._execute(
            OPERATIONS["createCardOnboarding"], (), None, None, None
        )

    def create_for_store(self, store_id: str) -> CardOnboardingLink:
        """Start card onboarding for a store (``POST /v1/stores/{store_id}/stripe_onboarding``)."""
        return self._client._execute(
            OPERATIONS["createStoreCardOnboarding"], (store_id,), None, None, None
        )

    def status(self) -> CardStatus:
        """Read your company's card readiness (``GET /v1/stripe_status``)."""
        return self._client._execute(OPERATIONS["getCardStatus"], (), None, None, None)

    def status_for_store(self, store_id: str) -> CardStatus:
        """Read a store's card readiness (``GET /v1/stores/{store_id}/stripe_status``)."""
        return self._client._execute(
            OPERATIONS["getStoreCardStatus"], (store_id,), None, None, None
        )


class ConnectRequestsResource(Resource):
    """Operations under ``client.connect_requests``."""

    def create(
        self, body: CreateConnectRequestRequest | Mapping[str, Any]
    ) -> ConnectRequest:
        """Ask a restaurant to connect its account (``POST /v1/connect_requests``)."""
        return self._client._execute(
            OPERATIONS["createConnectRequest"], (), body, None, None
        )


class ConnectionsResource(Resource):
    """Operations under ``client.connections``."""

    def create(self, body: CreateConnectionRequest | Mapping[str, Any]) -> Store:
        """Exchange an approval for the store (``POST /v1/connections``)."""
        return self._client._execute(
            OPERATIONS["createConnection"], (), body, None, None
        )


class DeliveriesResource(Resource):
    """Operations under ``client.deliveries``."""

    def cancel(
        self, delivery_id: str, body: CancelDeliveryRequest | Mapping[str, Any]
    ) -> Delivery:
        """Cancel a delivery (``POST /v1/deliveries/{delivery_id}/cancellations``)."""
        return self._client._execute(
            OPERATIONS["cancelDelivery"], (delivery_id,), body, None, None
        )

    def create(
        self,
        body: CreateDeliveryRequest | Mapping[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> Delivery:
        """Create a delivery (``POST /v1/deliveries``)."""
        return self._client._execute(
            OPERATIONS["createDelivery"], (), body, None, idempotency_key
        )

    def list(self, query: Mapping[str, Any] | None = None) -> DeliveryList:
        """List deliveries (``GET /v1/deliveries``)."""
        return self._client._execute(
            OPERATIONS["listDeliveries"], (), None, query, None
        )

    def refund(
        self,
        delivery_id: str,
        body: RefundDeliveryRequest | Mapping[str, Any] | None = None,
        *,
        idempotency_key: str | None = None,
    ) -> Delivery:
        """Refund a delivery (``POST /v1/deliveries/{delivery_id}/refunds``)."""
        return self._client._execute(
            OPERATIONS["refundDelivery"], (delivery_id,), body, None, idempotency_key
        )

    def reschedule(
        self, id: str, body: RescheduleDeliveryRequest | Mapping[str, Any]
    ) -> Delivery:
        """Update a delivery (``PATCH /v1/deliveries/{id}``)."""
        return self._client._execute(
            OPERATIONS["rescheduleDelivery"], (id,), body, None, None
        )

    def retrieve(self, id: str) -> Delivery:
        """Fetch a delivery (``GET /v1/deliveries/{id}``)."""
        return self._client._execute(OPERATIONS["getDelivery"], (id,), None, None, None)

    def retry(self, delivery_id: str) -> Delivery:
        """Retry a failed dispatch (``POST /v1/deliveries/{delivery_id}/retries``)."""
        return self._client._execute(
            OPERATIONS["retryDelivery"], (delivery_id,), None, None, None
        )


class EventsResource(Resource):
    """Operations under ``client.events``."""

    def list(self, query: Mapping[str, Any] | None = None) -> EventList:
        """List your webhook events (``GET /v1/events``)."""
        return self._client._execute(OPERATIONS["listEvents"], (), None, query, None)

    def resend(self, event_id: str) -> WebhookEvent | UnknownEvent:
        """Send a webhook event again (``POST /v1/events/{event_id}/resend``)."""
        return self._client._execute(
            OPERATIONS["resendEvent"], (event_id,), None, None, None
        )

    def retrieve(self, id: str) -> WebhookEvent | UnknownEvent:
        """Retrieve a webhook event (``GET /v1/events/{id}``)."""
        return self._client._execute(OPERATIONS["getEvent"], (id,), None, None, None)


class LedgerResource(Resource):
    """Operations under ``client.ledger``."""

    def list(self, query: Mapping[str, Any] | None = None) -> LedgerEntryList:
        """List your ledger entries (``GET /v1/ledger``)."""
        return self._client._execute(
            OPERATIONS["listLedgerEntries"], (), None, query, None
        )

    def list_for_store(
        self, store_id: str, query: Mapping[str, Any] | None = None
    ) -> LedgerEntryList:
        """List a store's ledger entries (``GET /v1/stores/{store_id}/ledger``)."""
        return self._client._execute(
            OPERATIONS["listStoreLedgerEntries"], (store_id,), None, query, None
        )


class QuotesResource(Resource):
    """Operations under ``client.quotes``."""

    def create(self, body: CreateQuoteRequest | Mapping[str, Any]) -> Quote:
        """Price a delivery (``POST /v1/quotes``)."""
        return self._client._execute(OPERATIONS["createQuote"], (), body, None, None)


class RequestLogsResource(Resource):
    """Operations under ``client.request_logs``."""

    def list(self, query: Mapping[str, Any] | None = None) -> RequestLogList:
        """List your request log (``GET /v1/request_logs``)."""
        return self._client._execute(
            OPERATIONS["listRequestLogs"], (), None, query, None
        )

    def retrieve(self, id: str) -> RequestLogDetail:
        """Retrieve a request log entry (``GET /v1/request_logs/{id}``)."""
        return self._client._execute(
            OPERATIONS["getRequestLog"], (id,), None, None, None
        )


class StoresResource(Resource):
    """Operations under ``client.stores``."""

    def cancel_plan(
        self, store_id: str, *, idempotency_key: str | None = None
    ) -> Store:
        """Cancel a store's plan (``POST /v1/stores/{store_id}/plan_cancellation``)."""
        return self._client._execute(
            OPERATIONS["cancelStorePlan"], (store_id,), None, None, idempotency_key
        )

    def create(
        self,
        body: CreateStoreRequest | Mapping[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> Store:
        """Create a store (``POST /v1/stores``)."""
        return self._client._execute(
            OPERATIONS["createStore"], (), body, None, idempotency_key
        )

    def create_owner(
        self, store_id: str, body: CreateStoreOwnerRequest | Mapping[str, Any]
    ) -> OwnerInvitation:
        """Invite a store owner (``POST /v1/stores/{store_id}/owner``)."""
        return self._client._execute(
            OPERATIONS["createStoreOwner"], (store_id,), body, None, None
        )

    def list(self, query: Mapping[str, Any] | None = None) -> StoreList:
        """List your stores (``GET /v1/stores``)."""
        return self._client._execute(OPERATIONS["listStores"], (), None, query, None)

    def reactivate_plan(
        self, store_id: str, *, idempotency_key: str | None = None
    ) -> Store:
        """Reactivate a store's plan (``POST /v1/stores/{store_id}/plan``)."""
        return self._client._execute(
            OPERATIONS["reactivateStorePlan"], (store_id,), None, None, idempotency_key
        )

    def retrieve(self, id: str) -> Store:
        """Fetch a store (``GET /v1/stores/{id}``)."""
        return self._client._execute(OPERATIONS["getStore"], (id,), None, None, None)

    def undo_plan_cancellation(self, store_id: str) -> Store:
        """Undo a store's plan cancellation (``DELETE /v1/stores/{store_id}/plan_cancellation``)."""
        return self._client._execute(
            OPERATIONS["undoStorePlanCancellation"], (store_id,), None, None, None
        )

    def update(
        self, id: str, body: UpdateStoreRequest | Mapping[str, Any] | None = None
    ) -> Store:
        """Update a store (``PATCH /v1/stores/{id}``)."""
        return self._client._execute(OPERATIONS["updateStore"], (id,), body, None, None)


class WebhooksResource(Resource):
    """Operations under ``client.webhooks``."""

    def list_deliveries(
        self, query: Mapping[str, Any] | None = None
    ) -> WebhookDeliveryList:
        """List webhook delivery attempts (``GET /v1/webhook_deliveries``)."""
        return self._client._execute(
            OPERATIONS["listWebhookDeliveries"], (), None, query, None
        )

    def send_test(
        self, body: SendTestWebhookRequest | Mapping[str, Any]
    ) -> WebhookEvent | UnknownEvent:
        """Send a test webhook (``POST /v1/test_webhooks``)."""
        return self._client._execute(
            OPERATIONS["sendTestWebhook"], (), body, None, None
        )


class WithdrawalsResource(Resource):
    """Operations under ``client.withdrawals``."""

    def create(self, body: CreateWithdrawalRequest | Mapping[str, Any]) -> Withdrawal:
        """Request a withdrawal (``POST /v1/withdrawals``)."""
        return self._client._execute(
            OPERATIONS["createWithdrawal"], (), body, None, None
        )

    def list(self, query: Mapping[str, Any] | None = None) -> WithdrawalList:
        """List your withdrawals (``GET /v1/withdrawals``)."""
        return self._client._execute(
            OPERATIONS["listWithdrawals"], (), None, query, None
        )

    def retrieve(self, id: str) -> Withdrawal:
        """Fetch a withdrawal (``GET /v1/withdrawals/{id}``)."""
        return self._client._execute(
            OPERATIONS["getWithdrawal"], (id,), None, None, None
        )


class RootOperations:
    """Operations that live on the client itself."""

    def ping(self) -> Ping:
        """Check that your API key works (``GET /v1/ping``)."""
        return self._execute(OPERATIONS["ping"], (), None, None, None)


RESOURCES: dict[str, type[Resource]] = {
    "balance": BalanceResource,
    "card_onboarding": CardOnboardingResource,
    "connect_requests": ConnectRequestsResource,
    "connections": ConnectionsResource,
    "deliveries": DeliveriesResource,
    "events": EventsResource,
    "ledger": LedgerResource,
    "quotes": QuotesResource,
    "request_logs": RequestLogsResource,
    "stores": StoresResource,
    "webhooks": WebhooksResource,
    "withdrawals": WithdrawalsResource,
}
