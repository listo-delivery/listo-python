from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_message_skipped_moment import DeliveryMessageSkippedMoment
from ..models.delivery_message_skipped_reason import DeliveryMessageSkippedReason

T = TypeVar("T", bound="DeliveryMessageSkipped")


@_attrs_define
class DeliveryMessageSkipped:
    """The body of a `delivery.message_skipped` event. Sent only for a delivery
    made in test mode, when a message to the customer was not sent: either
    because the delivery's `dropoff.phone` is not one of the team phones you
    verified on the dashboard (Settings, Test phones), or because you reached
    the 20 customer messages a day that test mode sends. The delivery itself
    carried on as usual. Correlate it with a delivery you already hold; it
    is not the delivery object and carries no phone number.

        Attributes:
            delivery_id (str): The `dlv_` id of the delivery whose message was not sent. Example:
                dlv_3kT8nQ2vLw5xZ9aB4cD7eF1g.
            moment (DeliveryMessageSkippedMoment): Which message was skipped. `courier_assigned`, `en_route`,
                `arriving`, `delivered`, `not_delivered` and `pickup_time_changed`
                are the tracking messages; `location_request` and `payment_request`
                are the links asking the customer to confirm the drop-off location or
                to pay; `dropoff_code` is the SMS with the drop-off code.
                 Example: en_route.
            reason (DeliveryMessageSkippedReason): Why it was skipped. `not_a_team_phone`: `dropoff.phone` is not one of
                the phones you verified. `daily_test_limit`: you already sent 20
                customer messages today in test mode.
                 Example: not_a_team_phone.
    """

    delivery_id: str
    moment: DeliveryMessageSkippedMoment
    reason: DeliveryMessageSkippedReason
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivery_id = self.delivery_id

        moment = self.moment.value

        reason = self.reason.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_id": delivery_id,
                "moment": moment,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        delivery_id = d.pop("delivery_id")

        moment = DeliveryMessageSkippedMoment(d.pop("moment"))

        reason = DeliveryMessageSkippedReason(d.pop("reason"))

        delivery_message_skipped = cls(
            delivery_id=delivery_id,
            moment=moment,
            reason=reason,
        )

        delivery_message_skipped.additional_properties = d
        return delivery_message_skipped

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
