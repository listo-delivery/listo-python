from enum import StrEnum


# The API adds enum values without a version bump, and a strict enum would turn
# one new value into a parse failure for the whole response. An unknown value
# comes back as a member carrying that exact string instead.
class DeliveryMessageSkippedMoment(StrEnum):
    ARRIVING = "arriving"
    COURIER_ASSIGNED = "courier_assigned"
    DELIVERED = "delivered"
    DROPOFF_CODE = "dropoff_code"
    EN_ROUTE = "en_route"
    LOCATION_REQUEST = "location_request"
    NOT_DELIVERED = "not_delivered"
    PAYMENT_REQUEST = "payment_request"
    PICKUP_TIME_CHANGED = "pickup_time_changed"

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
