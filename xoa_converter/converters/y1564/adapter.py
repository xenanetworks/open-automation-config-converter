import hashlib
from typing import Any, Dict, List

from loguru import logger
from pydantic import BaseModel, Field
from .model import (
    ValkyrieConfiguration1564,
)
from ..common import (
    PortIdentity,
)



class ValkyrieXOAResourceIDMap(BaseModel):
    chassis: Dict[str, str] = Field(default_factory=dict)
    port: Dict[str, str] = Field(default_factory=dict)


class Converter1564:
    old_model: ValkyrieConfiguration1564
    resource_id_map: ValkyrieXOAResourceIDMap

    def _gen_chassis_id_map(self) -> None:
        for chassis_info in self.old_model.chassis_list:
            new_chassis_id = hashlib.md5(
                f"{chassis_info.host_name}:{chassis_info.port_number}".encode("utf-8")
            ).hexdigest()
            self.resource_id_map.chassis[chassis_info.chassis_id] = new_chassis_id

    def __gen_port_identity(self) -> List["PortIdentity"]:
        port_identity = []

        for uni in self.old_model.uni_list:
            new_chassis_id = self.resource_id_map.chassis[uni.chassis_id]
            self.resource_id_map.port[uni.item_id] = f"P-{new_chassis_id}-{uni.module_index}-{uni.port_index}"
            identity = dict(
                tester_id=new_chassis_id,
                module_index=uni.module_index,
                port_index=uni.port_index,
            )

            port_identity.append(identity)
        return port_identity

    def __gen_port_config(self) -> Dict[str, Any]:
        conf = {}
        for chassis in self.old_model.chassis_list:
            for module in chassis.used_module_list:
                for port in module.used_port_list:
                    port_id = f"P-{self.resource_id_map.chassis[chassis.chassis_id]}-{module.resource_index}-{module.resource_index}-{port.resource_index}"
                    conf[port_id] = port
        return conf

    def gen(self) -> Dict[str, Any]:
        port_identities = self.__gen_port_identity()
        config = dict(
        )
        logger.debug(self.resource_id_map)
        port_config = self.__gen_port_config()
        logger.debug(port_config)
        return dict(username="Y-1564", config=config, port_identities=port_identities)

    def __init__(self, source_config: str) -> None:
        self.old_model = ValkyrieConfiguration1564.parse_raw(source_config)
        self.resource_id_map = ValkyrieXOAResourceIDMap()
        self._gen_chassis_id_map()
        logger.debug(self.old_model)