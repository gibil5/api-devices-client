from datetime import datetime, timedelta

import requests

#from proxy_flare.settings import (
from devices.settings import (
    AUTH0_AUDIENCE,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_GRANT_TYPE,
    AUTH0_URL,
)
#from proxy_flare.utils import timed_request
from devices.utils import timed_request


class Auth0Client:
    _singleton = None
    _access_token = None
    _expiration_date = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = object.__new__(Auth0Client)
        return cls._singleton

    def _token_is_valid(self):
        return not (self._access_token is None or self._expiration_date is None) \
               and self._expiration_date > datetime.now()  # and not DEBUG

    @timed_request
    def _request_token(self):
        start_time = datetime.now()

        # Make the Auth0 Post
        url = AUTH0_URL
        payload = {
            'grant_type': AUTH0_GRANT_TYPE,
            'client_id': AUTH0_CLIENT_ID,
            'client_secret': AUTH0_CLIENT_SECRET,
            'audience': AUTH0_AUDIENCE
        }
        response = requests.post(url, data=payload)

        if response.ok:
            parsed_response = response.json()
            self._access_token = parsed_response.get('access_token', None)

            expires_in = parsed_response.get('expires_in', 86400)
            self._expiration_date = start_time + timedelta(seconds=expires_in)
            return self._access_token
        else:
            raise Exception('Failed to get Auth0 Token')

    @property
    def token(self):
        return self._access_token if self._token_is_valid() else self._request_token()
