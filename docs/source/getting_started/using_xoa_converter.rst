Using XOA Test Configuration Converter
===================================================

First, import ``xoa_core`` and ``xoa_converter`` into your Python code. If you haven't installed ``xoa-core`` Python package in your environment, please go to `XOA Core <https://github.com/xenanetworks/open-automation-core>`_.

.. code-block:: python

    from xoa_core import controller
    from xoa_converter.entry import converter
    from xoa_converter.types import TestSuiteType

Then, to use the converter, you need the target schema for the old file to be converted into. After that, simply provide the target schema, the old config file to the converter function and get the new config file:

.. literalinclude:: ../code_example/using_converter.py
    :language: python
    :emphasize-lines: 17, 20-30
