from datetime import datetime
from http import HTTPStatus

import pytest
import responses
from devices.errors import InvalidParamsError
from devices.v2.errors import APIDevicesV2Error
from devices.v2.query import (
    MDM,
    Assignment,
    Device,
    DeviceAssignment,
    Devices,
    DownloadLink,
    FilterByOperator,
    Order,
    Query,
)
from devices.v2.schemas import DevicesResponse
from requests import Session
from tests.mocks.response import (
    http_200_callback,
    http_202_callback,
    http_204_callback,
    http_400_callback,
)

_APP_JSON = {"Accept": "*/*"}


@responses.activate
def test_execute_query_success(url, customer_id, devices):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    expected_endpoint = "/v2/devices"
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

    expected_endpoint = "/v2/devices"
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
    assert devices_query.session == session
    assert devices_query.url == url
    assert devices_query.query_parameters["customerId"] == customer_id


def test_filter_by(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.filter_by(bitlocker=True, firewall=True)

    # Then
    params = devices_query.query_parameters
    assert params["customerId"] == customer_id
    assert params["filterby"] == "bitlocker:true,firewall:true"


def test_filter_by_operator(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.filter_by_operator(FilterByOperator.AND)

    # Then
    params = devices_query.query_parameters
    assert params["customerId"] == customer_id
    assert params["filterbyOperator"] == "and"


def test_limit(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.limit(2)

    # Then
    params = devices_query.query_parameters
    assert params["customerId"] == customer_id
    assert params["limit"] == 2


def test_after(url, customer_id, device_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.after(device_id)

    # Then
    params = devices_query.query_parameters
    assert params["customerId"] == customer_id
    assert params["after"] == device_id


def test_order_by(url, customer_id):
    # Given
    session = Session()
    devices_query = Devices(session, url, customer_id=customer_id)

    # When
    devices_query.order_by(order=Order.ASCENDING, order_by="os_version")

    # Then
    params = devices_query.query_parameters
    assert params["customerId"] == customer_id
    assert params["sortby"] == "+os_version"


# Device Scenarios
# Scenario 01: Create query
# Scenario 02: Assignment
def test_create_device_success(customer_id, device_id, url):
    # Given
    session = Session()
    device_query = Device(session, url, customer_id=customer_id, device_id=device_id)

    # Then
    assert device_query.session == session
    assert device_query.url == url
    assert device_query.customer_id == customer_id
    assert device_query.device_id == device_id


def test_device_assignment_success(customer_id, device_id, url):
    # Given
    session = Session()

    # When
    device_query = Device(session, url, customer_id=customer_id, device_id=device_id)
    assignment_query = device_query.assignment()

    # Then
    assert device_query.session == session
    assert device_query.url == url
    assert device_query.customer_id == customer_id
    assert device_query.device_id == device_id

    assert assignment_query.host_identifier == f"{customer_id}::{device_id}"


# Device Assignment Scenarios
# Scenario 01: Create query
# Scenario 02: POST assignment
# Scenario 03: GET assignment
# Scenario 04: DELETE assignment
def test_create_device_assignment_success(customer_id, device_id, url):
    # Given
    host_identifier = f"{customer_id}::{device_id}"
    session = Session()

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)

    # Then
    assert device_assignment_query.session == session
    assert device_assignment_query.url == url
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
        responses.PUT,
        expected_url,
        callback=http_204_callback(request_headers=_APP_JSON, request_body=payload),
    )

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    device_assignment_query.create(assigned_by=assigned_by, assigned_to=assigned_to)

    # Then
    assert device_assignment_query.session == session
    assert device_assignment_query.url == url
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
    responses.add_callback(
        responses.GET,
        expected_url,
        callback=http_200_callback(body=payload),
    )

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    response = device_assignment_query.get()

    # Then
    assert device_assignment_query.session == session
    assert device_assignment_query.url == url
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
    responses.add_callback(
        responses.DELETE,
        expected_url,
        callback=http_204_callback(),
    )

    # When
    device_assignment_query = DeviceAssignment(session, url, host_identifier=host_identifier)
    device_assignment_query.delete()

    # Then
    assert device_assignment_query.session == session
    assert device_assignment_query.url == url
    assert device_assignment_query.host_identifier == host_identifier


# Scenarios for MDM
# Scenario 01: MDM create Query
# Scenario 02: Get MDM success
# Scenario 03: Get MDM incorrect mdm
# Scenario 04: Create MDM success
# Scenario 05: Create MDM incorrect mdm
def test_mdm_create_query(customer_id, url):
    # Given
    session = Session()

    # When
    mdm_query = MDM(session=session, url=url, customer_id=customer_id)

    # Then
    assert mdm_query.session == session
    assert mdm_query.url == url
    assert mdm_query.customer_id == customer_id


@responses.activate
def test_get_mdm_success(customer_id, mdm_name, url, mdm):
    # Given
    session = Session()

    expected_endpoint = f"/v2/mdm/{mdm_name}/{customer_id}"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET,
        expected_url,
        callback=http_200_callback(body=mdm, request_headers=_APP_JSON),
    )

    # When
    mdm_query = MDM(session=session, url=url, customer_id=customer_id)
    response = mdm_query.get(name=mdm_name)

    # Then
    mdm_info = response.data
    assert mdm_query.url == url
    assert mdm_query.customer_id == customer_id

    assert str(mdm_info.customer_id) == customer_id
    assert mdm_info.name == mdm_name
    assert mdm_info.state == mdm["data"]["state"]
    assert isinstance(mdm_info.updated_at, datetime)
    assert isinstance(mdm_info.created_at, datetime)
    assert mdm_info.identifier == mdm["data"]["identifier"]
    assert mdm_info.server_url == mdm["data"]["server_url"]
    assert mdm_info.enroll_url == mdm["data"]["enroll_url"]


def test_get_mdm_incorrect_mdm_name(url, customer_id):
    # Given
    session = Session()
    name = "not_an_mdm"

    mdm_query = MDM(session=session, url=url, customer_id=customer_id)

    # When/Then
    with pytest.raises(InvalidParamsError):
        _ = mdm_query.get(name=name)


@responses.activate
def test_create_mdm_success(customer_id, mdm_name, url, mdm):
    # Given
    session = Session()

    expected_endpoint = "/v2/mdm"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.POST, expected_url, callback=http_200_callback(
            body=mdm,
            request_headers=_APP_JSON,
        )
    )

    # When
    mdm_query = MDM(session=session, url=url, customer_id=customer_id)
    response = mdm_query.create(name=mdm_name)

    # Then
    mdm_info = response.data
    assert mdm_query.url == url
    assert mdm_query.customer_id == customer_id

    assert str(mdm_info.customer_id) == customer_id
    assert mdm_info.name == mdm_name
    assert mdm_info.state == mdm["data"]["state"]
    assert isinstance(mdm_info.updated_at, datetime)
    assert isinstance(mdm_info.created_at, datetime)
    assert mdm_info.identifier == mdm["data"]["identifier"]
    assert mdm_info.server_url == mdm["data"]["server_url"]
    assert mdm_info.enroll_url == mdm["data"]["enroll_url"]


