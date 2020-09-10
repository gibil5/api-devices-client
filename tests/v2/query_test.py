from http import HTTPStatus

import pytest
import responses
from devices.v2.errors import APIDevicesV2Error
from devices.v2.query import Devices, FilterByOperator, Order, Query
from devices.v2.schemas import DeviceResponse
from requests import Session
from tests.mocks.response import http_200_callback, http_400_callback

_APP_JSON = {"Accept": "*/*"}


@responses.activate
def test_execute_query_success(url, customer_id, customer_device_status):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    expected_endpoint = f"/v2/devices"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_200_callback(body=customer_device_status, request_headers=_APP_JSON)
    )
    # When
    response = customer_devices_query.all()

    # Then
    assert response.dumps() == DeviceResponse.load(customer_device_status).dumps()


@responses.activate
def test_execute_query_error(url, customer_id):
    # Given

    code = "some_code_from_api"
    detail = "exploded"
    source = {"extra": "detail", "api_devices_went": "boom boom"}

    error_response = dict(code=code, detail=detail, source=source)

    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    expected_endpoint = f"/v2/devices"
    expected_url = f"{url}{expected_endpoint}"
    responses.add_callback(
        responses.GET, expected_url, callback=http_400_callback(body=error_response, request_headers=_APP_JSON)
    )

    # When/Then
    with pytest.raises(APIDevicesV2Error) as err_info:
        _ = customer_devices_query.all()

    err = err_info.value
    assert err.status_code == HTTPStatus.BAD_REQUEST
    assert err.code == code
    assert err.detail == detail
    assert err.source == source
    assert str(err) == f"({code}) {detail}"


def test_create_customer_devices_success(customer_id, url):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # Then
    assert customer_devices_query._session == session
    assert customer_devices_query._url == url
    assert customer_devices_query._query_parameters["customerId"] == customer_id


def test_filter_by(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.filter_by(bitlocker=True, firewall=True)

    # Then
    params = customer_devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["filterby"] == "bitlocker:true,firewall:true"


def test_filter_by_operator(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.filter_by_operator(FilterByOperator.AND)

    # Then
    params = customer_devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["filterbyOperator"] == "and"


def test_limit(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.limit(2)

    # Then
    params = customer_devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["limit"] == 2


def test_after(url, customer_id, device_id):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.after(device_id)

    # Then
    params = customer_devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["after"] == device_id


def test_order_by(url, customer_id):
    # Given
    session = Session()
    customer_devices_query = Devices(session, url, customer_id=customer_id)

    # When
    customer_devices_query.order_by(order=Order.ASCENDING, order_by="os_version")

    # Then
    params = customer_devices_query._query_parameters
    assert params["customerId"] == customer_id
    assert params["orderby"] == "+os_version"


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
def device_id():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"


@pytest.fixture
def customer_device_status(customer_id, device_id):
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
                    "hostname": "one-device",
                    "healthy": False,
                    "created_at": "2020-07-25T04:00:11.143+00:00",
                    "updated_at": "2020-08-25T04:00:11.143+00:00",
                }
            ]
    }
