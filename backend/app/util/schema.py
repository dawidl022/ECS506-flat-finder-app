
import abc
import json
from marshmallow import Schema


class Schemable(abc.ABC):
    schema: Schema


def camel_case(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camel_case(field_obj.data_key or field_name)


class CamelCaseEncoder(json.JSONEncoder):
    """
    Custom encoder that converts all snake_case object property names into
    camelCase to conform with the naming convention used in our API spec
    """

    def encode(self, obj: object):
        obj = {camel_case(k): v for k, v in obj.__dict__.items()}
        for key, value in obj.items():
            if hasattr(value, "__dict__"):
                obj[key] = json.loads(self.encode(value))
        return super().encode(obj)
