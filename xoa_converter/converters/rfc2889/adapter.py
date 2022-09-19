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

if TYPE_CHECKING:
    from .model import (
        LegacyPortEntity,
    )
from loguru import logger

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

    def __gen_ipv4_addr(self, entity: "LegacyPortEntity"):
        return self.module.IPV4AddressProperties.construct(
            address=entity.ip_v4_address,
            routing_prefix=entity.ip_v4_routing_prefix,
            gateway=entity.ip_v4_gateway if entity.ip_v4_gateway else "0.0.0.0",
            public_address=entity.public_ip_address
            if entity.public_ip_address
            else "0.0.0.0",
            public_routing_prefix=entity.public_ip_routing_prefix,
            remote_loop_address=entity.remote_loop_ip_address
            if entity.remote_loop_ip_address
            else "0.0.0.0",
        )

    def __gen_ipv6_addr(self, entity: "LegacyPortEntity"):
        # self.module.IPV6AddressProperties.update_forward_refs()
        return self.module.IPV6AddressProperties.construct(
            address=entity.ip_v6_address,
            routing_prefix=entity.ip_v6_routing_prefix,
            gateway=entity.ip_v6_gateway if entity.ip_v6_gateway else "::",
            public_address=entity.public_ip_address_v6
            if entity.public_ip_address_v6
            else "::",
            public_routing_prefix=entity.public_ip_routing_prefix_v6,
            remote_loop_address=entity.remote_loop_ip_address_v6
            if entity.remote_loop_ip_address_v6
            else "::",
        )
    def __gen_port_conf(self, entity: "LegacyPortEntity"):
        profile_id = self.data.stream_profile_handler.profile_assignment_map.get(
            f"guid_{entity.item_id}"
        )
        logger.debug(list(self.module.PortRateCapProfile))
        logger.debug(entity.port_rate_cap_profile.name)
        return self.module.PortConfiguration.construct(
            port_slot=self.id_map[entity.item_id][1],
            peer_config_slot=self.id_map[entity.pair_peer_id][0]
            if entity.pair_peer_id and entity.pair_peer_id in self.id_map
            else "",
            port_group=entity.port_group,
            port_speed_mode=entity.port_speed,
            ipv4_properties=self.__gen_ipv4_addr(entity),
            ipv6_properties=self.__gen_ipv6_addr(entity),
            ip_gateway_mac_address=entity.ip_gateway_mac_address,
            reply_arp_requests=bool(entity.reply_arp_requests),
            reply_ping_requests=bool(entity.reply_ping_requests),
            remote_loop_mac_address=entity.remote_loop_mac_address,
            inter_frame_gap=entity.inter_frame_gap,
            speed_reduction_ppm=entity.adjust_ppm,
            pause_mode_enabled=entity.pause_mode_on,
            latency_offset_ms=entity.latency_offset,
            fec_mode=self.module.FECModeStr[entity.fec_mode.name.lower()],
            port_rate_cap_enabled=bool(entity.enable_port_rate_cap),
            port_rate_cap_value=entity.port_rate_cap_value,
            port_rate_cap_profile=self.module.PortRateCapProfile[str(entity.port_rate_cap_profile.name.lower())],
            port_rate_cap_unit=self.module.PortRateCapUnit[entity.port_rate_cap_unit.name.lower()],
            auto_neg_enabled=bool(entity.auto_neg_enabled),
            anlt_enabled=bool(entity.anlt_enabled),
            mdi_mdix_mode=entity.mdi_mdix_mode,
            broadr_reach_mode=entity.brr_mode,
            profile_id=profile_id,
        )
    def __gen_port_config(self) -> Dict:
        port_conf: Dict = {}
        for entity in self.data.port_handler.entity_list:
            port_conf[self.id_map[entity.item_id][0]] = self.__gen_port_conf(entity)
        return port_conf

    def gen(self) -> "TestParameters":
        port_identities = self.__gen_port_identity()
        config = self.module.TestSuiteConfiguration2889.construct(
            # port config =
            ports_configuration=self.__gen_port_config(),
            protocol_segments=convert_protocol_segments(self.data.stream_profile_handler, self.module),
            # general_test_configuration=self.__generate_general_test_config(),
        )
        return TestParameters(username="RFC-2889", config=config, port_identities=port_identities)

