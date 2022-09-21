import os
from enum import Enum


DEFAULT_SEGMENT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "reference/segment_refs",
    )
)


def from_legacy_multicast_role(string: str) -> str:
    return {
        "McSource": "mc_source",
        "McDestination": "mc_destination",
        "UcBurden": "uc_burden",
        "Undefined": "undefined",
    }.get(string, string)


def from_legacy_test_topology(string: str) -> str:
    return {
        "PAIRS": "pairs",
        "BLOCKS": "blocks",
        "MESH": "mesh",
    }.get(string, string)


def from_legacy_traffic_direction(string: str) -> str:
    return {
        "EAST_TO_WEST": "east_to_west",
        "WEST_TO_EAST": "west_to_east",
        "BIDIR": "bidir",
    }.get(string, string)


def from_legacy_igmp_version(string: str) -> str:
    return {
        "IGMP_V1": "igmp_v1",
        "IGMP_V2": "igmp_v2_or_mld_v1",
        "IGMP_V3": "igmp_v3_or_mld_v2",
    }.get(string, string)


def from_legacy_display_unit(string: str) -> str:
    return {
        "Millisecs": "millisecs",
        "Microsecs": "microsecs",
    }.get(string, string)


def from_legacy_protocol_option(string: str) -> str:
    return {
        "ARP": "arp",
        "ETHERNET": "ethernet",
        "FC": "fc",
        "FCOEHEAD": "fcoe",
        "FCOETAIL": "fcoetail",
        "GRE_CHECK": "gre_check",
        "GRE_NOCHECK": "gre_nocheck",
        "GTP": "gtp",
        "ICMP": "icmp",
        "ICMPV6": "icmpv6",
        "IGMPV1": "igmpv1",
        "IGMPV2": "igmpv2",
        "MLDV2_AR": "mldv2_ar",
        "IGMPV3_GR": "igmpv3_gr",
        "IGMPV3_MR": "igmpv3_mr",
        "IGMPV3L0": "igmpv3l0",
        "IGMPV3L1": "igmpv3l1",
        "IP": "ipv4",
        "IPv6": "ipv6",
        "LLC": "llc",
        "MACCTRL": "macctrl",
        "MPLS": "mpls",
        "NVGRE": "nvgre",
        "PBBTAG": "pbbtag",
        "RTCP": "rtcp",
        "RTP": "rtp",
        "SCTP": "sctp",
        "SNAP": "snap",
        "STP": "stp",
        "TCP": "tcp",
        "TCPCHECK": "tcp_check",
        "UDP": "udp",
        "UDPCHECK": "udpcheck",
        "VLAN": "vlan",
        "VXLAN": "vxlan",
    }.get(string, string)


def from_legacy_port_rate_cap_profile(string: str) -> str:
    return {
        "Physical Port Rate": "physical_port_rate",
        "Custom Rate Cap": "custom_rate_cap",
    }.get(string, string)


def from_legacy_rate_type(string: str) -> str:
    return {
        "Fraction": "fraction",
        "Pps": "pps",
    }.get(string, string)


def from_legacy_port_rate_cap_unit(string: str) -> str:
    return {
        "Gbps": "1e9_bps",
        "Mbps": "1e6_bps",
        "Kbps": "1e3_bps",
        "bps": "bps",
    }.get(string, string)


def from_legacy_flow_creation_type(string: str) -> str:
    return {
        "StreamBased": "stream_based",
        "ModifierBased": "modifier_based",
    }.get(string, string)


def from_legacy_latency_mode(string: str) -> str:
    return {
        "First_To_Last": "first_to_last",
        "Last_To_Last": "last_to_last",
        "First_To_First": "first_to_first",
        "Last_To_First": "last_to_first",
    }.get(string, string)


def from_legacy_tid_allocation_scope(string: str) -> str:
    return {
        "ConfigScope": "config_scope",
        "PortScope": "port_scope",
        "SourcePortId": "source_port_id",
    }.get(string, string)


def from_legacy_mdi_mdix_mode(string: str) -> str:
    return {
        "AUTO": "auto",
        "MDI": "mdi",
        "MDIX": "mdix",
    }.get(string, string)


def from_legacy_brr_mode(string: str) -> str:
    return {
        "MASTER": "master",
        "SLAVE": "slave",
    }.get(string, string)


def from_legacy_packet_size_type(string: str) -> str:
    return {
        "IEEEDefault": "ietf_default",
        "CustomSizes": "custom_sizes",
        "Specified": "specified",
        "Incrementing": "incrementing",
        "Butterfly": "butterfly",
        "Random": "random",
        "MixedSizes": "mixed_sizes",
    }.get(string, string)


def from_legacy_payload_type(string: str) -> str:
    return {
        "Pattern": "pattern",
        "Incrementing": "incrementing",
        "PRBS": "prbs",
    }.get(string, string)


def convert_base_mac_address(mac_address: str):
    return ":".join(
        [hex(int(i)).replace("0x", "").zfill(2).upper() for i in mac_address.split(",")]
    )


MIXED_DEFAULT_WEIGHTS = [0, 0, 0, 0, 57, 3, 5, 1, 2, 5, 1, 4, 4, 18, 0, 0]
