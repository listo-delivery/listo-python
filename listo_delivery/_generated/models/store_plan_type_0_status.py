from enum import StrEnum


# The API adds enum values without a version bump, and a strict enum would turn
# one new value into a parse failure for the whole response. An unknown value
# comes back as a member carrying that exact string instead.
class StorePlanType0Status(StrEnum):
    ACTIVE = "active"
    AWAITING_PAYMENT = "awaiting_payment"
    CANCELED = "canceled"
    CANCELING = "canceling"
    PAST_DUE = "past_due"

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
