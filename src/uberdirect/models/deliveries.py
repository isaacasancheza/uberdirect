from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Base64Bytes, BaseModel, EmailStr, Field, StringConstraints
from pydantic_extra_types.coordinate import Latitude, Longitude

from uberdirect import constants, fields


class DeliveryManifestItemCustomizationOptionTaxInfo(BaseModel):
    tax_percentage: fields.DecimalFromInt
    """
    Tax percentage associated to the item customization option. i.e.: 12.5% => 1250000.
    """


class DeliveryManifestItemCustomizationOption(BaseModel):
    name: str
    """
    Name of the customization option. Eg. Gluten Free
    """

    price: fields.DecimalFromInt
    """
    Price of the customization option in cents.
    """

    quantity: int
    """
    Quantity of the customization option.
    """

    customization_tax_info: DeliveryManifestItemCustomizationOptionTaxInfo | None = None
    """
    Tax information for the customization option.
    """


class DeliveryManifestItemCustomization(BaseModel):
    name: str
    """
    Name of the item customization. Eg. Bun Type
    """

    options: list[DeliveryManifestItemCustomizationOption]
    """
    Options for the item customization.
    """


class DeliveryManifestItemDimensions(BaseModel):
    length: int = Field(
        ge=1,
    )
    """
    Length in centimeters.
    """

    height: int = Field(
        ge=1,
    )
    """
    Height in centimeters.
    """

    depth: int = Field(
        ge=1,
    )
    """
    Depth in centimeters.
    """


class DeliveryManifestItem(BaseModel):
    name: str
    """
    Description of item.
    """

    quantity: int = Field(
        ge=1,
    )
    """
    Quantity of items.
    """

    size: constants.DeliveryManifestItemSize | None = None
    """
    Approximate size of item.

    **Note:** If nothing is specified, small will be applied by default.
    """

    dimensions: DeliveryManifestItemDimensions | None = None
    """
    Struct that contains dimensions. Please consider that weight is required when dimensions(length, depth and height) are provided.

    **Note:** If both size and dimensions are provided, the dimensions field will take precedence. Ideally, specify only one of these fields, with dimensions being the preferred option to ensure clarity and accuracy.
    """

    price: fields.DecimalFromInt | None = None
    """
    Price in cents ( ¹/₁₀₀ of currency unit ).
    """

    weight: Annotated[
        int | None,
        Field(
            ge=1,
        ),
    ] = None
    """
    Weight in grams.
    """

    vat_percentage: fields.DecimalFromInt | None = None
    """
    The percentage of VAT (value add tax) associated to the manifest_items. i.e.: 12.5% => 1250000.
    """

    item_customizations: list[DeliveryManifestItemCustomization] | None = None
    """
    Customizations for the item.
    """


class DeliverySignatureRequirement(BaseModel):
    enabled: bool
    """
    Flag for if a signature is required at this waypoint.
    """

    collect_signer_name: bool
    """
    Flag for if the signer's name is required at this waypoint.
    """

    collect_signer_relationship: bool
    """
    Flag for if the signer's relationship to the intended recipient is required at this waypoint.
    """


class DeliveryBarcodeRequirement(BaseModel):
    value: str
    """
    String value encoded in the barcode.
    """

    type: constants.DeliveryBarcodeRequirementType
    """
    Type of barcode.
    """


class DeliveryIdentificationRequirement(BaseModel):
    min_age: int
    """
    Minimum age that must be verified for this delivery. Please refer to Identification guide for more information.
    """

    no_sobriety_check: bool
    """
    A boolean flag to indicate whether a sobriety check is needed.

    **Note:**
    no_sobriety_check = true (No sobriety check will be done by courier, should be used for non-alcoholic age restricted items)
    no_sobriety_check = false (sobriety check will be done by courier, must be used if delivery contains alcoholic items)
    """


class DeliveryPickupVerification(BaseModel):
    signature_requirement: DeliverySignatureRequirement | None = None
    """
    Signature requirement spec to indicate that a signature must be collected at this waypoint.
    """

    barcodes: list[DeliveryBarcodeRequirement] | None = None
    """
    Barcode values/types that must be scanned at the waypoint. Number of elements in the array is equal to the number of barcodes that must be scanned.
    """

    identification: DeliveryIdentificationRequirement | None = None
    """
    Identification scanning/verification requirements for this waypoint.
    """

    picture: bool | None = None
    """
    Flag to indicate whether a photo is mandatory at this waypoint.
    """


class DeliveryPincodeRequirement(BaseModel):
    enabled: bool
    """
    When set to true in POST requests, the delivery will require pincode entry at handoff. The pincode is internally generated and shared by Uber.
    """

    type: constants.DeliveryPincodeRequirementType | None = None
    """
    Pincode type. Defaults to default if not provided.
    """

    value: str | None = None
    """
    The value of the pincode in case merchant_provided pincode_type was provided. Otherwise it is going to be ignored. Must be a 4-digit value for the pincode.
    """


