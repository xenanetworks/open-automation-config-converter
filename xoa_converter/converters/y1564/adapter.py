from typing import Any, Dict

from loguru import logger

from .model import (
    ValkyrieConfiguration1564,
)

class Converter1564:
    def gen(self) -> Dict[str, Any]:
        return {}

    def __init__(self, source_config: str) -> None:
        old_model = ValkyrieConfiguration1564.parse_raw(source_config)
        logger.debug(old_model)