from typing import Dict, List, Optional, Union

from pydantic import Field, BaseModel

from xoa_converter.converters.y1564 import const


class IdentifierBase(BaseModel):
    item_id: const.TypeItemUUID = Field(alias='ItemID')
    parent_id: const.TypeItemUUID = Field(alias='ParentID', default="")
    label: str = Field(alias='Label')


class UsedPortListItem(BaseModel):
    curr_speed_sel: Union[int, str] = Field(alias='CurrSpeedSel')
    port_group: const.PortGroup = Field(alias='PortGroup')
    pair_peer_ref: Optional[str] = Field(alias='PairPeerRef')
    inter_frame_gap: int = Field(alias='InterFrameGap')
    pause_mode_on: bool = Field(alias='PauseModeOn')
    auto_neg_enabled: bool = Field(alias='AutoNegEnabled')
    pp_auto_neg_enabled: bool = Field(alias='PPAutoNegEnabled')
    adjust_ppm: int = Field(alias='AdjustPpm')
    latency_offset: int = Field(alias='LatencyOffset')
    brr_mode: str = Field(alias='BrrMode')
    use_custom_port_speed: bool = Field(alias='UseCustomPortSpeed')
    custom_port_speed: float = Field(alias='CustomPortSpeed')
    port_speed_unit: str = Field(alias='PortSpeedUnit')
    reply_arp_requests: bool = Field(alias='ReplyArpRequests')
    reply_ndp_requests: bool = Field(alias='ReplyNdpRequests')
    reply_ping_requests: bool = Field(alias='ReplyPingRequests')
    reply_ping_v6_requests: bool = Field(alias='ReplyPingV6Requests')
    send_gratuitous_arp: bool = Field(alias='SendGratuitousArp')
    ip_address: str = Field(alias='IpAddress')
    ip_routing_prefix: int = Field(alias='IpRoutingPrefix')
    ip_gateway: str = Field(alias='IpGateway')
    ip_address_v6: str = Field(alias='IpAddressV6')
    ip_routing_prefix_v6: int = Field(alias='IpRoutingPrefixV6')
    ip_gateway_v6: str = Field(alias='IpGatewayV6')
    ip_gateway_mac_address: str = Field(alias='IpGatewayMacAddress')
    public_ip_address: str = Field(alias='PublicIpAddress')
    public_ip_routing_prefix: int = Field(alias='PublicIpRoutingPrefix')
    public_ip_address_v6: str = Field(alias='PublicIpAddressV6')
    public_ip_routing_prefix_v6: int = Field(alias='PublicIpRoutingPrefixV6')
    remote_loop_ip_address: str = Field(alias='RemoteLoopIpAddress')
    remote_loop_ip_v6_address: str = Field(alias='RemoteLoopIpV6Address')
    remote_loop_mac_address: str = Field(alias='RemoteLoopMacAddress')
    resource_used: bool = Field(alias='ResourceUsed')
    child_resource_used: bool = Field(alias='ChildResourceUsed')
    resource_index: int = Field(alias='ResourceIndex')


class UsedModuleListItem(BaseModel):
    used_port_list: List[UsedPortListItem] = Field(alias='UsedPortList')
    resource_used: bool = Field(alias='ResourceUsed')
    child_resource_used: bool = Field(alias='ChildResourceUsed')
    resource_index: int = Field(alias='ResourceIndex')


class ChassisItem(BaseModel):
    chassis_id: str = Field(alias="ChassisID")
    host_name: str = Field(alias="HostName")
    port_number: int = Field(alias="PortNumber")
    password: str = Field(alias="Password")
    connection_type: str = Field(alias="ConnectionType")
    used_module_list: List[UsedModuleListItem] = Field(alias='UsedModuleList')
    resource_index: int = Field(alias="ResourceIndex")
    resource_used: bool = Field(alias="ResourceUsed")
    child_resource_used: bool = Field(alias="ChildResourceUsed")