class DeliveryDropoffVerification(BaseModel):
    signature_requirement: DeliverySignatureRequirement | None = None
    """
    Signature requirement spec to indicate that a signature must be collected at this waypoint.
    """

    barcodes: list[DeliveryBarcodeRequirement] | None = None
    """
    Barcode values/types that must be scanned at the waypoint. Number of elements in the array is equal to the number of barcodes that must be scanned.
    """

    pincode: DeliveryPincodeRequirement | None = None

    identiciation: DeliveryIdentificationRequirement | None = None
    """
    Identification scanning/verification requirements for this waypoint.
    """

    picture: bool | None = None
    """
    When set to true, mandates the Courier to capture an image as proof of delivery.
    """


class DeliveryReturnVerificationRequirement(BaseModel):
    signature_requirement: DeliverySignatureRequirement | None = None
    """
    Signature requirement spec to indicate that a signature must be collected at this waypoint.
    """

    barcodes: list[DeliveryBarcodeRequirement] | None = None
    """
    Barcode values/types that must be scanned at the waypoint. Number of elements in the array is equal to the number of barcodes that must be scanned.
    """

    picture: bool | None = None
    """
    Picture captured at the return waypoint.
    """

    pincode: DeliveryPincodeRequirement | None = None


class DeliveryExternalUserInfoMerchantAccount(BaseModel):
    email: EmailStr
    """
    End-user's email used to create the account.
    """

    account_created_at: datetime
    """
    End-user's Account creation time.
    """


class DeliveryExternalUserInfoDevice(BaseModel):
    id: Annotated[
        str,
        StringConstraints(
            min_length=256,
        ),
    ]
    """
    A string that represents the end-user unique device id.
    """


class DeliveryExternalUserInfo(BaseModel):
    device: DeliveryExternalUserInfoDevice | None = None
    merchant_account: DeliveryExternalUserInfoMerchantAccount | None = None


class DeliveryUserFeesSummaryTaxInfo(BaseModel):
    tax_rate: fields.DecimalFromInt
    """
    Integer tax added to the price to get a total.
    """


class DeliveryUserFeesSummary(BaseModel):
    amount: fields.DecimalFromInt
    """
    Integer price in cents.
    """

    fee_type: str
    """
    Specifies the type of fee to be added or subtracted.Possible values include `delivery fee`, `promo`, `loyalty points`, etc.
    """

    user_fee_tax_info: DeliveryUserFeesSummaryTaxInfo


class LatLng(BaseModel):
    lat: Latitude
    """
    Latitude.
    """

    lng: Longitude
    """
    Longitude.
    """


class CourierPublicPhoneInfo(BaseModel):
    formatted_phone_number: str
    """
    The formatted phone number with the pin code.
    """

    phone_number: str
    """
    The anonimized courier's phone number.
    """

    pin_code: str
    """
    A pin code required for dialing the courier.
    """


class Courier(BaseModel):
    name: str
    """
    Courier's first name and last initial.
    """

    vehicle_type: str
    """
    The type of vehicle the courier is using. Currently supports bicycle, car, van, truck, scooter, motorcycle, and walker.
    """

    phone_number: str
    """
    The courier's phone number. This is a masked phone number that can only receive calls or SMS from the dropoff phone number.
    """

    location: LatLng

    img_href: str
    """
    A URL to the courier's profile image.
    """

    public_phone_info: CourierPublicPhoneInfo


class Delivery(BaseModel):
    id: str
    """
    Unique identifier for the delivery (del_ + tokenize(uuid)).
    """

    quote_id: str | None = None
    """
    ID for the Delivery Quote if one was provided when creating this delivery.
    """

    complete: bool
    """
    Flag indicating if the delivery has ended, regardless of the possible end status values: delivered, canceled, returned.
    """

    courier: Courier | None = None
    """
    Courier info.
    """

    courier_imminent: bool
    """
    Flag indicating if the courier is close to the pickup or dropoff location.
    """

    created: datetime
    """
    Date/time at which the delivery was created.
    """

    currency: str
    """
    Three-letter ISO currency code, in lowercase.
    """

    deliverable_action: constants.DeliveryDeliverableAction
    """
    Specify the action for the courier to take on a delivery.
    """

    dropoff_deadline: datetime | None = None
    """
    When a delivery must be dropped off. This is the end of the dropoff window.
    """

    dropoff_eta: datetime
    """
    Estimated dropoff time.
    """

    fee: fields.DecimalFromInt
    """
    Amount in cents ( ¹/₁₀₀ of currency unit ) that will be charged if this delivery is created.
    """

    pickup_deadline: datetime | None = None
    """
    When a delivery must be picked up by. This is the end of the pickup window.
    """

    pickup_eta: datetime
    """
    Estimated time the courier will arrive at the pickup location.
    """

    pickup_ready: datetime
    """
    When a delivery is ready to be picked up. This is the start of the pickup window.
    """

    uuid: UUID
    """
    Alternative delivery identifier. The id field should be used for any identification purposes. The uuid field is equally unique but loses contextual information - Nothing in this identifier indicates that it points to a Delivery. uuid is case-sensitive. Value for the 1uuid field is UUID v4 with - characters removed.
    """

    tracking_url: str
    """
    This URL can be used to track the courier during the delivery (via an unauthenticated webpage).
    """


