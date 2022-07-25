from xoa_converter.entry import converter
from xoa_converter.types import TestSuiteType

def start():
    SOURCE_CONFIG_FILE = "test/2.v2544"
    SCHEMA_FILE = "test/schema.json"
    TEST_RESULT_FILE = "test/result.json"
    with (
        open(SOURCE_CONFIG_FILE, 'r') as source_data_file,
        open(SCHEMA_FILE, 'r') as schema_file,
        open(TEST_RESULT_FILE, 'r') as result_file,
    ):
        target_config = converter(
            test_suite_type=TestSuiteType.RFC2544, 
            source_config=source_data_file.read(), 
            target_schema=schema_file.read()
        )
        
        print(target_config)        
        assert target_config == result_file.read()


if __name__ == '__main__':
    start()


