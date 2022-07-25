Using XOA Test Configuration Converter
===================================================

First, import ``xoa_core`` and ``xoa_converter`` into your Python code. If you haven't installed ``xoa-core`` Python package in your environment, please go to `XOA Core <https://github.com/xenanetworks/open-automation-core>`_.

.. code-block:: python

    from xoa_core import controller
    from xoa_converter.entry import converter
    from xoa_converter.types import TestSuiteType

Then, to use the converter, you need the target schema for the old file to be converted into:

.. code-block:: python

    core_ctrl = await controller.MainController() # create an instance of xoa core controller
    info = core_ctrl.get_test_suite_info("RFC-2544") # get 2544 test suite information from the core's registration
    target_schema = json.load(info['schema']) # get the target json schema

After that, simply provide the target schema, the old config file to the converter function and get the new config file:

.. literalinclude:: ../code_example/using_converter.py
    :language: python
    :linenos:
    :emphasize-lines: 3, 4, 5, 10, 11, 12, 15