class DeliveryCreateRequest(BaseModel):
    pickup_name: str
    """
    Designation of the location where the courier will make the pickup. This information will be visible within the courier app.

    **Note:** The app will prioritize the utilization of the pickup_business_name if this parameter is provided.
    """

    pickup_address: fields.StructuredAddress
    """
    Pickup address details.
    """

    pickup_phone_number: fields.PhoneNumber
    """
    Phone number for the pickup location, usually the store's contact. This number allows the courier to call before heading to the dropoff location.
    """

    pickup_business_name: str | None = None
    """
    Business name of the pickup location. This information will be visible in the courier app and will override the pickup_name if provided.
    """

    pickup_latitude: Latitude | None = None
    """
    Pickup latitude coordinate.
    """

    pickup_longitude: Longitude | None = None
    """
    Pickup longitude coordinate.
    """

    pickup_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Additional instructions for the courier at the pickup location. Max 280 characters.
    """

    pickup_verification: DeliveryPickupVerification | None = None
    """
    Verification steps (e.g. Picture, Barcode scanning) that must be taken before the pickup can be completed.
    """

    pickup_ready_dt: datetime | None = None
    """
    Beginning of the window when an order must be picked up. Must be less than 30 days in the future.
    """

    pickup_deadline_dt: datetime | None = None
    """
    End of the window when an order may be picked up. Must be at least 10 mins later than pickup_ready_dt and at least 20 minutes in the future from now.
    """

    dropoff_name: str
    """
    Name of the place where the courier will make the dropoff. This information will be visible in the courier app.
    """

    dropoff_address: fields.StructuredAddress
    """
    Dropoff address details.
    """

    dropoff_phone_number: fields.PhoneNumber
    """
    Phone number for the dropoff location, usually belonging to the end-user (recipient). This number enables the courier to make calls after en route to the dropoff and before completing the trip.
    """

    dropoff_business_name: str | None = None
    """
    Business name of the dropoff location.
    """

    dropoff_latitude: Latitude | None = None
    """
    Dropoff latitude coordinate. This field adds precision to dropoff_address field. For example, if the dropoff address is "JFK Airport Queens, NY 11430", it would be highly recommended to use coordinates to locate the precise location of the dropoff.
    """

    dropoff_longitude: Longitude | None = None
    """
    Dropoff longitude coordinate. This field adds precision to dropoff_address field. For example, if the dropoff address is "JFK Airport Queens, NY 11430", it would be highly recommended to use coordinates to locate the precise location of the dropoff.
    """

    dropoff_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Accessible after the courier accepts the trip and before heading to the dropoff location. Limited to 280 characters.
    """

    dropoff_seller_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Merchant's extra dropoff instructions, accessible after the courier accepts the trip and before heading to the dropoff location. Limited to 280 characters.
    """

    dropoff_verification: DeliveryDropoffVerification | None = None
    """
    Verification steps (e.g. Picture, Barcode scanning) that must be taken before the dropoff can be completed.
    """

    dropoff_ready_dt: datetime | None = None
    """
    Beginning of the window when an order must be dropped off. Must be less than or equal to pickup_deadline_dt.
    """

    dropoff_deadline_dt: datetime | None = None
    """
    End of the window when an order must be dropped off. Must be at least 20 mins later than dropoff_ready_dt and must be greater than or equal to pickup_deadline_dt.
    """

    manifest_items: list[DeliveryManifestItem] = Field(
        min_length=1,
    )
    """
    List of items being delivered. This information will be visible in the courier app.
    """

    deliverable_action: constants.DeliveryDeliverableAction | None = None
    """
    Specify the action for the courier to take on a delivery.
    """

    manifest_reference: str | None = None
    """
    A reference identifying the manifest. Utilize this to link a delivery with relevant data in your system. This detail will be visible within the courier app.
    
    **Note:**

    Please be aware that the combination of this field with external_id must be unique; otherwise, the delivery creation will not succeed.
    If you can't ensure uniqueness for the manifest_reference, please include the "idempotency_key" in the request body and make sure it is unique.
    """

    manifest_total_value: fields.DecimalFromInt
    """
    Value in cents ( ¹/₁₀₀ of currency unit ) of the items in the delivery. i.e.: $10.99 => 1099.
    """

    quote_id: str
    """
    The ID of a previously generated delivery quote.
    """

    undeliverable_action: constants.DeliveryUndeliverableAction | None = None
    """
    If not set then the default value is return.
    """

    tip: Annotated[
        fields.DecimalFromInt | None,
        Field(
            ge=0,
        ),
    ] = None
    """
    Amount in cents ( ¹/₁₀₀ of currency unit ) that will be paid to the courier as a tip. e.g.: $5.00 => 500.

    **Note:** The fee value in the Create Delivery response includes the tip value.
    """

    idempotency_key: str | None = None
    """
    A key which is used to avoid duplicate order creation with identical idempotency keys for the same account. The key persists for a set time frame, defaulting to 60 minutes.
    """

    external_store_id: str | None = None
    """
    Unique identifier used by our Partners to reference a store or location.

    **Note:** Please be aware that if you utilize external_store_id in the Create Delivery process, you MUST also include this field in your Create Quote API calls.
    """

    return_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Additional instructions for the courier for return trips. Max 280 characters.
    """

    return_verification: DeliveryReturnVerificationRequirement | None = None
    """
    Verification steps (barcode scanning, picture, or signature) that must be taken before the return can be completed.
    """

    external_user_info: DeliveryExternalUserInfo | None = None
    """
    End-user's information to help identify users.
    """

    external_id: str | None = None
    """
    Additional reference to identify the manifest. To be used by aggregators, POS systems, and other organization structures which have an internal reference in addition to the manifest_reference used by your sub-account. Merchants can search for this value in the dashboard, and it is also visible on the billing details report generated by the dashboard.
    """

    user_fees_summary: list[DeliveryUserFeesSummary] | None = None
    """
    A breakdown of how the order value is calculated.
    """


