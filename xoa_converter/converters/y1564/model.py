
from typing import Dict, List
from pydantic import Field, BaseModel

from xoa_converter.converters.y1564 import const



class ChassisItem(BaseModel):
    chassis_id: str = Field(alias="ChassisID")
    host_name: str = Field(alias="HostName")
    port_number: int = Field(alias="PortNumber")
    password: str = Field(alias="Password")
    connection_type: str = Field(alias="ConnectionType")
    used_module_list: List = Field(alias="UsedModuleList")
    resource_index: int = Field(alias="ResourceIndex")
    resource_used: bool = Field(alias="ResourceUsed")
    child_resource_used: bool = Field(alias="ChildResourceUsed")

class GlobalTrafficConfig(BaseModel):
    mac_base_address: str = Field(..., alias='MacBaseAddress')
    use_native_mac: bool = Field(..., alias='UseNativeMac')
    mac_learning_mode: str = Field(..., alias='MacLearningMode')
    mac_learning_retries: int = Field(..., alias='MacLearningRetries')
    use_phys_port_speed: bool = Field(..., alias='UsePhysPortSpeed')
    max_config_port_speed: int = Field(..., alias='MaxConfigPortSpeed')
    address_refresh_enabled: bool = Field(..., alias='AddressRefreshEnabled')
    address_refresh_period: float = Field(..., alias='AddressRefreshPeriod')

class PerformanceCriteria(BaseModel):
    max_frame_loss_ratio: float = Field(..., alias='MaxFrameLossRatio')
    use_max_frame_loss_ratio: bool = Field(..., alias='UseMaxFrameLossRatio')
    loss_ratio_unit: const.LossRatioUnit = Field(..., alias='LossRatioUnit')
    max_frame_transfer_delay: float = Field(..., alias='MaxFrameTransferDelay')
    use_max_frame_transfer_delay: bool = Field(..., alias='UseMaxFrameTransferDelay')
    max_frame_delay_variance: float = Field(..., alias='MaxFrameDelayVariance')
    use_max_frame_delay_variance: bool = Field(..., alias='UseMaxFrameDelayVariance')
    min_availability: float = Field(..., alias='MinAvailability')
    use_min_availability: bool = Field(..., alias='UseMinAvailability')


class ServiceItem(BaseModel):
    service_type: const.ServiceType = Field(..., alias='ServiceType')
    is_virtual_service: bool = Field(..., alias='IsVirtualService')
    performance_criteria: PerformanceCriteria = Field(..., alias='PerformanceCriteria')
    topology: const.TrafficTopology = Field(..., alias='Topology')
    direction: const.TrafficDirection = Field(..., alias='Direction')
    use_in_tests: bool = Field(..., alias='UseInTests')
    item_id: str = Field(..., alias='ItemID')
    parent_id: str = Field(..., alias='ParentID')
    label: str = Field(..., alias='Label')

class EthernetConfig(BaseModel):
    ether_type: str = Field(..., alias='EtherType')


class CVlANConfig(BaseModel):
    pcp: int = Field(..., alias='PCP')
    vlan_tag: int = Field(..., alias='VlanTag')
    ether_type: str = Field(..., alias='EtherType')


class SVlANConfig(BaseModel):
    pcp: int = Field(..., alias='PCP')
    vlan_tag: int = Field(..., alias='VlanTag')
    ether_type: str = Field(..., alias='EtherType')


class IPConfig(BaseModel):
    ip_version: str = Field(..., alias='IpVersion')
    diff_serv_code_point: int = Field(..., alias='DiffServCodePoint')
    ip_identification: int = Field(..., alias='IpIdentification')
    ip_protocol_type: str = Field(..., alias='IpProtocolType')


class UDPConfig(BaseModel):
    source_port: int = Field(..., alias='SourcePort')
    dest_port: int = Field(..., alias='DestPort')
    use_checksum: bool = Field(..., alias='UseChecksum')


class MPLSConfigItem(BaseModel):
    label: int = Field(..., alias='Label')
    traffic_class: int = Field(..., alias='TrafficClass')
    ttl: int = Field(..., alias='TTL')


class TrafficConfig(BaseModel):
    ether_config: EthernetConfig = Field(..., alias='EtherConfig')
    c_vlan_config: CVlANConfig = Field(..., alias='C_VlanConfig')
    s_vlan_config: SVlANConfig = Field(..., alias='S_VlanConfig')
    ip_config: IPConfig = Field(..., alias='IpConfig')
    udp_config: UDPConfig = Field(..., alias='UdpConfig')
    port_group: const.PortGroup = Field(..., alias='PortGroup')
    pair_peer_ref: str = Field(..., alias='PairPeerRef')
    frame_parts: List[const.FramePartType] = Field(..., alias='FrameParts')
    mpls_config_list: List[MPLSConfigItem] = Field(..., alias='MplsConfigList')
    payload_type: const.PayloadType = Field(..., alias='PayloadType')
    payload_pattern: str = Field(..., alias='PayloadPattern')


class COS2DSCPItem(BaseModel):
    use_dscp_value: bool = Field(..., alias='UseDscpValue')
    dscp_value: int = Field(..., alias='DscpValue')


class IngressProfiles(BaseModel):
    use_per_cos_profile: bool = Field(..., alias='UsePerCosProfile')
    uni_profile: const.TypeItemUUID = Field(..., alias='UniProfile')
    cos_profile_map: Dict[str, const.TypeItemUUID] = Field(..., alias='CosProfileMap')
    cos_2_dscp_map: Dict[str, COS2DSCPItem] = Field(..., alias='Cos2DscpMap')


class EgressProfiles(BaseModel):
    use_per_cos_profile: bool = Field(..., alias='UsePerCosProfile')
    uni_profile: const.TypeItemUUID = Field(..., alias='UniProfile')
    cos_profile_map: Dict[str, const.TypeItemUUID] = Field(..., alias='CosProfileMap')
    cos_2_dscp_map: Dict[str, COS2DSCPItem] = Field(..., alias='Cos2DscpMap')


class UNIItem(BaseModel):
    service_id: str = Field(..., alias='ServiceID')
    chassis_id: str = Field(..., alias='ChassisID')
    module_index: int = Field(..., alias='ModuleIndex')
    port_index: int = Field(..., alias='PortIndex')
    is_root: bool = Field(..., alias='IsRoot')
    traffic_config: TrafficConfig = Field(..., alias='TrafficConfig')
    ingress_profiles: IngressProfiles = Field(..., alias='IngressProfiles')
    egress_profiles: EgressProfiles = Field(..., alias='EgressProfiles')
    item_id: str = Field(..., alias='ItemID')
    parent_id: str = Field(..., alias='ParentID')
    label: str = Field(..., alias='Label')


class ValkyrieConfiguration1564(BaseModel):
    """represent '.v1564' configuration file"""

    tid_offset: int = Field(alias="TidOffset")
    global_traffic_config: GlobalTrafficConfig = Field(alias="GlobalTrafficConfig")
    service_list: List[ServiceItem] = Field(alias="ServiceList")
    uni_list: List[UNIItem] = Field(alias="UniList")
    chassis_list : List[ChassisItem] = Field(alias="ChassisList")
    tid_allocation_scope: const.LegacyTidAllocationScope = Field(alias="TidAllocationScope")