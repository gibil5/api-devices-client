import pytest

from devices.auth0 import Auth0Client


@pytest.fixture(name="customer_id", scope="session")
def get_customer_id():
    return "9a919a42-b506-49ee-b053-402827b761b7"


@pytest.fixture(name="device_id", scope="session")
def get_device_id():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"


@pytest.fixture(name="device_id_staging", scope="session")
def get_device_id_staging():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"


@pytest.fixture(name="user_id", scope="session")
def get_user_id():
    return "cd4b0d93-1012-4821-ad96-458a8e96cb65"


@pytest.fixture(name="url_staging", scope="session")
def get_url_staging():
    return "https://devices-staging.electric.ai/staging"


@pytest.fixture(name="auth_token_staging", scope="session")
def get_auth_token_staging():
    # Authentication.
    # This instantiation is using a singleton, thus this is not creating a new object
    auth_client = Auth0Client()
    return auth_client.token
