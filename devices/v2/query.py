from enum import Enum

from requests import HTTPError

from devices.errors import InvalidParamsError
from devices.v2.errors import APIDevicesV2Error
from devices.v2.schemas import (
    AssignmentResponse,
    AssignmentsRequestPayload,
    CreateAssignmentPayload,
    CreateMDMPayload,
    DevicesResponse,
    DownloadLinkResponse,
    MDMName,
    MDMResponse,
)


class DevicesV2Endpoint(str, Enum):
    DEVICES = "/v2/devices"
    DEVICE = "/v2/devices/{id}"
    DEVICE_ASSIGNMENT = "/v2/devices/{id}/assignment"
    # MDM
    MDM = "/v2/mdm"
    CUSTOMER_MDM = "/v2/mdm/{name}/{customer_id}"
    DOWNLOAD_LINK = "/v2/download-link/{customer_id}"
    # Assignments
    ASSIGNMENTS_REQUEST = "/v2/assignments/request"


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

    @property
    def session(self):
        return self._session

    @property
    def url(self):
        return self._url

    @property
    def query_parameters(self):
        return self._query_parameters

    def execute_request(self, resource, method="GET", schema=None, payload=None):
        url = f"{self._url}{resource}"
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=self._query_parameters,
                json=payload,
            )
            response.raise_for_status()
            return schema.load(response.json()) if schema else None
        except HTTPError as err:
            raise APIDevicesV2Error.wrap(err)


class Devices(Query):

    def __init__(self, session, url, customer_id):
        super().__init__(session, url)
        self._query_parameters["customerId"] = customer_id

    #jx
    def assigned_to(self, user_id):
        if user_id:
            self._query_parameters["assigned_to"] = user_id
        return self

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
        return self.execute_request(
            DevicesV2Endpoint.DEVICES,
            schema=DevicesResponse,
        )


class DeviceAssignment(Query):

    def __init__(self, session, url, host_identifier):
        super().__init__(session, url)
        self.host_identifier = host_identifier

    def get(self):
        resource = DevicesV2Endpoint.DEVICE_ASSIGNMENT.format(id=self.host_identifier)
        return self.execute_request(
            resource,
            method="GET",
            schema=AssignmentResponse,
        )

    def create(self, assigned_to, assigned_by):
        assignment = CreateAssignmentPayload(
            assigned_to=assigned_to,
            assigned_by=assigned_by,
        )
        resource = DevicesV2Endpoint.DEVICE_ASSIGNMENT.format(id=self.host_identifier)
        return self.execute_request(
            resource,
            method="PUT",
            payload=assignment.dump(),
        )

    def delete(self):
        resource = DevicesV2Endpoint.DEVICE_ASSIGNMENT.format(id=self.host_identifier)
        return self.execute_request(
            resource,
            method="DELETE",
        )


class Device(Query):

    def __init__(self, session, url, customer_id, device_id):
        super().__init__(session, url)
        self.device_id = device_id
        self.customer_id = customer_id

    def _host_identifier(self):
        return f"{self.customer_id}::{self.device_id}"

    def assignment(self) -> DeviceAssignment:
        return DeviceAssignment(
            session=self._session,
            url=self._url,
            host_identifier=self._host_identifier(),
        )


class MDM(Query):

    def __init__(self, session, url, customer_id):
        super().__init__(session, url)
        self.customer_id = customer_id

    def get(self, name):
        if name not in list(MDMName):
            raise InvalidParamsError(f"MDM name should be one of {list(MDMName)}")

        resource = DevicesV2Endpoint.CUSTOMER_MDM.format(
            name=name,
            customer_id=self.customer_id,
        )
        return self.execute_request(
            resource=resource,
            method="GET",
            schema=MDMResponse,
        )

    def create(self, name):
        if name not in list(MDMName):
            raise InvalidParamsError(f"MDM name should be one of {list(MDMName)}")

        create_mdm_payload = CreateMDMPayload(customer_id=self.customer_id, name=name)
        return self.execute_request(
            resource=DevicesV2Endpoint.MDM,
            method="POST",
            payload=create_mdm_payload.dump(),
            schema=MDMResponse,
        )


class DownloadLink(Query):

    def __init__(self, session, url, customer_id):
        super().__init__(session, url)
        self.customer_id = customer_id

    def get(self):
        resource = DevicesV2Endpoint.DOWNLOAD_LINK.format(customer_id=self.customer_id)
        return self.execute_request(
            resource=resource,
            method="GET",
            schema=DownloadLinkResponse,
        )


class Assignment(Query):

    def __init__(self, session, url, customer_id, employee_ids):
        super().__init__(session, url)
        self.customer_id = customer_id
        self.employee_ids = employee_ids

    def request(self):
        request = AssignmentsRequestPayload(
            customer_id=self.customer_id,
            employee_ids=self.employee_ids,
        )
        resource = DevicesV2Endpoint.ASSIGNMENTS_REQUEST
        return self.execute_request(
            resource=resource,
            method="POST",
            payload=request.dump(),
        )
