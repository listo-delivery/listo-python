from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.delivery_currency import DeliveryCurrency
from ..models.delivery_failure_reason_type_1 import DeliveryFailureReasonType1
from ..models.delivery_failure_reason_type_2_type_1 import (
    DeliveryFailureReasonType2Type1,
)
from ..models.delivery_failure_reason_type_3_type_1 import (
    DeliveryFailureReasonType3Type1,
)
from ..models.delivery_origin import DeliveryOrigin
from ..models.delivery_status import DeliveryStatus
from ..models.delivery_vehicle import DeliveryVehicle

if TYPE_CHECKING:
    from ..models.delivery_cancellation_type_0 import DeliveryCancellationType0
    from ..models.delivery_charges_item import DeliveryChargesItem
    from ..models.delivery_courier_type_0 import DeliveryCourierType0
    from ..models.delivery_dropoff import DeliveryDropoff
    from ..models.delivery_manifest_type_0 import DeliveryManifestType0
    from ..models.delivery_payment import DeliveryPayment
    from ..models.delivery_pickup import DeliveryPickup
    from ..models.delivery_proof_type_0 import DeliveryProofType0
    from ..models.delivery_proofs import DeliveryProofs
    from ..models.delivery_refunds_item import DeliveryRefundsItem
    from ..models.delivery_return_verification import DeliveryReturnVerification
    from ..models.delivery_verification_type_0 import DeliveryVerificationType0


T = TypeVar("T", bound="Delivery")