class GlobalTrafficConfig(BaseModel):
    mac_base_address: str = Field(alias='MacBaseAddress')
    use_native_mac: bool = Field(alias='UseNativeMac')
    mac_learning_mode: const.MacLearningModeType = Field(alias='MacLearningMode')
    mac_learning_retries: int = Field(alias='MacLearningRetries')
    use_phys_port_speed: bool = Field(alias='UsePhysPortSpeed')
    max_config_port_speed: int = Field(alias='MaxConfigPortSpeed')
    address_refresh_enabled: bool = Field(alias='AddressRefreshEnabled')
    address_refresh_period: float = Field(alias='AddressRefreshPeriod')


class PerformanceCriteria(BaseModel):
    max_frame_loss_ratio: float = Field(alias='MaxFrameLossRatio')
    use_max_frame_loss_ratio: bool = Field(alias='UseMaxFrameLossRatio')
    loss_ratio_unit: const.LossRatioUnit = Field(alias='LossRatioUnit')
    max_frame_transfer_delay: float = Field(alias='MaxFrameTransferDelay')
    use_max_frame_transfer_delay: bool = Field(alias='UseMaxFrameTransferDelay')
    max_frame_delay_variance: float = Field(alias='MaxFrameDelayVariance')
    use_max_frame_delay_variance: bool = Field(alias='UseMaxFrameDelayVariance')
    min_availability: float = Field(alias='MinAvailability')
    use_min_availability: bool = Field(alias='UseMinAvailability')


class ServiceItem(IdentifierBase):
    service_type: const.ServiceType = Field(alias='ServiceType')
    is_virtual_service: bool = Field(alias='IsVirtualService')
    performance_criteria: PerformanceCriteria = Field(alias='PerformanceCriteria')
    topology: const.TrafficTopology = Field(alias='Topology')
    direction: const.TrafficDirection = Field(alias='Direction')
    use_in_tests: bool = Field(alias='UseInTests')


class EthernetConfig(BaseModel):
    ether_type: str = Field(alias='EtherType')


class CVlANConfig(BaseModel):
    pcp: int = Field(alias='PCP')
    vlan_tag: int = Field(alias='VlanTag')
    ether_type: str = Field(alias='EtherType')


class SVlANConfig(BaseModel):
    pcp: int = Field(alias='PCP')
    vlan_tag: int = Field(alias='VlanTag')
    ether_type: str = Field(alias='EtherType')


class IPConfig(BaseModel):
    ip_version: str = Field(alias='IpVersion')
    diff_serv_code_point: int = Field(alias='DiffServCodePoint')
    ip_identification: int = Field(alias='IpIdentification')
    ip_protocol_type: str = Field(alias='IpProtocolType')


class UDPConfig(BaseModel):
    source_port: int = Field(alias='SourcePort')
    dest_port: int = Field(alias='DestPort')
    use_checksum: bool = Field(alias='UseChecksum')


class MPLSConfigItem(BaseModel):
    label: int = Field(alias='Label')
    traffic_class: int = Field(alias='TrafficClass')
    ttl: int = Field(alias='TTL')


class TrafficConfig(BaseModel):
    ether_config: EthernetConfig = Field(alias='EtherConfig')
    c_vlan_config: CVlANConfig = Field(alias='C_VlanConfig')
    s_vlan_config: SVlANConfig = Field(alias='S_VlanConfig')
    ip_config: IPConfig = Field(alias='IpConfig')
    udp_config: UDPConfig = Field(alias='UdpConfig')
    port_group: const.PortGroup = Field(alias='PortGroup')
    pair_peer_ref: Optional[const.TypeItemUUID] = Field(alias='PairPeerRef', default="")
    frame_parts: List[const.FramePartType] = Field(alias='FrameParts')
    mpls_config_list: List[MPLSConfigItem] = Field(alias='MplsConfigList')
    payload_type: const.PayloadType = Field(alias='PayloadType')
    payload_pattern: str = Field(alias='PayloadPattern')


class COS2DSCPItem(BaseModel):
    use_dscp_value: bool = Field(alias='UseDscpValue')
    dscp_value: int = Field(alias='DscpValue')


class IngressProfiles(BaseModel):
    use_per_cos_profile: bool = Field(alias='UsePerCosProfile')
    uni_profile: const.TypeItemUUID = Field(alias='UniProfile')
    cos_profile_map: Dict[str, const.TypeItemUUID] = Field(alias='CosProfileMap')
    cos_2_dscp_map: Dict[str, COS2DSCPItem] = Field(alias='Cos2DscpMap')


