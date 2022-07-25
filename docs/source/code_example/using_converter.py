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