from typing import Any, Type, Protocol, Dict
from xoa_converter import exceptions
from xoa_converter import types
from .rfc2544.adapter import Converter2544
from .rfc3918.adapter import Converter3918
from .rfc2889.adapter import Converter2889
from .y1564.adapter import Converter1564


class XoaConverter(Protocol):
    def __init__(self, source_config: str) -> None: ...
    def gen(self) -> Dict[str, Any]: ...


CONVERTER_MAPPING: Dict[types.TestSuiteType, Type[XoaConverter]] = {
    types.TestSuiteType.RFC2544: Converter2544,
    types.TestSuiteType.RFC3918: Converter3918,
    types.TestSuiteType.RFC2889: Converter2889,
    types.TestSuiteType.Y1564: Converter1564,
}


def get_converter(test_suite_type: types.TestSuiteType) -> Type[XoaConverter]:
    """Selecting and returning Converter"""
    converter = CONVERTER_MAPPING.get(test_suite_type)
    if not converter:
        raise exceptions.UnknowConverterType(test_suite_type)
    return converter