class EgressProfiles(BaseModel):
    use_per_cos_profile: bool = Field(alias='UsePerCosProfile')
    uni_profile: const.TypeItemUUID = Field(alias='UniProfile')
    cos_profile_map: Dict[str, const.TypeItemUUID] = Field(alias='CosProfileMap')
    cos_2_dscp_map: Dict[str, COS2DSCPItem] = Field(alias='Cos2DscpMap')


class UNIItem(IdentifierBase):
    service_id: str = Field(alias='ServiceID')
    chassis_id: str = Field(alias='ChassisID')
    module_index: int = Field(alias='ModuleIndex')
    port_index: int = Field(alias='PortIndex')
    is_root: bool = Field(alias='IsRoot')
    traffic_config: TrafficConfig = Field(alias='TrafficConfig')
    ingress_profiles: IngressProfiles = Field(alias='IngressProfiles')
    egress_profiles: EgressProfiles = Field(alias='EgressProfiles')


class FolderItem(IdentifierBase):
    parent_id: Optional[const.TypeItemUUID] = Field(alias='ParentID')

class BandwidthProfileItem(IdentifierBase):
    cir: float = Field(alias='CIR')
    cbs: int = Field(alias='CBS')
    eir: float = Field(alias='EIR')
    ebs: int = Field(alias='EBS')
    color_mode: const.ColorMode = Field(alias='ColorMode')
    coupling_flag: const.CouplingFlag = Field(alias='CouplingFlag')


class TestParamsCommon(BaseModel):
    enabled_sub_test_types: List[const.SubTestType] = Field(alias='EnabledSubTestTypes')
    break_on_fail: bool = Field(alias='BreakOnFail')
    traffic_size_sel: const.TrafficSize = Field(alias='TrafficSizeSel')
    custom_traffic_sizes: List[float] = Field(alias='CustomTrafficSizes')
    frame_start_size: int = Field(alias='FrameStartSize')
    frame_end_size: int = Field(alias='FrameEndSize')
    frame_step_size: int = Field(alias='FrameStepSize')
    frame_min_size: int = Field(alias='FrameMinSize')
    frame_max_size: int = Field(alias='FrameMaxSize')
    latency_mode: const.LatencyMode = Field(alias='LatencyMode')
    address_refresh_period: float = Field(alias='AddressRefreshPeriod')
    address_refresh_enabled: bool = Field(alias='AddressRefreshEnabled')


class ConfigTestParams(TestParamsCommon):
    policing_grace_factor: float = Field(alias='PolicingGraceFactor')
    iterations: int = Field(alias='Iterations')
    step_time: int = Field(alias='StepTime')
    start_rate: int = Field(alias='StartRate')
    step_rate: int = Field(alias='StepRate')
    fall_back_cir_step_load_test: bool = Field(alias='FallBackCirStepLoadTest')


class PerfTestParams(TestParamsCommon):
    perf_test_period: str = Field(alias='PerfTestPeriod')
    perf_test_custom_period: str = Field(alias='PerfTestCustomPeriod')
    ses_loss_ratio_threshold: float = Field(alias='SesLossRatioThreshold')


class ValkyrieConfiguration1564(BaseModel):
    """represent '.v1564' configuration file"""

    tid_offset: int = Field(alias="TidOffset")
    global_traffic_config: GlobalTrafficConfig = Field(alias="GlobalTrafficConfig")
    service_list: List[ServiceItem] = Field(alias="ServiceList")
    uni_list: List[UNIItem] = Field(alias="UniList")
    folder_list : List[FolderItem] = Field(alias="FolderList")
    bandwidth_profile_list: List[BandwidthProfileItem] = Field(alias="BandwidthProfileList")
    config_test_params: ConfigTestParams = Field(alias="ConfigTestParams")
    perf_test_params: PerfTestParams = Field(alias='PerfTestParams')
    tid_allocation_scope: const.LegacyTidAllocationScope = Field(alias="TidAllocationScope")
    chassis_list : List[ChassisItem] = Field(alias="ChassisList")
