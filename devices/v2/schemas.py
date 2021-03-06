from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from marshmallow import (
    EXCLUDE,
    Schema,
    fields,
    missing,
    post_load,
    pre_load,
    validate,
)

from devices.schemas import Serializable


class DeviceState(str, Enum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    NON_REPORTING = "NON_REPORTING"


class DeviceLockStatus(str, Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    PENDING_LOCK = "PENDING_LOCK"
    PENDING_UNLOCK = "PENDING_UNLOCK"
    FAILED_LOCK = "FAILED_LOCK"
    FAILED_UNLOCK = "FAILED_UNLOCK"
    UNKNOWN = "UNKNOWN"


class DeviceSchema(Schema):  # pylint: disable=too-few-public-methods

    class Meta:  # pylint: disable=too-few-public-methods
        unknown = EXCLUDE

    # Ids
    customer_id = fields.Str(required=True, allow_none=False)
    id = fields.Str(required=True, allow_none=False)
    # Audit
    created_at = fields.DateTime(required=True, allow_none=False)
    updated_at = fields.DateTime(required=True, allow_none=False)
    host_identifier = fields.Str(required=False, allow_none=True)
    host_uuid = fields.Str(required=False, allow_none=True)
    # Source
    source = fields.Str(required=True, allow_none=False)
    source_id = fields.Str(required=True, allow_none=False)
    source_last_sync = fields.DateTime(required=True, allow_none=False)
    source_last_check_in = fields.DateTime(required=True, allow_none=True)
    enrolled = fields.Boolean(required=True, allow_none=False)
    hostname = fields.Str(required=True, allow_none=True)
    traceable = fields.Boolean(required=True, allow_none=False)
    # Hardware
    serial = fields.Str(required=True, allow_none=True)
    hardware_model = fields.Str(required=False, allow_none=True)
    hardware_vendor = fields.Str(required=False, allow_none=True)
    hardware_description = fields.Str(required=False, allow_none=True)
    total_ram = fields.Float(required=False, allow_none=True)
    total_hard_drive_space = fields.Float(required=False, allow_none=True)
    free_hard_drive_space = fields.Float(required=False, allow_none=True)
    processor_type = fields.Str(required=False, allow_none=True)
    # OS
    os_type = fields.Str(required=False, allow_none=True)
    os_name = fields.Str(required=False, allow_none=True)
    os_version = fields.Str(required=False, allow_none=True)
    # OS Configuration
    os_auto_update = fields.Boolean(required=False, allow_none=True)
    screen_timeout = fields.Float(required=False, allow_none=True)
    # Security
    firewall = fields.Boolean(required=False, allow_none=True)
    bitlocker = fields.Boolean(required=False, allow_none=True)
    bitlocker_encryption_percent = fields.Float(required=False, allow_none=True)
    filevault = fields.Boolean(required=False, allow_none=True)
    filevault_encryption_percent = fields.Float(required=False, allow_none=True)
    gatekeeper = fields.Boolean(required=False, allow_none=True)
    lock_status = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf(list(DeviceLockStatus)),
        missing=DeviceLockStatus.UNKNOWN.value,
    )

    # Activity
    username = fields.Str(required=False, allow_none=True)
    last_active = fields.DateTime(required=False, allow_none=True)
    # Assignment
    assigned_to = fields.Str(required=False, allow_none=True)
    assigned_by = fields.Str(required=False, allow_none=True)
    assigned_at = fields.DateTime(required=False, allow_none=True)
    # Computed attributes
    healthy = fields.Boolean(required=True, allow_none=False)
    assigned = fields.Boolean(required=False, allow_none=False)
    state = fields.Str(required=True, allow_none=False, validate=validate.OneOf(list(DeviceState)))

    @pre_load
    def _lock_status_add_missing_as_replacement_for_none(self, data, **_):  # pylint: disable=no-self-use
        """
        Replaces None values with marshmallow.missing

        The goal of this function is to treat None values the same way
        as missing. The current version of marshmallow does not offer a default for
        load.
        It has a RFC:
        https://github.com/marshmallow-code/marshmallow/issues/778

        And an open PR:
        https://github.com/marshmallow-code/marshmallow/pull/1742

        But this apply for 3.12.X versions of the lib, not the one currently used

        This solution was inspired by this comment:
        https://github.com/marshmallow-code/marshmallow/issues/588#issuecomment-283544372

        Also, in theory there should NOT be any None field coming from the API, that'd
        mean something worse has happened, but still this schema was left flexible.

        Because this is added as missing, the value that the lib will return is UNKNOWN
        """
        try:
            lock_status = data["lock_status"]
            if lock_status is None:
                data["lock_status"] = missing
            return data
        except KeyError:
            return data

    @post_load
    def create_device(self, data, **_):  # pylint: disable=no-self-use
        return Device(**data)


class AssignmentSchema(Schema):  # pylint: disable=too-few-public-methods
    host_identifier = fields.Str(required=True, allow_none=False)
    assigned_to = fields.Str(required=True, allow_none=False)
    assigned_by = fields.Str(required=True, allow_none=False)
    assigned_at = fields.DateTime(required=True, allow_none=False)

    @post_load
    def create_assignment(self, data, **_):  # pylint: disable=no-self-use
        return Assignment(**data)


class DevicesResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    after = fields.Str(required=True, allow_none=True)
    total = fields.Integer(required=True, allow_none=False)
    count = fields.Integer(required=True, allow_none=False)
    data = fields.List(fields.Nested(DeviceSchema), required=True, allow_none=False)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return DevicesResponse(**data)


class DeviceResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    data = fields.Nested(DeviceSchema, required=True, allow_none=False)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return DeviceResponse(**data)


class AssignmentResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    data = fields.Nested(AssignmentSchema, required=True, allow_none=False)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return AssignmentResponse(**data)


class ErrorResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    code = fields.Str(required=True, allow_none=False)
    detail = fields.Str(required=True, allow_none=False)
    source = fields.Dict(required=True, allow_none=True)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return ErrorResponse(**data)


class CreateAssignmentPayloadSchema(Schema):  # pylint: disable=too-few-public-methods
    assigned_to = fields.Str(required=True, allow_none=False)
    assigned_by = fields.Str(required=True, allow_none=False)

    @post_load
    def create_payload(self, data, **_):  # pylint: disable=no-self-use
        return CreateAssignmentPayload(**data)


class CreateMDMPayloadSchema(Schema):  # pylint: disable=too-few-public-methods
    customer_id = fields.Str(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)

    @post_load
    def create_payload(self, data, **_):  # pylint: disable=no-self-use
        return CreateMDMPayloadSchema(**data)


@dataclass
class Device(Serializable):  # pylint: disable=too-many-instance-attributes
    serializer = DeviceSchema()
    # Ids
    customer_id: str
    id: str
    # Audit
    created_at: datetime
    updated_at: datetime
    host_identifier: str = None
    host_uuid: str = None
    # Source
    source: str = None
    source_id: str = None
    source_last_sync: datetime = None
    source_last_check_in: datetime = None
    enrolled: bool = None
    hostname: str = None
    traceable: bool = None
    # Hardware
    serial: str = None
    hardware_model: str = None
    hardware_vendor: str = None
    hardware_description: str = None
    total_ram: float = None
    total_hard_drive_space: float = None
    free_hard_drive_space: float = None
    processor_type: str = None
    # OS
    os_type: str = None
    os_name: str = None
    os_version: str = None
    # OS Configuration
    os_auto_update: bool = None
    screen_timeout: float = None
    # Security
    firewall: bool = None
    bitlocker: bool = None
    bitlocker_encryption_percent: float = None
    filevault: bool = None
    filevault_encryption_percent: float = None
    gatekeeper: bool = None
    lock_status: str = None
    # Activity
    username: str = None
    last_active: datetime = None
    # Assignment
    assigned_to: str = None
    assigned_by: str = None
    assigned_at: datetime = None
    # Computed attributes
    healthy: bool = None
    assigned: bool = None
    state: str = None


@dataclass
class Assignment(Serializable):
    serializer = AssignmentSchema()
    host_identifier: str
    assigned_to: str
    assigned_by: str
    assigned_at: datetime


@dataclass
class DevicesResponse(Serializable):
    serializer = DevicesResponseSchema()
    after: str
    total: int
    count: int
    data: list


@dataclass
class DeviceResponse(Serializable):
    serializer = DeviceResponseSchema()
    data: Device


@dataclass
class AssignmentResponse(Serializable):
    serializer = AssignmentResponseSchema()
    data: Assignment


@dataclass
class ErrorResponse(Serializable):
    serializer = ErrorResponseSchema()
    code: str
    detail: str
    source: dict


@dataclass
class CreateAssignmentPayload(Serializable):
    serializer = CreateAssignmentPayloadSchema()
    assigned_to: str
    assigned_by: str


@dataclass
class CreateMDMPayload(Serializable):
    serializer = CreateMDMPayloadSchema()
    customer_id: str
    name: str


class MDMName(str, Enum):
    JAMF = "jamf"
    KASEYA = "kaseya"


class MDMState(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    FAILED = "FAILED"


class MDMSchema(Schema):  # pylint: disable=too-few-public-methods
    customer_id = fields.UUID(required=True)
    name = fields.Str(required=True, validate=validate.OneOf(list(MDMName)))
    state = fields.Str(required=True, validate=validate.OneOf(list(MDMState)))
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    identifier = fields.Str(allow_none=True)
    server_url = fields.Str(allow_none=True)
    enroll_url = fields.Str(allow_none=True)

    @post_load
    def create_mdm(self, data, **_):  # pylint: disable=no-self-use
        return MDM(**data)


@dataclass
class MDM(Serializable):  # pylint: disable=too-many-instance-attributes
    serializer = MDMSchema()
    customer_id: str
    name: str
    state: str
    created_at: datetime
    updated_at: datetime
    identifier: str = None
    server_url: str = None
    enroll_url: str = None


class MDMResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    data = fields.Nested(MDMSchema, required=True, allow_none=False)

    @post_load
    def create_mdm_response(self, data, **_):  # pylint: disable=no-self-use
        return MDMResponse(**data)


@dataclass
class MDMResponse(Serializable):
    serializer = MDMResponseSchema()
    data: MDM


class DownloadLinkSchema(Schema):  # pylint: disable=too-few-public-methods
    jamf = fields.Str(required=True, allow_none=True)
    kaseya = fields.Str(required=True, allow_none=True)

    @post_load
    def create_download_link(self, data, **_):  # pylint: disable=no-self-use
        return DownloadLink(**data)


@dataclass
class DownloadLink(Serializable):
    serializer = DownloadLinkSchema()
    jamf: str
    kaseya: str


class DownloadLinkResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    data = fields.Nested(DownloadLinkSchema, required=True, allow_none=False)

    @post_load
    def create_download_link_response(self, data, **_):  # pylint: disable=no-self-use
        return DownloadLinkResponse(**data)


@dataclass
class DownloadLinkResponse(Serializable):
    serializer = DownloadLinkResponseSchema()
    data: DownloadLink


class AssignmentsRequestPayloadSchema(Schema):  # pylint: disable=too-few-public-methods
    customer_id = fields.Str(required=True, allow_none=False)
    employee_ids = fields.List(fields.Str(), required=True, allow_none=False)

    @post_load
    def create_payload(self, data, **_):  # pylint: disable=no-self-use
        return AssignmentsRequestPayload(**data)


@dataclass
class AssignmentsRequestPayload(Serializable):
    serializer = AssignmentsRequestPayloadSchema()
    customer_id: str
    employee_ids: List[str]
