from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_courier_location_event import DeliveryCourierLocationEvent
    from ..models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
    from ..models.delivery_rated_event import DeliveryRatedEvent
    from ..models.delivery_status_changed_event import DeliveryStatusChangedEvent
    from ..models.delivery_updated_event import DeliveryUpdatedEvent
    from ..models.store_connected_event import StoreConnectedEvent
    from ..models.store_updated_event import StoreUpdatedEvent
    from ..models.withdrawal_updated_event import WithdrawalUpdatedEvent


T = TypeVar("T", bound="EventList")


@_attrs_define
class EventList:
    """One page of events, newest first.

    Attributes:
        data (list[DeliveryCourierLocationEvent | DeliveryMessageSkippedEvent | DeliveryRatedEvent |
            DeliveryStatusChangedEvent | DeliveryUpdatedEvent | StoreConnectedEvent | StoreUpdatedEvent |
            WithdrawalUpdatedEvent]):
        has_more (bool): True when a further page exists.
        cursor (None | str): Pass as `cursor` to read the next page. Null on the last page.
    """

    data: list[
        DeliveryCourierLocationEvent
        | DeliveryMessageSkippedEvent
        | DeliveryRatedEvent
        | DeliveryStatusChangedEvent
        | DeliveryUpdatedEvent
        | StoreConnectedEvent
        | StoreUpdatedEvent
        | WithdrawalUpdatedEvent
    ]
    has_more: bool
    cursor: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_courier_location_event import (
            DeliveryCourierLocationEvent,
        )
        from ..models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
        from ..models.delivery_status_changed_event import DeliveryStatusChangedEvent
        from ..models.delivery_updated_event import DeliveryUpdatedEvent
        from ..models.store_connected_event import StoreConnectedEvent
        from ..models.store_updated_event import StoreUpdatedEvent
        from ..models.withdrawal_updated_event import WithdrawalUpdatedEvent

        data = []
        for data_item_data in self.data:
            data_item: dict[str, Any]
            if (
                isinstance(data_item_data, DeliveryStatusChangedEvent)
                or isinstance(data_item_data, DeliveryUpdatedEvent)
                or isinstance(data_item_data, DeliveryCourierLocationEvent)
                or isinstance(data_item_data, WithdrawalUpdatedEvent)
                or isinstance(data_item_data, StoreUpdatedEvent)
                or isinstance(data_item_data, StoreConnectedEvent)
                or isinstance(data_item_data, DeliveryMessageSkippedEvent)
            ):
                data_item = data_item_data.to_dict()
            else:
                data_item = data_item_data.to_dict()

            data.append(data_item)

        has_more = self.has_more

        cursor: None | str
        cursor = self.cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery_courier_location_event import (
            DeliveryCourierLocationEvent,
        )
        from ..models.delivery_message_skipped_event import DeliveryMessageSkippedEvent
        from ..models.delivery_rated_event import DeliveryRatedEvent
        from ..models.delivery_status_changed_event import DeliveryStatusChangedEvent
        from ..models.delivery_updated_event import DeliveryUpdatedEvent
        from ..models.store_connected_event import StoreConnectedEvent
        from ..models.store_updated_event import StoreUpdatedEvent
        from ..models.withdrawal_updated_event import WithdrawalUpdatedEvent

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:

            def _parse_data_item(
                data: object,
            ) -> (
                DeliveryCourierLocationEvent
                | DeliveryMessageSkippedEvent
                | DeliveryRatedEvent
                | DeliveryStatusChangedEvent
                | DeliveryUpdatedEvent
                | StoreConnectedEvent
                | StoreUpdatedEvent
                | WithdrawalUpdatedEvent
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_0 = (
                        DeliveryStatusChangedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_1 = (
                        DeliveryUpdatedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_2 = (
                        DeliveryCourierLocationEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_3 = (
                        WithdrawalUpdatedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_4 = (
                        StoreUpdatedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_5 = (
                        StoreConnectedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_webhook_event_type_6 = (
                        DeliveryMessageSkippedEvent.from_dict(data)
                    )

                    return componentsschemas_webhook_event_type_6
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_webhook_event_type_7 = DeliveryRatedEvent.from_dict(
                    data
                )

                return componentsschemas_webhook_event_type_7

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        def _parse_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        cursor = _parse_cursor(d.pop("cursor"))

        event_list = cls(
            data=data,
            has_more=has_more,
            cursor=cursor,
        )

        event_list.additional_properties = d
        return event_list

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
