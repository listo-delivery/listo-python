from enum import StrEnum


# A discriminator (an event's `type`) stays strict, because the generated union
# tells its members apart by which one accepts the value.
class DeliveryMessageSkippedEventType(StrEnum):
    DELIVERY_MESSAGE_SKIPPED = "delivery.message_skipped"

    def __str__(self) -> str:
        return str(self.value)
