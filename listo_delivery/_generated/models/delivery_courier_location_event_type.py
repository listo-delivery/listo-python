from enum import StrEnum


# A discriminator (an event's `type`) stays strict, because the generated union
# tells its members apart by which one accepts the value.
class DeliveryCourierLocationEventType(StrEnum):
    DELIVERY_COURIER_LOCATION = "delivery.courier_location"

    def __str__(self) -> str:
        return str(self.value)
