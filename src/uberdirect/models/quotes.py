from datetime import datetime

from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude

from uberdirect import fields
from uberdirect.models.common import StructuredAddress


class QuoteRequest(BaseModel):
    pickup_address: StructuredAddress
    """
    Pickup address details.
    """

    pickup_latitude: Latitude | None = None
    """
    Pickup latitude coordinate.
    """

    pickup_longitude: Longitude | None = None
    """
    Pickup longitude coordinate.
    """

    pickup_ready_dt: datetime | None = None
    """
    Beginning of the window when an order must be picked up. Must be less than 30 days in the future.
    """

    pickup_deadline_dt: datetime | None = None
    """
    End of the window when an order may be picked up. Must be at least 10 mins later than pickup_ready_dt and at least 20 minutes in the future from now.
    """

    pickup_phone_number: fields.PhoneNumber
    """
    Phone number for the pickup location, usually the store's contact. This number allows the courier to call before heading to the dropoff location.
    """

    dropoff_address: StructuredAddress
    """
    Dropoff address details.
    """

    dropoff_latitude: Latitude | None = None
    """
    Dropoff latitude coordinate.
    """

    dropoff_longitude: Longitude | None = None
    """
    Dropoff longitude coordinate.
    """

    dropoff_ready_dt: datetime | None = None
    """
    Beginning of the window when an order must be dropped off. Must be less than or equal to pickup_deadline_dt.
    """

    dropoff_deadline_dt: datetime | None = None
    """
    End of the window when an order must be dropped off. Must be at least 20 mins later than dropoff_ready_dt and must be greater than or equal to pickup_deadline_dt.
    """

    dropoff_phone_number: fields.PhoneNumber | None = None
    """
    Phone number for the dropoff location, usually belonging to the end-user (recipient). This number enables the courier to make calls after en route to the dropoff and before completing the trip.
    """

    manifest_total_value: fields.DecimalFromInt | None = None
    """
    Value in cents ( ¹/₁₀₀ of currency unit ) of the items in the delivery. i.e.: $10.99 => 1099.
    """

    external_store_id: str | None = None
    """
    Unique identifier used by our Partners to reference a store or location.

    **Note:** Please be aware that if you utilize external_store_id in the Create Delivery process, you MUST also include this field in your Create Quote API calls.
    """


class QuoteResponse(BaseModel):
    id: str
    """
    Unique identifier for the quote (always starts with dqt_)
    """

    kind: str
    """
    The type of object being described. Default: `delivery_quote`
    """

    created: datetime
    """
    Date/Time timestamp (RFC 3339) at which the quote was created.
    """

    expires: datetime
    """
    Date/Time timestamp (RFC 3339) after which the quote will no longer be accepted.
    """

    fee: fields.DecimalFromInt
    """
    Amount in cents (¹/₁₀₀ of currency unit) that will be charged if this delivery is created.
    """

    currency_type: str
    """
    Three-letter ISO currency code, in uppercase.
    """

    dropoff_eta: datetime
    """
    Estimated drop-off time. This value may exceed the request dropoff_deadline if the delivery window does not meet minimum requirements. Please validate the timestamps returned.
    """

    duration: datetime
    """
    Estimated minutes for this delivery to reach dropoff.    
    """

    pickup_duration: int
    """
    Estimated minutes until a courier will arrive at the pickup.
    """

    dropoff_deadline: datetime
    """
    When a delivery must be dropped off. This is the end of the dropoff window.
    """
