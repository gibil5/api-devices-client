from devices.auth import Auth0Bearer
from devices.errors import InvalidParamsError
from devices.v2.query import MDM, Device, Devices
from requests import Session


class DevicesV2API:

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

    def devices(self, customer_id) -> Devices:
        if not customer_id:
            raise InvalidParamsError("No customer id set to query API-devices")

        return Devices(
            session=self._session,
            url=self._url,
            customer_id=customer_id,
        )

    def device(self, customer_id, device_id):

        if not (customer_id and device_id):
            raise InvalidParamsError("Both customer_id and device_id are needed to query API-Devices")

        return Device(session=self._session, url=self._url, customer_id=customer_id, device_id=device_id)

    def mdm(self, customer_id):
        if not customer_id:
            raise InvalidParamsError("customer_id is needed to query API-devices")

        return MDM(session=self._session, url=self._url, customer_id=customer_id)
