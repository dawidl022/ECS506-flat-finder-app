from enum import StrEnum
from http.client import BAD_REQUEST
from typing import Any, Type, TypeVar, cast
from flask import abort, make_response, request
import dacite

from app.util.schema import Schemable
from app.util.encoding import CamelCaseDecoder


T = TypeVar('T', bound=Schemable)


def _get_input(type: Type[T], data: dict[str, Any]) -> T:
    error = type.schema.validate(data)
    if error:
        abort(make_response(error, BAD_REQUEST))
    model = dacite.from_dict(
        data_class=type,
        data=data,
        config=dacite.Config(cast=[float, int, StrEnum])
    )

    return model


def get_params(type: Type[T]) -> T:
    return _get_input(type, request.args)


def get_form(type: Type[T]) -> T:
    form = cast(dict[str, str], CamelCaseDecoder.snake_casify(request.form))
    return _get_input(type, form)


def get_input(type: Type[T], input: dict[str, str]) -> T:
    form = cast(dict[str, str], CamelCaseDecoder.snake_casify(input))
    return _get_input(type, form)
