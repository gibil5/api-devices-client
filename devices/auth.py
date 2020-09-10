from devices.errors import InvalidTokenError
from requests.auth import AuthBase


class Auth0Bearer(AuthBase):

    def __init__(self, token):
        self.token = token
        if not token:
            raise InvalidTokenError("No token set to query API-devices")

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
