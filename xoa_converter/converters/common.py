from typing import (
    Dict,
    List,
    Optional,
    Set,
)
from pydantic import BaseModel
from pydantic.fields import Field
from operator import attrgetter


class PortIdentity(BaseModel):
    tester_id: str
    tester_index: int
    module_index: int
    port_index: int

    @property
    def name(self) -> str:
        return f"P-{self.tester_index}-{self.module_index}-{self.port_index}"


class TestParameters(BaseModel):
    username: str
    port_identities: Dict[str, PortIdentity]
    config: BaseModel

    @property
    def get_testers_ids(self) -> Set[str]:
        return set(map(
            attrgetter("tester_id"),
            self.port_identities.values()
        ))


class LegacySegmentField(BaseModel):
    name: str = Field(alias='Name')
    bit_length: int = Field(alias='BitLength')
    display_type: str = Field(alias='DisplayType')
    default_value: str = Field(alias='DefaultValue')
    value_map_name: Optional[str] = Field(None, alias='ValueMapName')


class LegacySegment(BaseModel):
    name: str = Field(alias='Name')
    description: str = Field(alias='Description')
    segment_type: str = Field(alias='SegmentType')
    enclosed_type_index: int = Field(alias='EnclosedTypeIndex')
    protocol_fields: List[LegacySegmentField] = Field(alias='ProtocolFields')