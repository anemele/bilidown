import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__file__)


@dataclass
class REST:
    code: int
    message: str
    ttl: int
    data: Any


def loads_rest(content: bytes, cls) -> REST:
    logger.debug(content)
    data = json.loads(content)
    rest: REST = REST(**data)
    rest.data = cls(**rest.data)
    return rest
