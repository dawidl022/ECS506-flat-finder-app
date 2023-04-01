
import abc
from marshmallow import Schema
from marshmallow.fields import Field

from app.util.encoding import camel_case


class Schemable(abc.ABC):
    schema: Schema


class CamelCaseSchema(Schema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        field_obj.data_key = camel_case(field_obj.data_key or field_name)
