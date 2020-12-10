from enum import Enum

from devices.errors import InvalidParamsError
from devices.v2.errors import APIDevicesV2Error
from devices.v2.schemas import (
    AssignmentResponse,
    CreateAssignmentPayload,
    CreateMDMPayload,
    DevicesResponse,
    MDMName,
    MDMResponse,
)
from requests import HTTPError


class DevicesV2Endpoints(str, Enum):

    # Devices
    devices = "/v2/devices"
    device = "/v2/devices/%s"
    device_assignment = "/v2/devices/%s/assignment"

    # MDM
    customer_mdm = "/v2/mdm/{name}/{customer_id}"
    mdm = "/v2/mdm"


class FilterByOperator(str, Enum):
    AND = "and"
    OR = "or"


class Order(str, Enum):
    ASCENDING = "+"
    DESCENDING = "-"


class Query:  # pylint: disable=too-few-public-methods

    def __init__(self, session, url):
        self._session = session
        self._url = url
        self._query_parameters = {}

    def execute_request(self, resource, method="GET", schema=None, payload=None):
        url = f"{self._url}{resource}"
        try:
            response = self._session.request(method=method, url=url, params=self._query_parameters, json=payload)
            response.raise_for_status()
            return schema.load(response.json()) if schema else None
        except HTTPError as err:
            raise APIDevicesV2Error.wrap(err)


class Devices(Query):

    def __init__(self, session, url, customer_id):
        super().__init__(session, url)
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

    def all(self) -> DevicesResponse:
        return self.execute_request(DevicesV2Endpoints.devices, schema=DevicesResponse)


class DeviceAssignment(Query):

    def __init__(self, session, url, host_identifier):
        self.host_identifier = host_identifier
        super().__init__(session, url)

    def get(self):
        resource = DevicesV2Endpoints.device_assignment % self.host_identifier
        return self.execute_request(resource, method="GET", schema=AssignmentResponse)

    def create(self, assigned_to, assigned_by):
        assignment = CreateAssignmentPayload(assigned_to=assigned_to, assigned_by=assigned_by)

        resource = DevicesV2Endpoints.device_assignment % self.host_identifier
        return self.execute_request(resource, method="PUT", payload=assignment.dump())

    def delete(self):
        resource = DevicesV2Endpoints.device_assignment % self.host_identifier
        return self.execute_request(
            resource,
            method="DELETE",
        )


class Device(Query):

    def __init__(self, session, url, customer_id, device_id):
        super().__init__(session, url)
        self.customer_id = customer_id
        self.device_id = device_id

    def _host_identifier(self):
        return f"{self.customer_id}::{self.device_id}"

    def assignment(self) -> DeviceAssignment:
        return DeviceAssignment(session=self._session, url=self._url, host_identifier=self._host_identifier())


class MDM(Query):

    def __init__(self, session, url, customer_id):
        super().__init__(session, url)
        self.customer_id = customer_id

    def get(self, name):
        if name not in list(MDMName):
            raise InvalidParamsError(f"MDM name should be one of {list(MDMName)}")
        resource = DevicesV2Endpoints.customer_mdm.format(name=name, customer_id=self.customer_id)
        return self.execute_request(resource=resource, method="GET", schema=MDMResponse)

    def create(self, name):
        if name not in list(MDMName):
            raise InvalidParamsError(f"MDM name should be one of {list(MDMName)}")
        create_mdm_payload = CreateMDMPayload(customer_id=self.customer_id, name=name)
        return self.execute_request(
            resource=DevicesV2Endpoints.mdm, method="POST", payload=create_mdm_payload.dump(), schema=MDMResponse
        )
