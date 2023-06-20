import hashlib
from enum import Enum
from typing import Any, Dict, List, Union, TYPE_CHECKING

from loguru import logger
from pydantic import BaseModel, Field

from .model import (
    ValkyrieConfiguration1564,
)
from .const import ServiceType, TrafficTopology, TrafficDirection, PortGroup, PayloadType
from ..common import (
    PortIdentity,
)
from .const import TypeItemUUID

if TYPE_CHECKING:
    from .model import (
        FolderItem,
    )


class TreeNodeType(Enum):
    FOLDER = 'FOLDER'
    SERVICE = 'SERVICE'

class TreeNodeBase(BaseModel):
    tree_node_type: TreeNodeType

    @property
    def is_folder(self) -> bool:
        return self.tree_node_type == TreeNodeType.FOLDER

    @property
    def is_service(self) -> bool:
        return self.tree_node_type == TreeNodeType.SERVICE


TNode = Union["NodeService", "NodeFolder"]
TNodeList = List[TNode]


class NodeFolder(TreeNodeBase):
    tree_node_type: TreeNodeType = TreeNodeType.FOLDER
    name: str
    valkyrie_id: TypeItemUUID = Field(default_factory=str)
    nodes: TNodeList = Field(default_factory=list)


class UNI(BaseModel):
    port_id: str # xoa port id
    port_group: PortGroup
    ethernet_config: Dict[str, Any]
    c_vlan_config: Dict[str, Any]
    ip_config: Dict[str, Any]
    udp_config: Dict[str, Any]
    frame_parts: List[str] = Field(default_factory=list)
    mpls_configs: List[Dict[str, Any]] = Field(default_factory=list)
    payload_type: PayloadType
    payload_pattern: str


class NodeService(TreeNodeBase):
    tree_node_type: TreeNodeType = TreeNodeType.SERVICE
    service_name: str
    service_type: ServiceType
    topology: TrafficTopology
    direction: TrafficDirection
    UNIs: List[UNI] = Field(default_factory=list)


class ValkyrieXOAResourceIDMap(BaseModel):
    chassis: Dict[str, str] = Field(default_factory=dict)
    port: Dict[str, str] = Field(default_factory=dict)


class Converter1564:
    old_model: ValkyrieConfiguration1564
    resource_id_map: ValkyrieXOAResourceIDMap
    all_services: TNodeList

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

    def dfs_append_node(self, target_valkyrie_id: str, searching_node: TNode, to_append_node: TNode) -> None:
        if searching_node.is_service:
            return
        assert isinstance(searching_node, NodeFolder)

        if searching_node.valkyrie_id == target_valkyrie_id:
            searching_node.nodes.append(to_append_node)
            return

        for node in searching_node.nodes:
            self.dfs_append_node(target_valkyrie_id, node, to_append_node)

    def append_folder(self, valkyrie_folder: "FolderItem") -> None:
        node_folder = NodeFolder(name=valkyrie_folder.label, valkyrie_id=valkyrie_folder.item_id)
        if not valkyrie_folder.parent_id:
            self.all_services.append(node_folder)
            return

        for searching_node in self.all_services:
            self.dfs_append_node(valkyrie_folder.parent_id, searching_node, node_folder)

    def __gen_services(self) -> None:
        for folder in self.old_model.folder_list:
            self.append_folder(folder)
        for service in self.old_model.service_list:
            for node in self.all_services:
                if node.is_service:
                    continue
                self.dfs_append_node(service.parent_id, node, NodeService(service_name=service.label))

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
        return dict(username="Y-1564", config=config, port_identities=port_identities)

    def __init__(self, source_config: str) -> None:
        self.old_model = ValkyrieConfiguration1564.parse_raw(source_config)
        self.resource_id_map = ValkyrieXOAResourceIDMap()
        self._gen_chassis_id_map()
        self.all_services = []
        self.__gen_services()
        # logger.debug(self.old_model)
        logger.debug(self.all_services)