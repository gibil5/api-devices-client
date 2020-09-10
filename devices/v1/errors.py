from json.decoder import JSONDecodeError

from requests import HTTPError


class APIDevicesV1Error(Exception):
    error: str = None
    detail: dict = None
    status_code: int = None

    def __init__(self, error, detail, status_code):
        if error:
            self.error = error

        if detail:
            self.detail = detail

        if status_code:
            self.status_code = status_code

        message = f"(api_devices_error) {error}"
        super().__init__(message)

    @classmethod
    def wrap(cls, http_error: HTTPError):
        """
        This method wraps the v1 error message
        """

        try:
            detail = http_error.response.json()
        except JSONDecodeError:
            detail = {}

        error = str(http_error)
        status_code = http_error.response.status_code

        return cls(error=error, detail=detail, status_code=status_code)
