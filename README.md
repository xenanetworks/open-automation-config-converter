![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xoa-converter) [![PyPI](https://img.shields.io/pypi/v/xoa-converter)](https://pypi.python.org/pypi/xoa-converter) ![GitHub](https://img.shields.io/github/license/xenanetworks/open-automation-config-converter) [![Documentation Status](https://readthedocs.com/projects/xena-networks-open-automation-config-converter/badge/?version=latest)](https://docs.xenanetworks.com/projects/xoa-config-converter/en/latest/?badge=latest)
# Xena OpenAutomation Test Config Converter
Xena OpenAutomation (XOA) Test Configuration Converter is a supporting tool for users to quickly migrate their Valkyrie test suite configurations into XOA.

## Introduction
The XOA Test Config Converter is an open-source tool hosted on Xena Networks' GitHub repository. It is designed to help users migrate their existing Valkyrie test suite configurations into the XOA format, enabling a seamless transition to the XOA ecosystem for network automation and testing.

Key features of the XOA Test Config Converter include:

1. Conversion support: The tool supports conversion of Valkyrie test suite configuration files to XOA-compatible format, facilitating the integration of existing test cases into the XOA framework.

2. Ease of use: The XOA Test Config Converter is designed to be user-friendly, with a straightforward process for converting test suite configuration files.

3. Compatibility: The converter ensures that the migrated test suite configurations are compatible with XOA Core and can be executed within the XOA ecosystem.

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
