from enum import Enum as CaseSensitiveEnum, IntEnum
from typing import NewType, Type, TypeVar


TypeItemUUID = str

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


class ServiceType(Enum):
    EPL = "EPL"
    E_LAN = "E_LAN"
    E_TREE = "E_TREE"


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


class TrafficSize(Enum):
    IEEEDefault = "IEEEDefault"
    CustomSizes = "CustomSizes"
    Specified = "Specified"
    Incrementing = "Incrementing"
    Butterfly = "Butterfly"
    Random = "Random"
    MixedSizes = "MixedSizes"


class LatencyMode(Enum):
    Last_To_Last = "Last_To_Last"
    First_To_Last = "First_To_Last"
    Last_To_First = "Last_To_First"
    First_To_First = "First_To_First"


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


class ColorMode(Enum):
    ColorBlind = "ColorBlind"
    ColorAware = "ColorAware"


class CouplingFlag(Enum):
    EIR_Bound = "EIR_Bound"
    CIR_EIR_Bound = "CIR_EIR_Bound"


class SubTestType(Enum):
    CirValidationTest = "CirValidationTest"
    CirStepLoadTest = "CirStepLoadTest"
    EirConfigTest = "EirConfigTest"
    TrafficPolicingTest = "TrafficPolicingTest"
    CbsConfigTest = "CbsConfigTest"
    EbsConfigTest = "EbsConfigTest"
    PerfTest = "PerfTest"
    Invalid = "Invalid"


class MacLearningModeType(Enum):
    Never = "Never"
    Once = "Once"
    EveryTrial = "EveryTrial"