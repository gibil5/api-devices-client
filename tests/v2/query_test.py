from datetime import datetime
from http import HTTPStatus

import pytest
import responses
from devices.v2.errors import APIDevicesV2Error
from devices.v2.query import (
    Device,
    DeviceAssignment,
    Devices,
    FilterByOperator,
    Order,
    Query,
)
from devices.v2.schemas import DevicesResponse
from requests import Session
from tests.mocks.response import (
    http_200_callback,
    http_204_callback,
    http_400_callback,
)

_APP_JSON = {"Accept": "*/*"}


@responses.activate
def test_execute_query_success(url, customer_id, devices):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    expected_endpoint = f"/v2/devices"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_200_callback(body=devices, request_headers=_APP_JSON)
    )
    # When
    response = devices_query.all()

    # Then
    assert response.dumps() == DevicesResponse.load(devices).dumps()


@responses.activate
def test_execute_query_error(url, customer_id):
    # Given

    code = "some_code_from_api"
    detail = "exploded"
    source = {"extra": "detail", "api_devices_went": "boom boom"}

    error_response = dict(code=code, detail=detail, source=source)

    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    expected_endpoint = f"/v2/devices"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_400_callback(body=error_response, request_headers=_APP_JSON)
    )

    # When/Then
    with pytest.raises(APIDevicesV2Error) as err_info:
        _ = devices_query.all()

    err = err_info.value
    assert err.status_code == HTTPStatus.BAD_REQUEST
    assert err.code == code
    assert err.detail == detail
    assert err.source == source
    assert str(err) == f"({code}) {detail}"


# Devices Scenarios
# Scenario 01: Create Query
# Scenario 02: Filter by
# Scenario 03: Filter by operator
# Scenario 04: Limit
# Scenario 05: After
# Scenario 06: Order By
def test_create_devices_success(customer_id, url):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # Then
    assert devices_query._session == session
    assert devices_query._url == url
    assert devices_query._query_parameters["customerId"] == customer_id


def test_filter_by(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.filter_by(bitlocker=True, firewall=True)

    # Then
    params = devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["filterby"] == "bitlocker:true,firewall:true"


def test_filter_by_operator(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.filter_by_operator(FilterByOperator.AND)

    # Then
    params = devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["filterbyOperator"] == "and"


def test_limit(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.limit(2)

    # Then
    params = devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["limit"] == 2


def test_after(url, customer_id, device_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.after(device_id)

    # Then
    params = devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["after"] == device_id


def test_order_by(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.order_by(order=Order.ASCENDING, order_by="os_version")

    # Then
    params = devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["sortby"] == "+os_version"


# Device Scenarios
# Scenario 01: Create Query
# Scenario 02: Assignment


def test_create_device_success(customer_id, device_id, url):
    # Given
    session = Session()
    device_query = Device(session, url, customer_id=customer_id, device_id=device_id)

    # Then
    assert device_query._session == session
    assert device_query._url == url
    assert device_query.customer_id == customer_id
    assert device_query.device_id == device_id


def test_device_assignment_success(customer_id, device_id, url):
    # Given
    session = Session()

    # When
    device_query = Device(session, url, customer_id=customer_id, device_id=device_id)
    assignment_query = device_query.assignment()

    # Then
    assert device_query._session == session
    assert device_query._url == url
    assert device_query.customer_id == customer_id
    assert device_query.device_id == device_id

    assert assignment_query.host_identifier == f"{customer_id}::{device_id}"


# Device Assignment Scenarios
# Scenario 01: Create Query
# Scenario 02: Assign User
def test_create_device_assignment_success(customer_id, device_id, url):
    # Given
    host_identifier = f"{customer_id}::{device_id}"
    session = Session()

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)

    # Then
    assert device_assignment_query._session == session
    assert device_assignment_query._url == url
    assert device_assignment_query.host_identifier == host_identifier


@responses.activate
def test_device_assignment_create(customer_id, device_id, url):
    # Given
    host_identifier = f"{customer_id}::{device_id}"
    assigned_to = "a73af01b-fd2d-4af0-af24-b5e1c5b321da"
    assigned_by = "4ae1fa54-e832-422a-ac59-4daeea03cfa9"

    session = Session()

    payload = dict(assigned_to=assigned_to, assigned_by=assigned_by)

    expected_endpoint = f"/v2/devices/{host_identifier}/assignment"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.PUT, expected_url, callback=http_204_callback(request_headers=_APP_JSON, request_body=payload)
    )

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    device_assignment_query.create(assigned_by=assigned_by, assigned_to=assigned_to)

    # Then
    assert device_assignment_query._session == session
    assert device_assignment_query._url == url
    assert device_assignment_query.host_identifier == host_identifier


@responses.activate
def test_device_assignment_get(customer_id, device_id, url):
    # Given
    host_identifier = f"{customer_id}::{device_id}"
    assigned_to = "a73af01b-fd2d-4af0-af24-b5e1c5b321da"
    assigned_by = "4ae1fa54-e832-422a-ac59-4daeea03cfa9"
    assigned_at = datetime.now()

    session = Session()

    payload = dict(
        data=dict(
            host_identifier=host_identifier,
            assigned_to=assigned_to,
            assigned_by=assigned_by,
            assigned_at=assigned_at.isoformat()
        )
    )

    expected_endpoint = f"/v2/devices/{host_identifier}/assignment"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(responses.GET, expected_url, callback=http_200_callback(body=payload))

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    response = device_assignment_query.get()

    # Then
    assert device_assignment_query._session == session
    assert device_assignment_query._url == url
    assert device_assignment_query.host_identifier == host_identifier

    assignment = response.data
    assert assignment.host_identifier == host_identifier
    assert assignment.assigned_to == assigned_to
    assert assignment.assigned_by == assigned_by
    assert assignment.assigned_at == assigned_at


@responses.activate
def test_device_assignment_delete(customer_id, device_id, url):
    # Given
    host_identifier = f"{customer_id}::{device_id}"

    session = Session()

    expected_endpoint = f"/v2/devices/{host_identifier}/assignment"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(responses.DELETE, expected_url, callback=http_204_callback())

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    device_assignment_query.delete()

    # Then
    assert device_assignment_query._session == session
    assert device_assignment_query._url == url
    assert device_assignment_query.host_identifier == host_identifier


class SomeResource(Query):

    def __init__(self, session, url):
        super().__init__(session, url)


@pytest.fixture
def url():
    return "http://someurlrandom.com.ar"


@pytest.fixture
def auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


@pytest.fixture
def customer_id():
    return "9a919a42-b506-49ee-b053-402827b761b7"


@pytest.fixture
def device_id():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"


@pytest.fixture
def devices(customer_id, device_id):
    return {
        "after":
            None,
        "count":
            1,
        "total":
            1,
        "data":
            [
                {
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
                    "created_at": "2020-07-25T04:00:11.143+00:00",
                    "updated_at": "2020-08-25T04:00:11.143+00:00",
                }
            ]
    }
