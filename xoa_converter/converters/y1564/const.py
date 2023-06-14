from enum import Enum as CaseSensitiveEnum, IntEnum
from typing import NewType, TypeVar


TypeItemUUID = NewType("TypeItemUUID", str)

class Enum(CaseSensitiveEnum):
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member


class LegacyTidAllocationScope(Enum):
    CONFIGURATION_SCOPE = "configscope"
    RX_PORT_SCOPE = "portscope"
    SOURCE_PORT_ID = "srcportid"


class ServiceType(IntEnum):
    EPL = 0
    E_LAN = 1
    E_TREE = 2


class LossRatioUnit(Enum):
    Percent = "Percent"
    EMinus3 = "EMinus3"
    EMinus4 = "EMinus4"
    EMinus5 = "EMinus5"
    EMinus6 = "EMinus6"

class TrafficTopology(Enum):
    PAIRS = "pairs"
    BLOCKS = "blocks"
    MESH = "mesh"


class TrafficDirection(Enum):
    EAST_TO_WEST = "east_west"
    WEST_TO_EAST = "west_east"
    BIDIR = "bidir"


class PortGroup(Enum):
    EAST = "east"
    WEST = "west"
    UNDEFINED = "undefined"


class PayloadType(Enum):
    PATTERN = "pattern"
    INCREMENTING = "incrementing"
    PRBS = "prbs"


class FramePartType(Enum):
    ETHERNET = "ETHERNET"
    C_TAG = "C_TAG"
    S_TAG = "S_TAG"
    MPLS = "MPLS"
    IPv4 = "IPv4"
    IPv6 = "IPv6"
    UDP = "UDP"