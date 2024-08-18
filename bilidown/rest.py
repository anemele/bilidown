from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from mashumaro.mixins.orjson import DataClassORJSONMixin

T = TypeVar('T')


@dataclass
class Rest(
    Generic[T],
    DataClassORJSONMixin,
):
    code: int
    message: str
    ttl: int
    data: T


# See the runtime bug
# https://github.com/Fatal1ty/mashumaro/issues/86#issuecomment-1325304599
def loads_rest(content: bytes, cls: Type[T]) -> Rest[T]:
    class Model(Rest[cls]):
        pass

    return Model.from_json(content)
