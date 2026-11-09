from enum import StrEnum


# The API adds enum values without a version bump, and a strict enum would turn
# one new value into a parse failure for the whole response. An unknown value
# comes back as a member carrying that exact string instead.
class SendTestWebhookRequestType(StrEnum):
    DELIVERY_COURIER_LOCATION = "delivery.courier_location"
    DELIVERY_MESSAGE_SKIPPED = "delivery.message_skipped"
    DELIVERY_RATED = "delivery.rated"
    DELIVERY_STATUS_CHANGED = "delivery.status_changed"
    DELIVERY_UPDATED = "delivery.updated"
    STORE_CONNECTED = "store.connected"
    STORE_UPDATED = "store.updated"
    WITHDRAWAL_UPDATED = "withdrawal.updated"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object):
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value
        member._value_ = value
        return member
