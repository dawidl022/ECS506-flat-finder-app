import json


def camel_case(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseEncoder(json.JSONEncoder):
    """
    Custom encoder that converts all snake_case object property names into
    camelCase to conform with the naming convention used in our API spec
    """

    def encode(self, obj: object) -> str:
        if isinstance(obj, list):
            return super().encode(
                [json.loads(self.encode(item)) for item in obj]
            )

        obj = {camel_case(k): v for k, v in obj.__dict__.items()}
        for key, value in obj.items():
            if hasattr(value, "__dict__"):
                obj[key] = json.loads(self.encode(value))
        return super().encode(obj)
