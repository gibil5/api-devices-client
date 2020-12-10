from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from devices.schemas import Serializable
from marshmallow import EXCLUDE, Schema, fields, post_load, validate


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
class Device(Serializable):
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
    jamf = fields.Str()
    kaseya = fields.Str()

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
