import functools
import json
from http import HTTPStatus


def _get_request_body(request):
    content_type = request.headers["Content-Type"]
    if content_type == "application/json":
        return json.loads(request.body)
    return request.body


def _transform(body, headers):
    headers = headers or {}
    if body is not None:
        if isinstance(body, dict):
            body = json.dumps(body)
            headers["Content-Type"] = "application/json"
        elif isinstance(body, str):
            headers["Content-Type"] = "text/xml"
        else:
            raise ValueError(f"Not supported type for body: {type(body)}")
    else:
        body = ""
    return body, headers


# pylint: disable=too-many-arguments
def _http_callback(status_code, headers=None, body=None, request_body=None, request_headers=None, request_params=None):
    # Define values for response parameters
    body, headers = _transform(body, headers)

    # Define values for request parameters
    request_headers = request_headers or {}
    request_params = request_params or {}

    def request_callback(request):
        # Assert that the request header is the expected one
        for header, param_expected_value in request_headers.items():
            assert request.headers.get(header) == param_expected_value

        # Assert that the request body is the expected one
        if request_body:
            assert _get_request_body(request) == request_body

        # Assert that the request params are the expected ones
        for param_name, param_expected_value in request_params.items():
            assert request.get(param_name) == param_expected_value

        return status_code, headers, body

    return request_callback


http_200_callback = functools.partial(_http_callback, status_code=HTTPStatus.OK)
http_201_callback = functools.partial(_http_callback, status_code=HTTPStatus.CREATED)
http_204_callback = functools.partial(_http_callback, status_code=HTTPStatus.NO_CONTENT)
http_400_callback = functools.partial(_http_callback, status_code=HTTPStatus.BAD_REQUEST)
http_401_callback = functools.partial(_http_callback, status_code=HTTPStatus.UNAUTHORIZED)
http_500_callback = functools.partial(_http_callback, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
