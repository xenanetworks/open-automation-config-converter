import hashlib
import types
from decimal import Decimal
from typing import Dict, Union, TYPE_CHECKING
from .model import (
    ValkyrieConfiguration2889 as old_model,
)
from ..common import (
    TestParameters,
    PortIdentity,
    convert_protocol_segments,
)

# if TYPE_CHECKING:
    # from .model import (
    # )

class Converter2889:
    def __init__(self, source_config: str, target_module: types.ModuleType) -> None:
        self.id_map = {}
        self.module = target_module
        self.data = old_model.parse_raw(source_config)

    def __gen_port_identity(self) -> Dict[str, "PortIdentity"]:
        chassis_id_map = {}
        port_identity = {}

        for chassis_info in self.data.chassis_manager.chassis_list:
            chassis_id = hashlib.md5(
                f"{chassis_info.host_name}:{chassis_info.port_number}".encode("utf-8")
            ).hexdigest()
            chassis_id_map[chassis_info.chassis_id] = chassis_id
        count = 0
        chassis_id_list = list(chassis_id_map.values())
        for p_info in self.data.port_handler.entity_list:
            port = p_info.port_ref
            port.chassis_id = chassis_id_map[port.chassis_id]
            identity = PortIdentity(
                tester_id=port.chassis_id,
                tester_index=chassis_id_list.index(port.chassis_id),
                module_index=port.module_index,
                port_index=port.port_index,
            )

            self.id_map[p_info.item_id] = (f"c-{identity.name}", f"p{count}")
            port_identity[f"p{count}"] = identity
            count += 1
        return port_identity

    def gen(self) -> "TestParameters":
        port_identities = self.__gen_port_identity()
        test_conf = self.__gen_test_config()
        config = self.module.TestSuiteConfiguration2889.construct(
            protocol_segments=convert_protocol_segments(self.data.stream_profile_handler, self.module),
            test_configuration=test_conf,
            test_types_configuration=self.__gen_test_type_config(),
            ports_configuration=self.__generate_port_config(),
        )
        return TestParameters(
            username="hello", config=config, port_identities=port_identities
        )

