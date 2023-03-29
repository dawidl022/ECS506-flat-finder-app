
import abc
from marshmallow import Schema


class Schemable(abc.ABC):
    schema: Schema


def camel_case(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camel_case(field_obj.data_key or field_name)
