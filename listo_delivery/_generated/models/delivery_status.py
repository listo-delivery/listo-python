from enum import StrEnum


# The API adds enum values without a version bump, and a strict enum would turn
# one new value into a parse failure for the whole response. An unknown value
# comes back as a member carrying that exact string instead.
class DeliveryStatus(StrEnum):
    AWAITING_LOCATION = "awaiting_location"
    AWAITING_PAYMENT = "awaiting_payment"
    CANCELED = "canceled"
    COURIER_ASSIGNED = "courier_assigned"
    DELIVERED = "delivered"
    DISPATCHING = "dispatching"
    EN_ROUTE = "en_route"
    NO_COURIER = "no_courier"
    PICKING_UP = "picking_up"
    RETURNED = "returned"
    RETURNING = "returning"
    SCHEDULED = "scheduled"

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
