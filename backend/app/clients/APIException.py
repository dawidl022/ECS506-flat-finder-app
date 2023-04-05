class APIException(Exception):
    def __init__(self, err: str="") -> None:
        self.err: str = err;

class APIUnreachableException(APIException):
    def __str__(self) -> str:
        return f"API is unreachable."
    
class APIKeyError(APIException):
    def __init__(self, err: str) -> None:
        super().__init__(err)

    def __str__(self) -> str:
        return f"API key is invalid, expired or you are not subscribed. message:{self.err}"
    
class APIResponseError(APIException):
    def __init__(self, err: str) -> None:
        super().__init__(err)
    
    def __str__(self) -> str:
        return f"The API returned error: :{self.err}"
    