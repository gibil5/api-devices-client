from enum import Enum

from devices.v2.errors import APIDevicesV2Error
from devices.v2.schemas import DeviceResponse
from requests import HTTPError


class DevicesV2Endpoints(str, Enum):
    devices = "/v2/devices"
    device_assignment = "/v2/devices/%s/assignment"


class FilterByOperator(str, Enum):
    AND = "and"
    OR = "or"


class Order(str, Enum):
    ASCENDING = "+"
    DESCENDING = "-"


class Query:  # pylint: disable=too-few-public-methods
    endpoint = None
    schema = None

    def __init__(self, session, url, **_):
        self._session = session
        self._url = url
        self._query_parameters = {}

    def execute_request(self, resource, method="GET"):
        url = f"{self._url}{resource}"
        try:
            response = self._session.request(method=method, url=url, params=self._query_parameters)
            response.raise_for_status()
            return self.schema.load(response.json())
        except HTTPError as err:
            raise APIDevicesV2Error.wrap(err)


class Devices(Query):
    endpoint = DevicesV2Endpoints.devices
    schema = DeviceResponse

    def __init__(self, session, url, customer_id, **kwargs):
        super().__init__(session, url, **kwargs)
        self._query_parameters["customerId"] = customer_id

    def filter_by(self, **kwargs):
        if kwargs:
            filters = [f"{filter_param}:{str(value)}" for filter_param, value in kwargs.items()]
            filter_by_param = ",".join(filters)
            self._query_parameters["filterby"] = filter_by_param.lower()
        return self

    def filter_by_operator(self, operator: FilterByOperator):
        if operator:
            self._query_parameters["filterbyOperator"] = operator.value
        return self

    def limit(self, limit):
        if limit:
            self._query_parameters["limit"] = limit
        return self

    def after(self, after):
        if after:
            self._query_parameters["after"] = after
        return self

    def order_by(self, order: Order, order_by):
        if order_by and order:
            # In the v2 API we've decided to change the api param to 
            # sort by. We still have the signature method as order by
            # until v1 is totally deprecated. 
            self._query_parameters["sortby"] = f"{order.value}{order_by}"
        return self

    def all(self) -> DeviceResponse:
        return self.execute_request(self.endpoint)
