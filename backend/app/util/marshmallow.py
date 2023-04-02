from enum import StrEnum
from http.client import BAD_REQUEST
from typing import Type, TypeVar
import dacite

from flask import abort, make_response, request

from app.util.schema import Schemable


T = TypeVar('T', bound=Schemable)


def get_params(type: Type[T]) -> T:
    error = type.schema.validate(request.args)
    if error:
        abort(make_response(error, BAD_REQUEST))
    params = dacite.from_dict(
        data_class=type,
        data=request.args,
        config=dacite.Config(cast=[float, int, StrEnum])
    )

    return params
