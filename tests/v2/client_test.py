import pytest
from devices.errors import InvalidParamsError, InvalidTokenError
from devices.v2.client import DevicesV2API
from devices.v2.query import (
    MDM,
    Assignment,
    Device,
    Devices,
    DownloadLink,
    Query,
)
from requests import Session


def test_client_session_creation_success(url, auth_token):
    # Given / When
    with DevicesV2API(url, auth_token) as devices:
        assert devices.session.auth.token == auth_token
        assert devices.url == url
        assert isinstance(devices.session, Session)


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
    assert customer_devices.session == devices.session
    assert customer_devices.url == devices.url
    assert customer_devices.query_parameters["customerId"] == customer_id


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
    assert device_query.session == devices.session
    assert device_query.url == devices.url
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
    with DevicesV2API(url, auth_token) as devices:
        # When
        customer_mdm = devices.mdm(customer_id=customer_id)

        # Then
    assert isinstance(customer_mdm, MDM)
    assert customer_mdm.session == devices.session
    assert customer_mdm.url == devices.url
    assert customer_mdm.customer_id == customer_id


def test_mdm_missing_customer_id(url, auth_token):
    # Given
    customer_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.mdm(customer_id=customer_id)


# Scenarios for DownloadLink
# Scenario 01: Create DownloadLink query
# Scenario 02: Invalid params
def test_download_link(url, auth_token, customer_id):
    # Given
    with DevicesV2API(url, auth_token) as devices:
        # When
        download_link = devices.download_link(customer_id=customer_id)

    # Then
    assert isinstance(download_link, DownloadLink)
    assert download_link.session == devices.session
    assert download_link.url == devices.url
    assert download_link.customer_id == customer_id


def test_download_link_missing_customer_id(url, auth_token):
    # Given
    customer_id = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.download_link(customer_id=customer_id)


# Scenarios for Assignment
# Scenario 01: Create Assignment query
# Scenario 02: Invalid params
def test_assignment(url, auth_token, customer_id, employee_ids):
    # Given
    with DevicesV2API(url, auth_token) as devices:
        # When
        assignment = devices.assignments(
            customer_id=customer_id,
            employee_ids=employee_ids,
        )

    # Then
    assert isinstance(assignment, Assignment)
    assert assignment.session == devices.session
    assert assignment.url == devices.url
    assert assignment.customer_id == customer_id
    assert assignment.employee_ids == employee_ids


def test_assignment_missing_employee_ids(url, auth_token, customer_id):
    # Given
    employee_ids = None

    with DevicesV2API(url, auth_token) as devices:
        # When/Then
        with pytest.raises(InvalidParamsError):
            _ = devices.assignments(
                customer_id=customer_id,
                employee_ids=employee_ids,
            )


@pytest.fixture(name="customer_id")
def get_customer_id():
    return "9a919a42-b506-49ee-b053-402827b761b7"


@pytest.fixture(name="employee_ids")
def get_employee_ids():
    return [
        "25938eac-f148-45a0-bf5b-620b373c59e1",
        "8a46f176-7db2-403d-bf40-ea91146f8e76",
    ]


@pytest.fixture(name="url")
def get_url():
    return "http://someurlrandom.com.ar"


@pytest.fixture(name="auth_token")
def get_auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


class SomeResource(Query):  # pylint: disable=too-few-public-methods
    """
    No need to re-define __init__ here since by default Python will look for
    the parent's __init__ method when it's not present in the child class.
    """


class InvalidResource:  # pylint: disable=too-few-public-methods
    pass
