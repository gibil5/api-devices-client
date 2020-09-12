from dataclasses import dataclass
from datetime import datetime

from devices.schemas import Serializable
from marshmallow import EXCLUDE, Schema, fields, post_load


class DeviceSchema(Schema):  # pylint: disable=too-few-public-methods

    class Meta:
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
    source_last_check_in = fields.DateTime(required=True, allow_none=False)
    enrolled = fields.Boolean(required=True, allow_none=False)
    hostname = fields.Str(required=True, allow_none=False)
    traceable = fields.Boolean(required=True, allow_none=False)
    # Hardware
    serial = fields.Str(required=True, allow_none=False)
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
    assigned = fields.Boolean(required=False, allow_none=True)

    @post_load
    def create_device(self, data, **_):  # pylint: disable=no-self-use
        return Device(**data)


class DeviceResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    after = fields.Str(required=True, allow_none=True)
    total = fields.Integer(required=True, allow_none=False)
    count = fields.Integer(required=True, allow_none=False)
    data = fields.List(fields.Nested(DeviceSchema), required=True, allow_none=False)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return DeviceResponse(**data)


class ErrorResponseSchema(Schema):  # pylint: disable=too-few-public-methods
    code = fields.Str(required=True, allow_none=False)
    detail = fields.Str(required=True, allow_none=False)
    source = fields.Dict(required=True, allow_none=True)

    @post_load
    def create_response(self, data, **_):  # pylint: disable=no-self-use
        return ErrorResponse(**data)


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
class DeviceResponse(Serializable):
    serializer = DeviceResponseSchema()
    after: str
    total: int
    count: int
    data: list


@dataclass
class ErrorResponse(Serializable):
    serializer = ErrorResponseSchema()
    code: str
    detail: str
    source: dict
