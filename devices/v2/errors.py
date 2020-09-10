from devices.v2.schemas import ErrorResponse
from marshmallow import ValidationError
from requests import HTTPError


class APIDevicesV2Error(Exception):
    code: str = None
    detail: str = None
    source: dict = None
    status_code: int = None

    def __init__(self, code, detail, source, status_code):
        if code:
            self.code = code

        if detail:
            self.detail = detail

        if source:
            self.source = source

        if status_code:
            self.status_code = status_code

        message = f"({code}) {detail}"
        super().__init__(message)

    @classmethod
    def wrap(cls, http_error: HTTPError):
        """
        This method wraps the v1 error message
        """

        try:
            error = ErrorResponse.load(http_error.response.json())
            code = error.code
            detail = error.detail
            source = error.source
        except ValidationError:
            code = "unknown"
            detail = str(http_error)
            source = None

        status_code = http_error.response.status_code

        return cls(code=code, detail=detail, source=source, status_code=status_code)
