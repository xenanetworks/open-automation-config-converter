![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xoa-converter) [![PyPI](https://img.shields.io/pypi/v/xoa-converter)](https://pypi.python.org/pypi/xoa-converter) ![GitHub](https://img.shields.io/github/license/xenanetworks/open-automation-config-converter) [![Documentation Status](https://readthedocs.org/projects/xena-openautomation-test-config-converter/badge/?version=stable)](https://xena-openautomation-test-config-converter.readthedocs.io/en/stable/?badge=stable)
# Xena OpenAutomation Test Config Converter
Xena OpenAutomation (XOA) Test Configuration Converter is a supporting tool for users to quickly migrate their Valkyrie test suite configurations into XOA.

## Introduction
Xena's test suite applications have only been for Windows platform for a long time. Moving forward, all of Xena's existing and future test suites will be included in Xena OpenAutomation, which is not limited to Windows anymore. 

We have developed this test configuration converter and made it into a Python package to help users easily migrate their existing Windows test suite configurations (`.v2544` for [Valkyrie2544](https://xenanetworks.com/product/valkyrie2544/), `.v2889` for [Valkyrie2889](https://xenanetworks.com/product/valkyrie2889/), `.v3918` for [Valkyrie3918](https://xenanetworks.com/product/valkyrie3918/), and `.v1564` for [Valkyrie1564](https://xenanetworks.com/product/valkyrie1564/)) into `XOA`.

For users of XOA who only uses the web GUI to create, import and run tests, there is no need to use this Python package, because [XOA Core](https://github.com/xenanetworks/open-automation-core) is already using this converter.

This converter is meant for those who want to integrate XOA test suites into their own Python environment without using the web GUI at all.

> The purpose of XOA Converter is ONLY to convert Xena Valkyrie test suit applications' configuration files into XOA's configuration files. Thus only four test suite types are supported by XOA Converter as the source config files. 

## Documentation
The user documentation is hosted:
[Xena OpenAutomation Test Config Converter Documentation](https://docs.xenanetworks.com/projects/xoa-config-converter)


## Installation

### Install Using `pip`
Make sure Python `pip` is installed on you system. If you are using virtualenv, then pip is already installed into environments created by virtualenv, and using sudo is not needed. If you do not have pip installed, download this file: https://bootstrap.pypa.io/get-pip.py and run `python get-pip.py`.

To install the latest, use pip to install from pypi:
``` shell
~/> pip install xoa-converter
```

To upgrade to the latest, use pip to upgrade from pypi:
``` shell
~/> pip install xoa-converter --upgrade
```

### Install From Source Code
Make sure these packages are installed ``wheel``, ``setuptools`` on your system.

Install ``setuptools`` using pip:
``` shell
~/> pip install wheel setuptools
```

To install source of python packages:
``` shell
/xoa_driver> python setup.py install
```

To build ``.whl`` file for distribution:
``` shell
/xoa_driver> python setup.py bdist_wheel
```

## Quick Start

* Get Python pip if not already installed (Download https://bootstrap.pypa.io/get-pip.py):
    `python get-pip.py`

* Install the latest xoa-driver:
    `pip install xoa-converter -U`

* Code example to convert `.v2544` into XOA 2544 test configuration:
    ```python
    import asyncio
    import json
    from xoa_core import controller
    from xoa_converter.entry import converter
    from xoa_converter.types import TestSuiteType

    async def start():
        SOURCE_CONFIG_FILE = "my_old2544_config.v2544" # source config file to be converted

        core_ctrl = await controller.MainController() # create an instance of xoa core controller
        info = core_ctrl.get_test_suite_info("RFC-2544") # get 2544 test suite information from the core's registration
        target_schema = json.load(info['schema']) # get the target json schema

        with open(SOURCE_CONFIG_FILE, 'r') as source_data_file:
            target_config = converter(
                test_suite_type=TestSuiteType.RFC2544, 
                source_config=source_data_file.read(), 
                target_schema=target_schema
            )
            
            print(target_config)


    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.create_task(start())
        loop.run_forever()
    ```


***

FOR TESTING BEYOND THE STANDARD.
