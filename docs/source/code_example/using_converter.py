import asyncio
import json
from xoa_core import controller
from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType

# source config file to be converted
OLD_CONFIG_FILE = "my_old2544_config.v2544" 
NEW_CONFIG_FILE = "xoa2544.json"
T_SUITE_NAME = "RFC-2544"

async def start():

    # create an instance of xoa core controller
    c = await controller.MainController()

    with open(OLD_CONFIG_FILE) as f:
        app_data = f.read()

        # get 2544 test suite information from the core's registration
        info = c.get_test_suite_info(T_SUITE_NAME)
        if not info:
            print("Test suite is not recognized.")
            return None
        
        # convert the old config file into new config file
        new_data = converter(TestSuiteType.RFC2544, app_data, info["schema"])

        with open(NEW_CONFIG_FILE, "w") as f:
            f.write(new_data)
        
        # you can use the config file below to start the test
        config = json.loads(new_data)
        exec_id = c.start_test_suite(T_SUITE_NAME, config, debug_connection=False)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()