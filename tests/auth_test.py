import pytest
from devices.auth import Auth0Bearer
from devices.errors import InvalidTokenError


def test_bearer_token_creation_success(auth_token):
    # Given / When
    auth0_bearer = Auth0Bearer(auth_token)
    some_request = Request()
    auth0_bearer(some_request)

    # Then
    assert some_request.headers["Authorization"] == f"Bearer {auth_token}"


def test_missing_token():
    # Given / When
    with pytest.raises(InvalidTokenError):
        _ = Auth0Bearer(token=None)


@pytest.fixture
def auth_token():
    return "aRandomBearerTokenForAuth0Authentication"


class Request:
    headers: dict = {}
