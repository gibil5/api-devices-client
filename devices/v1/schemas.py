import uuid
from dataclasses import dataclass
from datetime import datetime

from devices.schemas import Serializable
from marshmallow import Schema, fields, post_load, validate


class DeviceAttributeSchema(Schema):  # pylint: disable=too-few-public-methods
    value = fields.Str(required=False, default=None)
    last_update = fields.DateTime(required=False, default=None)

    @post_load
    def create_device_attribute(self, data, **_):  # pylint: disable=no-self-use
        return DeviceAttribute(**data)


class DeviceAttributesSchema(Schema):  # pylint: disable=too-few-public-methods
    bitlocker = fields.Nested(DeviceAttributeSchema, required=False)
    device_name = fields.Nested(DeviceAttributeSchema, required=False)
    filevault = fields.Nested(DeviceAttributeSchema, required=False)
    firewall = fields.Nested(DeviceAttributeSchema, required=False)
    gatekeeper = fields.Nested(DeviceAttributeSchema, required=False)
    hardware_model = fields.Nested(DeviceAttributeSchema, required=False)
    hardware_vendor = fields.Nested(DeviceAttributeSchema, required=False)
    hardware_description = fields.Nested(DeviceAttributeSchema, required=False)
    host_identifier = fields.Nested(DeviceAttributeSchema, required=False)
    host_uuid = fields.Nested(DeviceAttributeSchema, required=False)
    hostname = fields.Nested(DeviceAttributeSchema, required=False)
    last_active = fields.Nested(DeviceAttributeSchema, required=False)
    os_auto_update = fields.Nested(DeviceAttributeSchema, required=False)
    os_type = fields.Nested(DeviceAttributeSchema, required=False)
    os_version = fields.Nested(DeviceAttributeSchema, required=False)
    os_name = fields.Nested(DeviceAttributeSchema, required=False)
    serial_number = fields.Nested(DeviceAttributeSchema, required=False)
    username = fields.Nested(DeviceAttributeSchema, required=False)
    total_ram = fields.Nested(DeviceAttributeSchema, required=False)
    total_hard_drive_space = fields.Nested(DeviceAttributeSchema, required=False)
    free_hard_drive_space = fields.Nested(DeviceAttributeSchema, required=False)
    bitlocker_encryption_percent = fields.Nested(DeviceAttributeSchema, required=False)
    filevault_encryption_percent = fields.Nested(DeviceAttributeSchema, required=False)
    screen_timeout = fields.Nested(DeviceAttributeSchema, required=False)
    source_last_check_in = fields.DateTime(required=False)
    serial = fields.Str(required=False)

    @post_load
    def _create_device_attributes(self, data, **_):  # pylint: disable=no-self-use
        return DeviceAttributes(**data)


class DeviceStatusSchema(Schema):  # pylint: disable=too-few-public-methods
    customer_id = fields.Str(required=True)
    serial_number_hash = fields.Str(required=True)
    serial = fields.Str(allow_none=True)
    enrolled = fields.Bool(allow_none=True)
    source = fields.Str(allow_none=True)
    last_check_in = fields.DateTime(allow_none=True)
    healthy = fields.Bool(allow_none=True)
    attributes = fields.Nested(DeviceAttributesSchema, required=False)

    @post_load
    def create__device_status(self, data, **_):  # pylint: disable=no-self-use
        return DeviceStatus(**data)


class CustomerDeviceStatusSchema(Schema):  # pylint: disable=too-few-public-methods
    after = fields.Str(allow_none=True, validate=validate.Length(equal=32))
    count = fields.Int(required=True)
    total = fields.Int(required=True)
    devices = fields.Nested(DeviceStatusSchema, required=True, many=True)

    @post_load
    def create_customer_device_status(self, data, **_):  # pylint: disable=no-self-use
        return CustomerDeviceStatus(**data)


@dataclass
class CustomerDeviceStatus(Serializable):
    serializer = CustomerDeviceStatusSchema()

    after: str
    count: int
    total: int
    devices: list


@dataclass
class DeviceAttribute(Serializable):
    value: str = None
    last_update: datetime = None


@dataclass
class DeviceAttributes(Serializable):
    serial: str = None
    source_last_check_in: datetime = None
    filevault: DeviceAttribute = None
    firewall: DeviceAttribute = None
    gatekeeper: DeviceAttribute = None
    hardware_model: DeviceAttribute = None
    hardware_vendor: DeviceAttribute = None
    hardware_description: DeviceAttribute = None
    host_identifier: DeviceAttribute = None
    host_uuid: DeviceAttribute = None
    hostname: DeviceAttribute = None
    last_active: DeviceAttribute = None
    os_auto_update: DeviceAttribute = None
    os_type: DeviceAttribute = None
    os_version: DeviceAttribute = None
    os_name: DeviceAttribute = None
    serial_number: DeviceAttribute = None
    username: DeviceAttribute = None
    total_ram: DeviceAttribute = None
    total_hard_drive_space: DeviceAttribute = None
    free_hard_drive_space: DeviceAttribute = None
    bitlocker_encryption_percent: DeviceAttribute = None
    filevault_encryption_percent: DeviceAttribute = None
    screen_timeout: DeviceAttribute = None
    bitlocker: DeviceAttribute = None
    device_name: DeviceAttribute = None


@dataclass
class DeviceStatus(Serializable):
    serializer = DeviceStatusSchema()

    customer_id: uuid.UUID
    serial_number_hash: str
    serial: str
    enrolled: bool
    source: str
    last_check_in: datetime
    healthy: bool
    attributes: DeviceAttributes = None
