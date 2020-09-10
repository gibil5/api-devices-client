from http import HTTPStatus

import pytest
import responses
from devices.v1.errors import APIDevicesV1Error
from devices.v1.query import CustomerDevices, FilterByOperator, Order, Query
from devices.v1.schemas import CustomerDeviceStatus
from requests import Session
from tests.mocks.response import http_200_callback, http_400_callback

_APP_JSON = {"Accept": "*/*"}


@responses.activate
def test_execute_query_success(url, customer_id, customer_device_status):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    expected_endpoint = f"/customers/{customer_id}/devices/status"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_200_callback(body=customer_device_status, request_headers=_APP_JSON)
    )
    # When
    response = customer_devices_query.all()

    # Then
    assert response.dumps() == CustomerDeviceStatus.load(customer_device_status).dumps()


@responses.activate
def test_execute_query_error(url, customer_id, customer_device_error, error_message):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    expected_endpoint = f"/customers/{customer_id}/devices/status"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_400_callback(body=customer_device_error, request_headers=_APP_JSON)
    )

    # When/Then
    with pytest.raises(APIDevicesV1Error) as err_info:
        _ = customer_devices_query.all()

    err = err_info.value

    assert err.status_code == HTTPStatus.BAD_REQUEST

    expected_error = f"HTTPStatus.BAD_REQUEST Client Error: Bad Request for url: {url}/customers/{customer_id}/devices/status"
    assert err.error == expected_error

    assert err.detail["message"] == error_message


def test_create_customer_devices_success(customer_id, url):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # Then
    assert customer_devices_query._customer_id == customer_id
    assert customer_devices_query._session == session
    assert customer_devices_query._url == url
    assert customer_devices_query._query_parameters == {}


def test_filter_by(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.filter_by(bitlocker=True, firewall=True)

    # Then
    assert customer_devices_query._query_parameters == {"filterby": "bitlocker:true,firewall:true"}


def test_filter_by_operator(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.filter_by_operator(FilterByOperator.AND)

    # Then
    assert customer_devices_query._query_parameters == {"filterbyOperator": "and"}


def test_limit(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.limit(2)

    # Then
    assert customer_devices_query._query_parameters == {"limit": 2}


def test_after(url, customer_id, serial_number_hash):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.after(serial_number_hash)

    # Then
    assert customer_devices_query._query_parameters == {"after": serial_number_hash}


def test_order_by(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = CustomerDevices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.order_by(order=Order.ASCENDING, order_by="os_version")

    # Then
    assert customer_devices_query._query_parameters == {"orderby": "+os_version"}


class SomeResource(Query):

    def __init__(self, session, url, **kwargs):
        super().__init__(session, url, **kwargs)


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
def serial_number_hash():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"


@pytest.fixture
def error_message():
    return "some_problem"


@pytest.fixture
def customer_device_status(customer_id, serial_number_hash):
    return {
        "after":
            None,
        "count":
            1,
        "total":
            1,
        "devices":
            [
                {
                    "customer_id": customer_id,
                    "serial_number_hash": serial_number_hash,
                    "enrolled": True,
                    "source": "kaseya",
                    "last_check_in": "2020-08-26T04:00:11.143+00:00",
                    "serial": "aSerial",
                    "healthy": False,
                    "attributes":
                        {
                            "hostname": {
                                "value": "one-device",
                                "last_update": "2020-08-26T04:00:14.845+00:00"
                            },
                            "serial": "aSerial",
                            "source_last_check_in": "2020-08-26T04:00:11.143+00:00"
                        }
                }
            ]
    }


@pytest.fixture
def customer_device_error(error_message):
    return {"message": "some_problem"}