@_attrs_define
class Delivery:
    """The shape of a delivery: every field the object can carry, with the
    nullability each one really has. It is the response of every operation
    that answers a delivery (the create, the fetch, a list row, the
    reschedule, the cancel, the retry and the refund) and the `data` of
    every full delivery event, so ONE type holds all of them.

    Every operation returns the whole object. A field that a given call
    cannot yet have is present and null rather than missing: a create
    response has a null `courier`, because no courier has been assigned
    yet, and a reschedule only ever answers with a still-scheduled order,
    so its `delivered_at` is null.

    Money is integer centavos, timestamps are ISO-8601 in UTC, and every
    enum below is ours rather than a passthrough of anyone else's.

        Attributes:
            id (str): The delivery id, `dlv_` prefixed. Example: dlv_7hK2mQ9xR4tV6bN1cZ8sLwYe.
            external_id (None | str): Your own order reference, echoed back exactly as you sent it. Example: order-841.
            origin (DeliveryOrigin): Which lane created the delivery. `api` is one you created through
                `POST /v1/deliveries`. `console` is one the store dispatched itself
                from the Listo merchant console, which a store can do only at the
                `full` access tier. `whatsapp` is one a customer ordered from the
                store in a chat, which the store then accepted; no operator typed
                it anywhere.

                Always present, never null, and fixed for the life of the delivery.
                A console order carries a null `external_id`, but read this field
                rather than that null: the missing reference is a consequence of the
                lane, not a way of identifying it.
                 Example: api.
            code (str): The human order code the courier and our support quote. Unique per
                store, not globally, so never address an order by it.
                 Example: LS-2048.
            status (DeliveryStatus): `delivered`, `returned` and `canceled` are terminal. `no_courier` is
                a dead end you can retry or cancel. A `returned` delivery is this
                same object throughout; there is no second delivery for the return
                leg.

                `returning`: the drop-off failed and the courier is bringing the
                order back to the store; it ends in `returned`. It is NOT terminal,
                and it is where a failed delivery now spends the minutes between the
                courier giving up at the customer's door and the order actually
                arriving back. `returned` means the order is back. Treat `returning`
                as a live delivery: the courier is still moving and
                `delivery.courier_location` events keep arriving for it.

                The return charge is posted when the delivery enters `returning`,
                not when it reaches `returned`, so `charges` is already complete on
                the `returning` event.

                `awaiting_location`: an order the store took through Listo's console
                or its WhatsApp assistant, held for the drop-off location. No
                courier is requested yet. The customer confirms the location on a
                map link or by sharing it in the WhatsApp chat, or the store
                confirms it from its console. The delivery then moves to
                `scheduled` or `dispatching`; to `no_courier` when a courier
                cannot be requested for it (the location is outside where the
                store delivers, or the store itself cannot request a courier right
                now); or to `canceled` if the order is canceled or the store
                changes it to a pickup at the counter. A delivery you create
                through this API never sits in it.
            store_id (str): The `st_` id of the store the courier collects from.
            test (bool): Whether this order lives in the sandbox. Derived from the store, so
                there is no field to set: a test key can only reach test stores.
            payment (DeliveryPayment): How the customer pays, and where that got to.
            order_value_cents (int | None): The goods value you sent, untouched.
            fee_cents (int): The total delivery fee.
            business_fee_cents (int): The part of `fee_cents` charged to you.
            customer_fee_cents (int): The part of `fee_cents` charged to the customer. Always sums with
                `business_fee_cents` back to `fee_cents`.
            tip_cents (int): The courier tip you sent on this delivery, paid to the courier and
                passed on at cost with no margin taken. Deliberately OUTSIDE
                `fee_cents`, which is the delivery fee `business_fee_cents` and
                `customer_fee_cents` sum back to. 0 when you sent none, and never
                null.
            currency (DeliveryCurrency):
            quote_id (None | str): The `qt_` quote this order bound, so you can tie the price you were
                quoted to the order that spent it. Null when the order was priced
                inline instead.
            pickup (DeliveryPickup): Where the courier collects, snapshotted at create, so a historical
                order keeps reporting where the courier actually went even after the
                store is renamed or moved.
            dropoff (DeliveryDropoff): Where the courier delivers, echoed back as you sent it.
            manifest (DeliveryManifestType0 | None): The descriptive item list you sent, for the courier. Money never
                comes from it, with one exception: an item sized `xlarge` makes the
                trip a car. Null when you sent none.
            vehicle (DeliveryVehicle): What the trip was priced and dispatched as: `car` when you asked for
                one or when an item was sized `xlarge`, `moto` otherwise. A car's
                surcharge is inside `fee_cents`. Always present, never null, and
                fixed for the life of the delivery.

                Not the vehicle that arrived. That is `courier.vehicle_type`, which
                can be a car on a `moto` trip without the fee changing.
                 Example: moto.
            courier (DeliveryCourierType0 | None): Null until a courier is assigned, and then FROZEN: a terminal
                delivery keeps reporting who carried it.
            pickup_eta_at (datetime.datetime | None): When the courier is expected at the store. Absolute, so you compute
                your own countdown; a countdown computed here is stale before you
                read it.
            dropoff_eta_at (datetime.datetime | None): When the courier is expected at the customer. Null until there is
                an estimate, and null again once the drop-off has failed
                (`returning`, `returned`): the courier is then bringing the order
                back to the store, there is no arrival at the customer left to
                describe, and the time it gets back to the store is never published
                here.
            tracking_url (None | str): The branded live tracking page for the customer: the map, the
                courier, the delivery code and what is owed at the door. Null when
                there is no page to point at, so you never relay a dead link.

                There is a page from the moment the order is dispatched, including
                the whole window before a courier is assigned, and for 48 hours
                after the order is delivered, canceled or returned. It is null while
                an order is still held awaiting payment or awaiting a confirmed
                drop-off pin, and null again once that 48 hours has passed.
                 Example: https://app.listo.delivery/t/abc123.
            verification (DeliveryVerificationType0 | None): Present only when the order carries a dropoff PIN: when you
                asked
                for one (`verification.dropoff_pincode` on the create), or when
                Listo requires a PIN on every delivery of this store's account, in
                which case it is present even though you did not ask. `pincode` is
                null until the order is actually dispatched, which is when the code
                is minted.
            return_verification (DeliveryReturnVerification): The return code (código de devolución). When an order cannot
                be
                delivered and the courier brings it back to the store, the courier
                must be given this code at the store to hand the order over; without
                it the return cannot be completed. `pincode` is a 4-digit string
                while the delivery is `returning`, and null in every other state
                (before the return, and once it is `returned`). The object is
                always present, so this field never needs a presence check. It
                arrives in `delivery.status_changed` (the move into `returning`) and
                in `delivery.updated`, which carry the whole object. A new attempt
                (a retry) gets its own code. Show it to the store, and never to the
                customer.
            proof (DeliveryProofType0 | None): Proof of delivery. Null unless we hold some, and each field is null
                when that piece is missing; a photo with no signature is normal. The
                URLs are Listo's own signed links to the stored copy and are valid
                for 24 hours from the response (or webhook) that carried them:
                fetch `GET /v1/deliveries/{id}` again for a fresh link, or keep a
                copy. **A URL is null until Listo has its own copy of the image**
                (a few seconds after the courier takes it); the copy's arrival is
                announced by a `delivery.updated` webhook that carries the link.
                It may come from a delivery attempt that failed at the
                door, so it is not by itself proof that the order was handed over:
                `proofs.dropoff.delivered` says which. Prefer `proofs`, which keeps
                each moment of the trip apart.
            proofs (DeliveryProofs): The evidence the trip left, one entry per moment. Each moment is
                null until it happens (nothing has been captured for it yet), so
                this object is always present with its three keys. A photo or
                signature link is Listo's own signed link to the stored copy, and
                **it is null until Listo holds that copy** (a few seconds after the
                courier takes the photo): the rest of the moment, the signer, the
                time and the distance, is there from the start, and when the copy
                lands a `delivery.updated` webhook carries the link. **Each link is
                valid for 24 hours** from the response (or webhook) that carried
                it: it is a short-lived signed link, never a permanent one. A
                partner that needs the image later fetches
                `GET /v1/deliveries/{id}` again for a fresh link, or keeps a copy.
            cancellation (DeliveryCancellationType0 | None): Who called the order off, and why. Null on an order that was
                not cancelled.
            failure_reason (DeliveryFailureReasonType1 | DeliveryFailureReasonType2Type1 | DeliveryFailureReasonType3Type1 |
                None): Why a dispatch failed, bucketed by whose side the problem is on, so
                you can act on it rather than just retry blindly.
                `no_couriers_available` is the retriable one.
                `delivery_failed` is the honest catch-all. Null unless a failure was
                recorded.
            charges (list[DeliveryChargesItem]): What a trip that was driven but wasted was billed at: the delivery
                fee for each leg driven, less your own store markup. Empty on
                almost every delivery, and never null.

                **This amount changed on 2026-08-29.** It used to be what the
                wasted trip cost Listo, so expect larger values on the same orders
                from that date onward. The field itself is unchanged.

                Always present on a delivery object, so treat an absent `charges`
                as impossible rather than as "no charges". It is in this schema's
                `required` list for that reason.

                A charge can arrive on the delivery's final
                `delivery.status_changed` or, when the cost settles afterwards, on
                a later `delivery.updated`. You cannot assume which, so read this
                on both: billing the moment a delivery reaches its terminal status
                bills short on every order whose cost landed late.

                The same movement appears on `GET /v1/ledger` as a signed row, so
                it reads negative there while `amount_cents` here is positive.
            refunds (list[DeliveryRefundsItem]): Every time money went back to the customer on this order, newest
                first. Empty on an order that has never been refunded, and never
                null.

                Always present on a delivery object, so treat an absent `refunds`
                as impossible rather than as "no refunds". It is in this schema's
                `required` list for that reason, exactly as `charges` above is.

                It is a LIST because refunds repeat: a partial refund is followed
                by another refund, each with its own amount, its own reason and its
                own outcome. Every refund we can see is here whoever made it, which
                is what makes the list worth reconciling against. The connected
                account belongs to the merchant of record, which can refund a charge
                on it without going through us at all; those arrive as
                `requested_via: external`, and a list that showed only the refunds
                you asked for would silently disagree with this order's own
                `payment.status`.

                A refund rides `delivery.updated`, never an event of its own.
            refunded_cents (int): The sum of the SUCCEEDED refunds above, in Mexican peso cents. 0,
                never null, on an order nothing has gone back on. A `pending` refund
                is not counted, because the money has not moved and may yet be
                refused.

                Published rather than left for you to compute, because the array
                cannot always be summed correctly: a refund of the remaining balance
                carries no `amount_cents` until it is confirmed, so adding the
                list up counts it as zero and reads the whole charge as still
                refundable. We take that case pessimistically instead, as having
                taken the entire remaining balance, because guessing low ends in
                refunding a customer twice.
            refundable_cents (int): What a further refund could still return: what the customer paid
                (`order_value_cents` plus `customer_fee_cents`, which IS the charge)
                minus `refunded_cents`, floored at zero. 0, never null.

                0 on any order with no collected card payment behind it, whatever
                its value. Cash never touched our rails, a prepaid order's customer
                is yours and we hold nothing of theirs, and an order still awaiting
                payment was never charged, so there is nothing on any of them a
                refund could return.

                This is the ceiling `POST /v1/deliveries/{id}/refunds` refuses an
                `amount_cents` against, so read it before you call rather than
                discovering the bound from a `refund_amount_too_large`.
            support_reference (None | str): A short handle to quote when you escalate an order to us. Null until
                the order reaches dispatch.
                 Example: 2080F.
            pickup_ready_at (datetime.datetime | None): The scheduled pickup time you asked for. Null on a dispatch-now
                order.
            requested_at (datetime.datetime | None):
            courier_assigned_at (datetime.datetime | None): When a courier was first observed on the current attempt.
                Honestly
                an observation rather than an assignment clock, because no
                assignment time is published to us. Null on an attempt that never
                had one.
            picked_up_at (datetime.datetime | None):
            delivered_at (datetime.datetime | None):
            canceled_at (datetime.datetime | None):
            returned_at (datetime.datetime | None):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
    """

    id: str
    external_id: None | str
    origin: DeliveryOrigin
    code: str
    status: DeliveryStatus
    store_id: str
    test: bool
    payment: DeliveryPayment
    order_value_cents: int | None
    fee_cents: int
    business_fee_cents: int
    customer_fee_cents: int
    tip_cents: int
    currency: DeliveryCurrency
    quote_id: None | str
    pickup: DeliveryPickup
    dropoff: DeliveryDropoff
    manifest: DeliveryManifestType0 | None
    vehicle: DeliveryVehicle
    courier: DeliveryCourierType0 | None
    pickup_eta_at: datetime.datetime | None
    dropoff_eta_at: datetime.datetime | None
    tracking_url: None | str
    verification: DeliveryVerificationType0 | None
    return_verification: DeliveryReturnVerification
    proof: DeliveryProofType0 | None
    proofs: DeliveryProofs
    cancellation: DeliveryCancellationType0 | None
    failure_reason: (
        DeliveryFailureReasonType1
        | DeliveryFailureReasonType2Type1
        | DeliveryFailureReasonType3Type1
        | None
    )
    charges: list[DeliveryChargesItem]
    refunds: list[DeliveryRefundsItem]
    refunded_cents: int
    refundable_cents: int
    support_reference: None | str
    pickup_ready_at: datetime.datetime | None
    requested_at: datetime.datetime | None
    courier_assigned_at: datetime.datetime | None
    picked_up_at: datetime.datetime | None
    delivered_at: datetime.datetime | None
    canceled_at: datetime.datetime | None
    returned_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.delivery_cancellation_type_0 import DeliveryCancellationType0
        from ..models.delivery_courier_type_0 import DeliveryCourierType0
        from ..models.delivery_manifest_type_0 import DeliveryManifestType0
        from ..models.delivery_proof_type_0 import DeliveryProofType0
        from ..models.delivery_verification_type_0 import DeliveryVerificationType0

        id = self.id

        external_id: None | str
        external_id = self.external_id

        origin = self.origin.value

        code = self.code

        status = self.status.value

        store_id = self.store_id

        test = self.test

        payment = self.payment.to_dict()

        order_value_cents: int | None
        order_value_cents = self.order_value_cents

        fee_cents = self.fee_cents

        business_fee_cents = self.business_fee_cents

        customer_fee_cents = self.customer_fee_cents

        tip_cents = self.tip_cents

        currency = self.currency.value

        quote_id: None | str
        quote_id = self.quote_id

        pickup = self.pickup.to_dict()

        dropoff = self.dropoff.to_dict()

        manifest: dict[str, Any] | None
        if isinstance(self.manifest, DeliveryManifestType0):
            manifest = self.manifest.to_dict()
        else:
            manifest = self.manifest

        vehicle = self.vehicle.value

        courier: dict[str, Any] | None
        if isinstance(self.courier, DeliveryCourierType0):
            courier = self.courier.to_dict()
        else:
            courier = self.courier

        pickup_eta_at: None | str
        if isinstance(self.pickup_eta_at, datetime.datetime):
            pickup_eta_at = self.pickup_eta_at.isoformat()
        else:
            pickup_eta_at = self.pickup_eta_at

        dropoff_eta_at: None | str
        if isinstance(self.dropoff_eta_at, datetime.datetime):
            dropoff_eta_at = self.dropoff_eta_at.isoformat()
        else:
            dropoff_eta_at = self.dropoff_eta_at

        tracking_url: None | str
        tracking_url = self.tracking_url

        verification: dict[str, Any] | None
        if isinstance(self.verification, DeliveryVerificationType0):
            verification = self.verification.to_dict()
        else:
            verification = self.verification

        return_verification = self.return_verification.to_dict()

        proof: dict[str, Any] | None
        if isinstance(self.proof, DeliveryProofType0):
            proof = self.proof.to_dict()
        else:
            proof = self.proof

        proofs = self.proofs.to_dict()

        cancellation: dict[str, Any] | None
        if isinstance(self.cancellation, DeliveryCancellationType0):
            cancellation = self.cancellation.to_dict()
        else:
            cancellation = self.cancellation

        failure_reason: None | str
        if (
            isinstance(self.failure_reason, DeliveryFailureReasonType1)
            or isinstance(self.failure_reason, DeliveryFailureReasonType2Type1)
            or isinstance(self.failure_reason, DeliveryFailureReasonType3Type1)
        ):
            failure_reason = self.failure_reason.value
        else:
            failure_reason = self.failure_reason

        charges = []
        for charges_item_data in self.charges:
            charges_item = charges_item_data.to_dict()
            charges.append(charges_item)

        refunds = []
        for refunds_item_data in self.refunds:
            refunds_item = refunds_item_data.to_dict()
            refunds.append(refunds_item)

        refunded_cents = self.refunded_cents

        refundable_cents = self.refundable_cents

        support_reference: None | str
        support_reference = self.support_reference

        pickup_ready_at: None | str
        if isinstance(self.pickup_ready_at, datetime.datetime):
            pickup_ready_at = self.pickup_ready_at.isoformat()
        else:
            pickup_ready_at = self.pickup_ready_at

        requested_at: None | str
        if isinstance(self.requested_at, datetime.datetime):
            requested_at = self.requested_at.isoformat()
        else:
            requested_at = self.requested_at

        courier_assigned_at: None | str
        if isinstance(self.courier_assigned_at, datetime.datetime):
            courier_assigned_at = self.courier_assigned_at.isoformat()
        else:
            courier_assigned_at = self.courier_assigned_at

        picked_up_at: None | str
        if isinstance(self.picked_up_at, datetime.datetime):
            picked_up_at = self.picked_up_at.isoformat()
        else:
            picked_up_at = self.picked_up_at

        delivered_at: None | str
        if isinstance(self.delivered_at, datetime.datetime):
            delivered_at = self.delivered_at.isoformat()
        else:
            delivered_at = self.delivered_at

        canceled_at: None | str
        if isinstance(self.canceled_at, datetime.datetime):
            canceled_at = self.canceled_at.isoformat()
        else:
            canceled_at = self.canceled_at

        returned_at: None | str
        if isinstance(self.returned_at, datetime.datetime):
            returned_at = self.returned_at.isoformat()
        else:
            returned_at = self.returned_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "external_id": external_id,
                "origin": origin,
                "code": code,
                "status": status,
                "store_id": store_id,
                "test": test,
                "payment": payment,
                "order_value_cents": order_value_cents,
                "fee_cents": fee_cents,
                "business_fee_cents": business_fee_cents,
                "customer_fee_cents": customer_fee_cents,
                "tip_cents": tip_cents,
                "currency": currency,
                "quote_id": quote_id,
                "pickup": pickup,
                "dropoff": dropoff,
                "manifest": manifest,
                "vehicle": vehicle,
                "courier": courier,
                "pickup_eta_at": pickup_eta_at,
                "dropoff_eta_at": dropoff_eta_at,
                "tracking_url": tracking_url,
                "verification": verification,
                "return_verification": return_verification,
                "proof": proof,
                "proofs": proofs,
                "cancellation": cancellation,
                "failure_reason": failure_reason,
                "charges": charges,
                "refunds": refunds,
                "refunded_cents": refunded_cents,
                "refundable_cents": refundable_cents,
                "support_reference": support_reference,
                "pickup_ready_at": pickup_ready_at,
                "requested_at": requested_at,
                "courier_assigned_at": courier_assigned_at,
                "picked_up_at": picked_up_at,
                "delivered_at": delivered_at,
                "canceled_at": canceled_at,
                "returned_at": returned_at,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.delivery_cancellation_type_0 import DeliveryCancellationType0
        from ..models.delivery_charges_item import DeliveryChargesItem
        from ..models.delivery_courier_type_0 import DeliveryCourierType0
        from ..models.delivery_dropoff import DeliveryDropoff
        from ..models.delivery_manifest_type_0 import DeliveryManifestType0
        from ..models.delivery_payment import DeliveryPayment
        from ..models.delivery_pickup import DeliveryPickup
        from ..models.delivery_proof_type_0 import DeliveryProofType0
        from ..models.delivery_proofs import DeliveryProofs
        from ..models.delivery_refunds_item import DeliveryRefundsItem
        from ..models.delivery_return_verification import DeliveryReturnVerification
        from ..models.delivery_verification_type_0 import DeliveryVerificationType0

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("external_id"))

        origin = DeliveryOrigin(d.pop("origin"))

        code = d.pop("code")

        status = DeliveryStatus(d.pop("status"))

        store_id = d.pop("store_id")

        test = d.pop("test")

        payment = DeliveryPayment.from_dict(d.pop("payment"))

        def _parse_order_value_cents(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        order_value_cents = _parse_order_value_cents(d.pop("order_value_cents"))

        fee_cents = d.pop("fee_cents")

        business_fee_cents = d.pop("business_fee_cents")

        customer_fee_cents = d.pop("customer_fee_cents")

        tip_cents = d.pop("tip_cents")

        currency = DeliveryCurrency(d.pop("currency"))

        def _parse_quote_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        quote_id = _parse_quote_id(d.pop("quote_id"))

        pickup = DeliveryPickup.from_dict(d.pop("pickup"))

        dropoff = DeliveryDropoff.from_dict(d.pop("dropoff"))

        def _parse_manifest(data: object) -> DeliveryManifestType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                manifest_type_0 = DeliveryManifestType0.from_dict(data)

                return manifest_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryManifestType0 | None, data)

        manifest = _parse_manifest(d.pop("manifest"))

        vehicle = DeliveryVehicle(d.pop("vehicle"))

        def _parse_courier(data: object) -> DeliveryCourierType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                courier_type_0 = DeliveryCourierType0.from_dict(data)

                return courier_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryCourierType0 | None, data)

        courier = _parse_courier(d.pop("courier"))

        def _parse_pickup_eta_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pickup_eta_at_type_0 = datetime.datetime.fromisoformat(data)

                return pickup_eta_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        pickup_eta_at = _parse_pickup_eta_at(d.pop("pickup_eta_at"))

        def _parse_dropoff_eta_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                dropoff_eta_at_type_0 = datetime.datetime.fromisoformat(data)

                return dropoff_eta_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        dropoff_eta_at = _parse_dropoff_eta_at(d.pop("dropoff_eta_at"))

        def _parse_tracking_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tracking_url = _parse_tracking_url(d.pop("tracking_url"))

        def _parse_verification(data: object) -> DeliveryVerificationType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = DeliveryVerificationType0.from_dict(data)

                return verification_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryVerificationType0 | None, data)

        verification = _parse_verification(d.pop("verification"))

        return_verification = DeliveryReturnVerification.from_dict(
            d.pop("return_verification")
        )

        def _parse_proof(data: object) -> DeliveryProofType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                proof_type_0 = DeliveryProofType0.from_dict(data)

                return proof_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryProofType0 | None, data)

        proof = _parse_proof(d.pop("proof"))

        proofs = DeliveryProofs.from_dict(d.pop("proofs"))

        def _parse_cancellation(data: object) -> DeliveryCancellationType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cancellation_type_0 = DeliveryCancellationType0.from_dict(data)

                return cancellation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeliveryCancellationType0 | None, data)

        cancellation = _parse_cancellation(d.pop("cancellation"))

        def _parse_failure_reason(
            data: object,
        ) -> (
            DeliveryFailureReasonType1
            | DeliveryFailureReasonType2Type1
            | DeliveryFailureReasonType3Type1
            | None
        ):
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                failure_reason_type_1 = DeliveryFailureReasonType1(data)

                return failure_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                failure_reason_type_2_type_1 = DeliveryFailureReasonType2Type1(data)

                return failure_reason_type_2_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                failure_reason_type_3_type_1 = DeliveryFailureReasonType3Type1(data)

                return failure_reason_type_3_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                DeliveryFailureReasonType1
                | DeliveryFailureReasonType2Type1
                | DeliveryFailureReasonType3Type1
                | None,
                data,
            )

        failure_reason = _parse_failure_reason(d.pop("failure_reason"))

        charges = []
        _charges = d.pop("charges")
        for charges_item_data in _charges:
            charges_item = DeliveryChargesItem.from_dict(charges_item_data)

            charges.append(charges_item)

        refunds = []
        _refunds = d.pop("refunds")
        for refunds_item_data in _refunds:
            refunds_item = DeliveryRefundsItem.from_dict(refunds_item_data)

            refunds.append(refunds_item)

        refunded_cents = d.pop("refunded_cents")

        refundable_cents = d.pop("refundable_cents")

        def _parse_support_reference(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        support_reference = _parse_support_reference(d.pop("support_reference"))

        def _parse_pickup_ready_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pickup_ready_at_type_0 = datetime.datetime.fromisoformat(data)

                return pickup_ready_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        pickup_ready_at = _parse_pickup_ready_at(d.pop("pickup_ready_at"))

        def _parse_requested_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                requested_at_type_0 = datetime.datetime.fromisoformat(data)

                return requested_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        requested_at = _parse_requested_at(d.pop("requested_at"))

        def _parse_courier_assigned_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                courier_assigned_at_type_0 = datetime.datetime.fromisoformat(data)

                return courier_assigned_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        courier_assigned_at = _parse_courier_assigned_at(d.pop("courier_assigned_at"))

        def _parse_picked_up_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                picked_up_at_type_0 = datetime.datetime.fromisoformat(data)

                return picked_up_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        picked_up_at = _parse_picked_up_at(d.pop("picked_up_at"))

        def _parse_delivered_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                delivered_at_type_0 = datetime.datetime.fromisoformat(data)

                return delivered_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        delivered_at = _parse_delivered_at(d.pop("delivered_at"))

        def _parse_canceled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                canceled_at_type_0 = datetime.datetime.fromisoformat(data)

                return canceled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        canceled_at = _parse_canceled_at(d.pop("canceled_at"))

        def _parse_returned_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                returned_at_type_0 = datetime.datetime.fromisoformat(data)

                return returned_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        returned_at = _parse_returned_at(d.pop("returned_at"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        delivery = cls(
            id=id,
            external_id=external_id,
            origin=origin,
            code=code,
            status=status,
            store_id=store_id,
            test=test,
            payment=payment,
            order_value_cents=order_value_cents,
            fee_cents=fee_cents,
            business_fee_cents=business_fee_cents,
            customer_fee_cents=customer_fee_cents,
            tip_cents=tip_cents,
            currency=currency,
            quote_id=quote_id,
            pickup=pickup,
            dropoff=dropoff,
            manifest=manifest,
            vehicle=vehicle,
            courier=courier,
            pickup_eta_at=pickup_eta_at,
            dropoff_eta_at=dropoff_eta_at,
            tracking_url=tracking_url,
            verification=verification,
            return_verification=return_verification,
            proof=proof,
            proofs=proofs,
            cancellation=cancellation,
            failure_reason=failure_reason,
            charges=charges,
            refunds=refunds,
            refunded_cents=refunded_cents,
            refundable_cents=refundable_cents,
            support_reference=support_reference,
            pickup_ready_at=pickup_ready_at,
            requested_at=requested_at,
            courier_assigned_at=courier_assigned_at,
            picked_up_at=picked_up_at,
            delivered_at=delivered_at,
            canceled_at=canceled_at,
            returned_at=returned_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        delivery.additional_properties = d
        return delivery

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
