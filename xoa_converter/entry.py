from .converters import fabric
from . import types
from . import _generator


def converter(test_suite_type: types.TestSuiteType, source_config: types.JsonStr, target_schema: types.JsonStr) -> str:
    """Convert an Valkyrie test suite application's config file into XOA's test suite config.

    :param test_suite_type: Registered test suite type.
    :type test_suite_type: types.TestSuiteType
    :param source_config:  Old application config data from .v2544, .v3918, .v2889, or .v1564 files.
    :type source_config: types.JsonStr
    :param target_schema: Target JSON schema
    :type target_schema: types.JsonStr
    :return: JSON string of the converted config file
    :rtype: str
    """
    converter_class = fabric.get_converter(test_suite_type)
    target_module = _generator.gen_target_module(target_schema)
    _model = converter_class(
        source_config=source_config, 
        target_module=target_module
    ).gen()
    return _model.json(indent=2)