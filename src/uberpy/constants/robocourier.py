from enum import StrEnum


class RoboCourierMode(StrEnum):
    AUTO = 'auto'
    CUSTOM = 'custom'


class RoboCourierCancelReason(StrEnum):
    CUSTOMER_UNAVAILABLE = 'customer_unavailable'
    CUSTOMER_REJECTED_ORDER = 'customer_rejected_order'
    CANNOT_FIND_CUSTOMER_ADDRESS = 'cannot_find_customer_address'
    CANNOT_ACCESS_CUSTOMER_LOCATION = 'cannot_access_customer_location'
