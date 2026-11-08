from enum import StrEnum


# A discriminator (an event's `type`) stays strict, because the generated union
# tells its members apart by which one accepts the value.
class DeliveryStatusChangedEventType(StrEnum):
    DELIVERY_STATUS_CHANGED = "delivery.status_changed"

    def __str__(self) -> str:
        return str(self.value)
