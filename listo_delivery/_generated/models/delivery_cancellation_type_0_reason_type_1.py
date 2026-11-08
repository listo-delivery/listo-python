from enum import StrEnum


# The API adds enum values without a version bump, and a strict enum would turn
# one new value into a parse failure for the whole response. An unknown value
# comes back as a member carrying that exact string instead.
class DeliveryCancellationType0ReasonType1(StrEnum):
    CUSTOMER_CANCELED = "customer_canceled"
    ITEM_UNAVAILABLE = "item_unavailable"
    NO_LONGER_NEEDED = "no_longer_needed"
    OTHER = "other"
    STORE_CLOSED = "store_closed"
    WRONG_ADDRESS = "wrong_address"

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
