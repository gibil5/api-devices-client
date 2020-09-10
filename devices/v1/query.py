from enum import Enum

from devices.v1.errors import APIDevicesV1Error
from devices.v1.schemas import CustomerDeviceStatus
from requests import HTTPError


class DevicesV1Endpoints(Enum):
    customer_devices_status = "/customers/%s/devices/status"


class FilterByOperator(Enum):
    AND = "and"
    OR = "or"


class Order(Enum):
    ASCENDING = "+"
    DESCENDING = "-"


class Query:  # pylint: disable=too-few-public-methods
    endpoint = None
    schema = None

    def __init__(self, session, url, **_):
        self._session = session
        self._url = url
        self._query_parameters = {}

    def execute_query(self, resource):
        url = f"{self._url}{resource}"
        try:
            response = self._session.get(url=url, params=self._query_parameters)
            response.raise_for_status()
            return self.schema.load(response.json())
        except HTTPError as err:
            raise APIDevicesV1Error.wrap(err)


class CustomerDevices(Query):
    endpoint = DevicesV1Endpoints.customer_devices_status.value
    schema = CustomerDeviceStatus

    def __init__(self, session, url, customer_id, **kwargs):
        self._customer_id = customer_id
        super().__init__(session, url, **kwargs)

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
            self._query_parameters["orderby"] = f"{order.value}{order_by}"
        return self

    def all(self):
        resource = self.endpoint % self._customer_id
        return self.execute_query(resource)