def test_create_mdm_incorrect_mdm_name(url, customer_id):
    # Given
    session = Session()
    name = "not_an_mdm"

    mdm_query = MDM(session=session, url=url, customer_id=customer_id)

    # When/Then
    with pytest.raises(InvalidParamsError):
        _ = mdm_query.create(name=name)


# Scenarios for DownloadLink
# Scenario 01: Query Creation
# Scenario 02: Success (Non null values)
# Scenario 03: Null Values
def test_download_link_query(customer_id, url):
    # Given
    session = Session()

    # When
    download_link_query = DownloadLink(
        session=session,
        url=url,
        customer_id=customer_id,
    )

    # Then
    assert download_link_query.session == session
    assert download_link_query.url == url
    assert download_link_query.customer_id == customer_id


@responses.activate
def test_get_download_link_success(customer_id, url, download_links):
    # Given
    session = Session()

    expected_endpoint = f"/v2/download-link/{customer_id}"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET,
        expected_url,
        callback=http_200_callback(body=download_links, request_headers=_APP_JSON),
    )

    # When
    download_link_query = DownloadLink(
        session=session,
        url=url,
        customer_id=customer_id,
    )
    response = download_link_query.get()

    # Then
    assert download_link_query.url == url
    assert download_link_query.customer_id == customer_id

    assert response.data.jamf == download_links["data"]["jamf"]
    assert response.data.kaseya == download_links["data"]["kaseya"]


