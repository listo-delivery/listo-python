# Generated from Listo's API definition. Do not edit.

from ._generated.models import (
    DeliveryCourierLocationEvent,
    DeliveryCreatedEvent,
    DeliveryMessageSkippedEvent,
    DeliveryRatedEvent,
    DeliveryStatusChangedEvent,
    DeliveryUpdatedEvent,
    OrderStatusChangedEvent,
    StoreConnectedEvent,
    StoreUpdatedEvent,
    WithdrawalUpdatedEvent,
)

WebhookEvent = (
    DeliveryCourierLocationEvent
    | DeliveryCreatedEvent
    | DeliveryMessageSkippedEvent
    | DeliveryRatedEvent
    | DeliveryStatusChangedEvent
    | DeliveryUpdatedEvent
    | OrderStatusChangedEvent
    | StoreConnectedEvent
    | StoreUpdatedEvent
    | WithdrawalUpdatedEvent
)

EVENT_TYPES: dict[str, type] = {
    "delivery.courier_location": DeliveryCourierLocationEvent,
    "delivery.created": DeliveryCreatedEvent,
    "delivery.message_skipped": DeliveryMessageSkippedEvent,
    "delivery.rated": DeliveryRatedEvent,
    "delivery.status_changed": DeliveryStatusChangedEvent,
    "delivery.updated": DeliveryUpdatedEvent,
    "order.status_changed": OrderStatusChangedEvent,
    "store.connected": StoreConnectedEvent,
    "store.updated": StoreUpdatedEvent,
    "withdrawal.updated": WithdrawalUpdatedEvent,
}
