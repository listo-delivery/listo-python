# Generated from Listo's API definition. Do not edit.

from ._generated.models import (
    DeliveryCourierLocationEvent,
    DeliveryMessageSkippedEvent,
    DeliveryRatedEvent,
    DeliveryStatusChangedEvent,
    DeliveryUpdatedEvent,
    StoreConnectedEvent,
    StoreUpdatedEvent,
    WithdrawalUpdatedEvent,
)

WebhookEvent = (
    DeliveryCourierLocationEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
)

EVENT_TYPES: dict[str, type] = {
    "delivery.courier_location": DeliveryCourierLocationEvent,
    "delivery.message_skipped": DeliveryMessageSkippedEvent,
    "delivery.rated": DeliveryRatedEvent,
    "delivery.status_changed": DeliveryStatusChangedEvent,
    "delivery.updated": DeliveryUpdatedEvent,
    "store.connected": StoreConnectedEvent,
    "store.updated": StoreUpdatedEvent,
    "withdrawal.updated": WithdrawalUpdatedEvent,
}