@responses.activate
def test_get_download_link_null_values(customer_id, url, null_download_links):
    # Given
    session = Session()

    expected_endpoint = f"/v2/download-link/{customer_id}"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET,
        expected_url,
        callback=http_200_callback(body=null_download_links, request_headers=_APP_JSON),
    )

    # When
    download_link_query = DownloadLink(
        session=session,
        url=url,
        customer_id=customer_id,
    )
    response = download_link_query.get()

    # Then
    assert download_link_query.url == url
    assert download_link_query.customer_id == customer_id

    assert response.data.jamf is None
    assert response.data.kaseya is None


# Scenarios for Assignment
# Scenario 01: Query Creation
# Scenario 02: Success (Non null values)
# Scenario 03: Null Values
def test_assignment_query(customer_id, url, employee_ids):
    # Given
    session = Session()

    # When
    download_link_query = Assignment(
        session=session,
        url=url,
        customer_id=customer_id,
        employee_ids=employee_ids,
    )

    # Then
    assert download_link_query.session == session
    assert download_link_query.url == url
    assert download_link_query.customer_id == customer_id
    assert download_link_query.employee_ids == employee_ids


@responses.activate
def test_request_assignments_success(customer_id, url, employee_ids):
    # Given
    session = Session()

    expected_endpoint = "/v2/assignments/request"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.POST,
        expected_url,
        callback=http_202_callback(),
    )

    # When
    assignments_query = Assignment(
        session=session,
        url=url,
        customer_id=customer_id,
        employee_ids=employee_ids,
    )
    assignments_query.request()

    # Then
    assert assignments_query.url == url
    assert assignments_query.customer_id == customer_id
    assert assignments_query.employee_ids == employee_ids


@responses.activate
def test_request_assignments_failed(customer_id, url):
    # Given
    session = Session()
    employee_ids = None

    code = "some_code_from_api"
    detail = "exploded"
    source = {"extra": "detail", "api_devices_went": "boom boom"}

    error_response = dict(code=code, detail=detail, source=source)

    expected_endpoint = "/v2/assignments/request"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.POST, expected_url, callback=http_400_callback(
            body=error_response,
            request_headers=_APP_JSON,
        )
    )
    # When
    assignments_query = Assignment(
        session=session,
        url=url,
        customer_id=customer_id,
        employee_ids=employee_ids,
    )
    with pytest.raises(APIDevicesV2Error) as err_info:
        _ = assignments_query.request()

    # Then
    assert assignments_query.url == url
    assert assignments_query.customer_id == customer_id
    assert assignments_query.employee_ids == employee_ids

    err = err_info.value
    assert err.status_code == HTTPStatus.BAD_REQUEST
    assert err.code == code
    assert err.detail == detail
    assert err.source == source
    assert str(err) == f"({code}) {detail}"


class SomeResource(Query):  # pylint: disable=too-few-public-methods
    """
    No need to re-define __init__ here since by default Python will look for
    the parent's __init__ method when it's not present in the child class.
    """


@pytest.fixture(name="url")
def get_url():
    return "http://someurlrandom.com.ar"


@pytest.fixture(name="auth_token")
def get_auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


@pytest.fixture(name="mdm_name")
def get_mdm_name():
    return "kaseya"


@pytest.fixture(name="org_id")
def get_org_id():
    return "987654345678899010101"


@pytest.fixture(name="employee_ids")
def get_employee_ids():
    return [
        "25938eac-f148-45a0-bf5b-620b373c59e1",
        "8a46f176-7db2-403d-bf40-ea91146f8e76",
    ]


@pytest.fixture(name="devices")
def get_devices(customer_id, device_id):
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
                    "state": "NON_REPORTING",
                    "lock_status": "UNLOCKED",
                    "created_at": "2020-07-25T04:00:11.143+00:00",
                    "updated_at": "2020-08-25T04:00:11.143+00:00",
                }
            ]
    }


@pytest.fixture(name="mdm")
def get_mdm(customer_id, mdm_name, org_id, url):
    return {
        "data":
            {
                "customer_id": customer_id,
                "name": mdm_name,
                "state": "CREATED",
                "created_at": "2020-07-25T04:00:11.143+00:00",
                "updated_at": "2020-08-25T04:00:11.143+00:00",
                "identifier": org_id,
                "server_url": url,
                "enroll_url": f"{url}/enroll"
            }
    }


@pytest.fixture(name="download_links")
def get_download_links():
    return {
        "data": {
            "jamf": "jamf_url",
            "kaseya": "kaseya_url",
        },
    }


@pytest.fixture(name="null_download_links")
def get_null_download_links():
    return {
        "data": {
            "jamf": None,
            "kaseya": None,
        },
    }
