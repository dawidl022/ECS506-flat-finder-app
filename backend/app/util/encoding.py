from enum import StrEnum
import json
import re
from uuid import UUID


def camel_case(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def snake_case(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


class CamelCaseEncoder(json.JSONEncoder):
    """
    Custom encoder that converts all snake_case object property names into
    camelCase to conform with the naming convention used in our API spec
    """

    def encode(self, obj: object) -> str:
        if obj is None or isinstance(obj, (StrEnum, str, int, float, UUID)):
            return super().encode(obj)

        if isinstance(obj, list):
            return super().encode(
                [json.loads(self.encode(item)) for item in obj]
            )

        if isinstance(obj, dict):
            obj = {camel_case(k): v for k, v in obj.items()}
        else:
            obj = {camel_case(k): v for k, v in obj.__dict__.items()}

        for key, value in obj.items():
            obj[key] = json.loads(self.encode(value))

        return super().encode(obj)


class CamelCaseDecoder(json.JSONDecoder):
    """
    Custom encoder that converts all snake_case object property names into
    camelCase to conform with the naming convention used in our API spec
    """

    def decoder(self, s: str) -> object:
        obj = super().decode(s)
        return self.snake_casify(obj)

    @staticmethod
    def snake_casify(obj: object) -> object:
        if isinstance(obj, list):
            return [CamelCaseDecoder.snake_casify(item) for item in obj]

        if isinstance(obj, dict):
            obj = {snake_case(k): v for k, v in obj.items()}
        else:
            obj = {snake_case(k): v for k, v in obj.__dict__.items()}

        for key, value in obj.items():
            if hasattr(value, "__dict__"):
                obj[key] = CamelCaseDecoder.snake_casify(obj[key])
        return obj
