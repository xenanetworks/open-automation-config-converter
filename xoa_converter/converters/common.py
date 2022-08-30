from typing import (
    Any,
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
    bit_position: Optional[int] = None # position of current segment


class LegacySegment(BaseModel):
    name: str = Field(alias='Name')
    description: str = Field(alias='Description')
    segment_type: str = Field(alias='SegmentType')
    enclosed_type_index: int = Field(alias='EnclosedTypeIndex')
    checksum_offset: Optional[int] = Field(alias='ChecksumOffset')
    protocol_fields: List[LegacySegmentField] = Field(alias='ProtocolFields')

    def calc_field_position(self) -> None:
        bit_position_count = 0
        for field in self.protocol_fields:
            field.bit_position = bit_position_count
            bit_position_count += field.bit_length

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.calc_field_position()