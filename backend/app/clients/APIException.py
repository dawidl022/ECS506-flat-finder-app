class APIException(Exception):
    def __init__(self, err: object = "") -> None:
        self.err: object = err


class APIUnreachableException(APIException):
    def __init__(self, err: object) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"API is unreachable. :{self.err}"


class APIKeyError(APIException):
    def __init__(self, err: object) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"API key is invalid, expired\
                or you are not subscribed. message:{self.err}"


class APIResponseError(APIException):
    def __init__(self, err: object) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"The API returned error: :{self.err}"


class APIRequestExecption(APIException):
    def __init__(self, err: object) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"There was a problem with the request :{self.err}"


class APIHTTPError(APIException):
    def __init__(self, err: object) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"HTTP Error occured :{self.err}"
