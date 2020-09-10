from devices.auth import Auth0Bearer
from devices.errors import InvalidParamsError
from devices.v1.query import CustomerDevices
from requests import Session


class DevicesV1API:

    def __init__(self, url, auth_token):
        self._url = url
        self._session = self._new_session(auth_token)

    @staticmethod
    def _new_session(auth_token):
        session = Session()
        session.auth = Auth0Bearer(auth_token)
        return session

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._session.close()

    def get_devices(self, customer_id) -> CustomerDevices:
        if not customer_id:
            raise InvalidParamsError("No customer id set to query API-devices")

        return CustomerDevices(
            session=self._session,
            url=self._url,
            customer_id=customer_id,
        )
