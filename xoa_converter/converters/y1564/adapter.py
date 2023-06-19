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
                    port_id = f"P-{self.resource_id_map.chassis[chassis.chassis_id]}-{module.resource_index}-{port.resource_index}"
                    conf[port_id] = dict(
                        current_speed_select=port.curr_speed_sel,
                        port_group=port.port_group,
                        interframe_gap=port.inter_frame_gap,
                        puase_mode_enabled=port.pause_mode_on,
                        autoneg_enabled=port.auto_neg_enabled,
                        pp_autoneg_enabled=port.pp_auto_neg_enabled,
                        adjust_ppm=port.adjust_ppm,
                        latency_offset=port.latency_offset,
                        brr_mode=port.brr_mode,
                        use_custom_port_speed=port.use_custom_port_speed,
                        custom_port_speed=port.custom_port_speed,
                        port_speed_unit=port.port_speed_unit,
                        reply_arp_requests=port.reply_arp_requests,
                        reply_ndp_requests=port.reply_ndp_requests,
                        reply_ping_requests=port.reply_ping_requests,
                        reply_ping_v6_requests=port.reply_ping_v6_requests,
                        ip_address=port.ip_address,
                        ip_routing_prefix=port.ip_routing_prefix,
                        ip_gateway=port.ip_gateway,
                        ip_address_v6=port.ip_address_v6,
                        ip_routing_prefix_v6=port.ip_routing_prefix_v6,
                        ip_gateway_v6=port.ip_gateway_v6,
                        gateway_mac_address=port.ip_gateway_mac_address,
                        public_ip_address=port.public_ip_address,
                        public_ip_routing_prefix=port.public_ip_routing_prefix,
                        public_ip_address_v6=port.public_ip_address_v6,
                        public_ip_routing_prefix_v6=port.public_ip_routing_prefix_v6,
                        remote_loop_ip_address=port.remote_loop_ip_address,
                        remote_loop_ip_address_v6=port.remote_loop_ip_v6_address,
                        remote_loop_mac_address=port.remote_loop_mac_address,
                    )
        return conf

    def gen(self) -> Dict[str, Any]:
        port_config = self.__gen_port_config()
        port_identities = self.__gen_port_identity()
        config = dict(
            port_config=port_config,
        )
        logger.debug(config)
        return dict(username="Y-1564", config=config, port_identities=port_identities)

    def __init__(self, source_config: str) -> None:
        self.old_model = ValkyrieConfiguration1564.parse_raw(source_config)
        self.resource_id_map = ValkyrieXOAResourceIDMap()
        self._gen_chassis_id_map()
        logger.debug(self.old_model)