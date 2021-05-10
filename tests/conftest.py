import pytest


@pytest.fixture(name="customer_id", scope="session")
def get_customer_id():
    return "9a919a42-b506-49ee-b053-402827b761b7"


@pytest.fixture(name="device_id", scope="session")
def get_device_id():
    return "9c9a7ce5b2fca4658633800bf9cd9d6e"
