class APIException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = [*args];

class APIUnreachableException(APIException):
    def __str__(self):
        return f"API is unreachable."
    
class APIKeyError(APIException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"API key is invalid, expired or you are not subscribed. message:{self.args}"
    
class APIResponseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return f"The API returned error: :{self.args}"
    