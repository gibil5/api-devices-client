import pytest
from devices.errors import InvalidParamsError, InvalidTokenError
from devices.v2.client import DevicesV2API
from devices.v2.query import MDM, Device, Devices, Query
from requests import Session


def test_client_session_creation_success(url, auth_token):
    # Given / When
    with DevicesV2API(url, auth_token) as devices:
        assert devices._session.auth.token == auth_token
        assert devices._url == url
        assert isinstance(devices._session, Session)


def test_client_session_invalid_token(url):
    with pytest.raises(InvalidTokenError):
        with DevicesV2API(url, auth_token=None) as _:
            pass


def test_devices(url, auth_token):
    # Given
    customer_id = "224656a5-c95e-4de9-a845-237e9207f348"

    with DevicesV2API(url, auth_token) as devices:
        # When
        customer_devices = devices.devices(customer_id=customer_id)

    # Then
    assert isinstance(customer_devices, Devices)
    assert customer_devices._session == devices._session
    assert customer_devices._url == devices._url
    assert customer_devices._query_parameters["customerId"] == customer_id


def test_devices_missing_customer_id(url, auth_token):
    # Given
    customer_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.devices(customer_id=customer_id)


def test_device(url, auth_token):
    # Given
    customer_id = "224656a5-c95e-4de9-a845-237e9207f348"
    device_id = "0cc175b9c0f1b6a831c399e269772661"

    with DevicesV2API(url, auth_token) as devices:
        # When
        device_query = devices.device(customer_id=customer_id, device_id=device_id)

    # Then
    assert isinstance(device_query, Device)
    assert device_query._session == devices._session
    assert device_query._url == devices._url
    assert device_query.customer_id == customer_id
    assert device_query.device_id == device_id


def test_device_missing_customer_id(url, auth_token):
    # Given
    customer_id = None
    device_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.device(customer_id=customer_id, device_id=device_id)


# Scenarios for MDM:
# Scenario 01: Create MDM Query
# Scenario 02: Create MDM Query Invalid params
# Scenario 03: Create MDM Invalid MDM name
def test_mdm(url, auth_token, customer_id):
    # Given
    mdm_name = "kaseya"
    with DevicesV2API(url, auth_token) as devices:
        # When
        customer_mdm = devices.mdm(customer_id=customer_id)

        # Then
    assert isinstance(customer_mdm, MDM)
    assert customer_mdm._session == devices._session
    assert customer_mdm._url == devices._url

    assert customer_mdm.customer_id == customer_id


def test_mdm_missing_customer_id(url, auth_token):
    # Given
    customer_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.mdm(customer_id=customer_id)


@pytest.fixture
def customer_id():
    return "9a919a42-b506-49ee-b053-402827b761b7"


@pytest.fixture
def url():
    return "http://someurlrandom.com.ar"


@pytest.fixture
def auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


class SomeResource(Query):

    def __init__(self, session, url):
        super().__init__(session, url)


class InvalidResource:
    pass
