from enum import StrEnum


class DeliveryManifestItemSize(StrEnum):
    """
    Approximate size of item.
    """

    SMALL = 'small'
    """
    You can carry it with one hand e.g. bottle of water.
    """

    MEDIUM = 'medium'
    """
    You need a tote bag to carry it e.g. retail bag.
    """

    LARGE = 'large'
    """
    You need two hands to carry it e.g. computer monitor.
    """

    XLARGE = 'xlarge'
    """
    You need two hands to carry it e.g. 42 inch Flat Screen TV.
    """


class DeliveryBarcodeRequirementType(StrEnum):
    QR = 'QR'
    EAN13 = 'EAN13'
    CODE39 = 'CODE39'
    CODE128 = 'CODE128'
    CODE39_FULL_ASCII = 'CODE39_FULL_ASCII'


class DeliveryPincodeRequirementType(StrEnum):
    RANDOM = 'random'
    DEFAULT = 'default'
    MERCHANT_PROVIDED = 'merchant_provided'


class DeliveryUndeliverableAction(StrEnum):
    RETURN = 'return'
    """
    Once a normal delivery attempt is made and a customer is not available. This action requests the courier to return the package back to the pickup location.

    **Note:** Even if deliverable_action was set as leave at door and courier feels it is not okay then the package can be returned back to the pickup location.
    """

    DISCARD = 'discard'
    """
    Discard option will allow the courier to keep/throw away the package if they are unable to deliver the package.
    """

    LEAVE_AT_DOOR = 'leave_at_door'
    """
    Once a normal delivery attempt is made and a customer is not available. This action requests the courier to leave the package at dropoff location.

    **Note 1:** It cannot be set to leave at door when signature or PIN or ID verification requirements are applied when creating a delivery.

    **Note 2:** A photo confirmation of delivery will be automatically applied as a requirement to complete the dropoff.
    """


class DeliveryDeliverableAction(StrEnum):
    DELIVERABLE_ACTION_MEET_AT_DOOR = 'deliverable_action_meet_at_door'
    """
    Meet at door delivery. This is the default if DeliverableAction is not set.
    """

    DELIVERABLE_ACTION_LEAVE_AT_DOOR = 'deliverable_action_leave_at_door'
    """
    The “happy path” action for the courier to take on a delivery. When used, delivery action can be set to “leave at door” for a contactless delivery. Cannot leave at door when signature or ID verification requirements are applied when creating a delivery. Photo confirmation of delivery will be automatically applied as a requirement to complete drop-off.
    """
