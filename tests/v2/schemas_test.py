import pytest
from devices.v2.schemas import DeviceSchema
from marshmallow import ValidationError


# Scenarios for DeviceSchema
# Scenario 01: Lock Status valid
# Scenario 02: Lock Status missing
# Scenario 03: Lock Status None
# Scenario 04: Lock Status invalid
@pytest.mark.parametrize(
    "lock_status", [
        "LOCKED",
        "UNLOCKED",
        "PENDING_LOCK",
        "PENDING_UNLOCK",
        "FAILED_LOCK",
        "FAILED_UNLOCK",
    ]
)
def test_device_schema_lock_status_valid(customer_id, device_id, device_factory, lock_status):
    # Given
    device_payload = device_factory(lock_status=lock_status)

    # When
    device = DeviceSchema().load(device_payload)

    # Then
    assert device.customer_id == customer_id
    assert device.id == device_id
    assert device.lock_status == lock_status


def test_device_schema_lock_status_missing(customer_id, device_id, device_factory):
    # Given
    device_payload = device_factory(lock_status=None)
    del device_payload["lock_status"]

    # When
    device = DeviceSchema().load(device_payload)

    # Then
    assert device.customer_id == customer_id
    assert device.id == device_id
    assert device.lock_status == "UNKNOWN"


def test_device_schema_lock_status_none(customer_id, device_id, device_factory):
    # Given
    device_payload = device_factory(lock_status=None)

    # When
    device = DeviceSchema().load(device_payload)

    # Then
    assert device.customer_id == customer_id
    assert device.id == device_id
    assert device.lock_status == "UNKNOWN"


@pytest.mark.parametrize("lock_status", [
    "not_the_enum",
    123456,
    True,
])
def test_device_schema_lock_status_invalid(customer_id, device_id, device_factory, lock_status):
    # Given
    device_payload = device_factory(lock_status=lock_status)

    # When/Then
    with pytest.raises(ValidationError):
        _ = DeviceSchema().load(device_payload)


@pytest.fixture(name="device_factory")
def _get_device_factory(
    customer_id,
    device_id,
):

    def factory(lock_status="UNLOCKED"):
        return {
            "customer_id": customer_id,
            "id": device_id,
            "enrolled": True,
            "source": "kaseya",
            "source_id": "132135486721",
            "source_last_check_in": "2020-08-26T04:00:11.143+00:00",
            "source_last_sync": "2020-08-25T04:00:11.143+00:00",
            "serial": "aSerial",
            "traceable": True,
            "hostname": "one-device",
            "healthy": False,
            "state": "NON_REPORTING",
            "lock_status": lock_status,
            "created_at": "2020-07-25T04:00:11.143+00:00",
            "updated_at": "2020-08-25T04:00:11.143+00:00",
        }

    return factory
