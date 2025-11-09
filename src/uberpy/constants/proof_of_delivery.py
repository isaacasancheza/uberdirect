from enum import StrEnum


class ProofOfDeliveryType(StrEnum):
    PINCODE = 'pincode'
    PICTURE = 'picture'
    SIGNATURE = 'signature'


class ProofOfDeliveryWaypoint(StrEnum):
    RETURN = 'return'
    PICKUP = 'pickup'
    DROPOFF = 'dropoff'
