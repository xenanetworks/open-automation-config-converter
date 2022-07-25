from types import ModuleType
from typing import Type, Protocol
from xoa_converter import exceptions
from xoa_converter import types
from .common import TestParameters
from .rfc2544.adapter import Converter2544


class XoaConverter(Protocol):
    def __init__(self, source_config: str, target_module: ModuleType) -> None: ...
    def gen(self) -> "TestParameters": ...


def get_converter(test_suite_type: types.TestSuiteType) -> Type[XoaConverter]:
    """Selecting and returning Converter"""
    if test_suite_type == types.TestSuiteType.RFC2544:
        return Converter2544
    raise exceptions.UnknowConverterType(test_suite_type)