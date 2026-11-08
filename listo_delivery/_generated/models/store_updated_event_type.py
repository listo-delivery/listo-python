from enum import StrEnum


# A discriminator (an event's `type`) stays strict, because the generated union
# tells its members apart by which one accepts the value.
class StoreUpdatedEventType(StrEnum):
    STORE_UPDATED = "store.updated"

    def __str__(self) -> str:
        return str(self.value)