class DeliveryUpdateRequestPickupVerification(BaseModel):
    barcodes: list[DeliveryBarcodeRequirement]
    """
    Barcode values/types that must be scanned at the waypoint. Number of elements in the array is equal to the number of barcodes that must be scanned.
    """


class DeliveryUpdateRequestDropoffVerification(BaseModel):
    barcodes: list[DeliveryBarcodeRequirement]
    """
    Barcode values/types that must be scanned at the waypoint. Number of elements in the array is equal to the number of barcodes that must be scanned.
    """


class DeliveryUpdateRequest(BaseModel):
    pickup_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Additional instructions for the courier at the pickup location. Max 280 characters.
    """

    pickup_ready_dt: datetime | None = None
    """
    (RFC 3339) Beginning of the window when an order must be picked up. Must be less than 30 days in the future.
    """

    pickup_deadline_dt: datetime | None = None
    """
    (RFC 3339) End of the window when an order may be picked up. Must be at least 10 mins later than pickup_ready_dt and at least 20 minutes in the future from now.
    """

    pickup_verification: DeliveryUpdateRequestDropoffVerification | None = None
    """
    Verification steps (e.g. Barcode scanning) that must be taken before the pickup can be completed.
    """

    dropoff_notes: Annotated[
        str | None,
        StringConstraints(
            max_length=280,
        ),
    ] = None
    """
    Additional instructions for the courier at the dropoff location, accessible after the courier accepts the trip and before heading to the dropoff location. Limited to 280 characters.
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
    (RFC 3339) Beginning of the window when an order must be dropped off. Must be less than or equal to pickup_deadline_dt.
    """

    dropoff_deadline_dt: datetime | None = None
    """
    (RFC 3339) End of the window when an order must be dropped off. Must be at least 20 mins later than dropoff_ready_dt and must be greater than or equal to pickup_deadline_dt.
    """

    dropoff_verification: DeliveryUpdateRequestDropoffVerification | None = None
    """
    Verification steps (e.g. Barcode scanning) that must be taken before the dropoff can be completed.
    """

    manifest_reference: str | None = None
    """
    A reference identifying the manifest. Utilize this to link a delivery with relevant data in your system. This detail will be visible within the courier app.

    **Note:**
    Please be aware that the combination of this field with external_id must be unique; otherwise, the delivery creation will not succeed.
    If you can't ensure uniqueness for the manifest_reference, please include the "idempotency_key" in the request body and make sure it is unique.
    """

    tip_by_customer: fields.DecimalFromInt | None = None
    """
    Amount in cents ( ¹/₁₀₀ of currency unit ) that will be paid to the courier as a tip.
    """


class DeliveryProofOfDeliveryRequest(BaseModel):
    type: constants.ProofOfDeliveryType
    waypoint: constants.ProofOfDeliveryWaypoint


class DeliveryProofOfDeliveryResponse(BaseModel):
    document: Base64Bytes
