import pytest
from devices.errors import InvalidParamsError, InvalidTokenError
from devices.v2.client import DevicesV2API
from devices.v2.query import Devices, Query
from requests import Session


def test_devices_session_creation_success(url, auth_token):
    # Given / When
    with DevicesV2API(url, auth_token) as devices:
        assert devices._session.auth.token == auth_token
        assert devices._url == url
        assert isinstance(devices._session, Session)


def test_devices_session_invalid_token(url):
    with pytest.raises(InvalidTokenError):
        with DevicesV2API(url, auth_token=None) as _:
            pass


def test_get_get_devices(url, auth_token):
    # Given
    customer_id = "224656a5-c95e-4de9-a845-237e9207f348"

    with DevicesV2API(url, auth_token) as devices:
        # When
        customer_devices = devices.get_devices(customer_id=customer_id)

    # Then
    assert isinstance(customer_devices, Devices)
    assert customer_devices._session == devices._session
    assert customer_devices._url == devices._url
    assert customer_devices._query_parameters["customerId"] == customer_id


def test_get_get_devices_missing_customer_id(url, auth_token):
    # Given
    customer_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.get_devices(customer_id=customer_id)


@pytest.fixture
def url():
    return "http://someurlrandom.com.ar"


@pytest.fixture
def auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


class SomeResource(Query):

    def __init__(self, session, url, **kwargs):
        super().__init__(session, url, **kwargs)


class InvalidResource:
    pass
