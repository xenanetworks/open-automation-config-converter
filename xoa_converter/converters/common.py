import base64
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    TYPE_CHECKING,
)
from pydantic import BaseModel
from pydantic.fields import Field
from operator import attrgetter

if TYPE_CHECKING:
    from xoa_converter.converters.rfc2544.model import LegacyStreamProfileHandler
    from types import ModuleType


CURRENT_FILE_PARENT_PATH = Path(__file__).parent.resolve()
SEGMENT_REFS_FOLDER = CURRENT_FILE_PARENT_PATH / 'segment_refs'


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


class SegmentRef(BaseModel):
    name: str = Field(alias='Name')
    description: str = Field(alias='Description')
    segment_type: str = Field(alias='SegmentType')
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


def load_segment_refs_json(segment_type_value: str) -> SegmentRef:
    segment_ref = SegmentRef.parse_file(SEGMENT_REFS_FOLDER / f'{segment_type_value}.json')
    return segment_ref


def convert_protocol_segments(stream_profile_handler: "LegacyStreamProfileHandler", target_module: "ModuleType") -> Dict:
    protocol_segments_profile = {}

    for profile in stream_profile_handler.entity_list:
        header_segments = []

        for hs in profile.stream_config.header_segments:
            hw_modifiers = {}
            field_value_ranges = {}
            for hm in profile.stream_config.hw_modifiers:
                if hm.segment_id == hs.item_id:
                    hw_modifiers[hm.field_name] = target_module.HWModifier.construct(
                        start_value=hm.start_value,
                        stop_value=hm.stop_value,
                        step_value=hm.step_value,
                        repeat=hm.repeat_count,
                        action=target_module.ModifierActionOption[
                            hm.action.name.lower()
                        ],
                        mask=f"{base64.b64decode(hm.mask).hex()}0000",
                        offset=hm.offset,
                    )
            for hvr in profile.stream_config.field_value_ranges:
                if hvr.segment_id == hs.item_id:
                    field_value_ranges[hvr.field_name] = target_module.ValueRange.construct(
                        field_name=hvr.field_name,
                        start_value=hvr.start_value,
                        stop_value=hvr.stop_value,
                        step_value=hvr.step_value,
                        action=target_module.ModifierActionOption[
                            hvr.action.name.lower()
                        ],
                        restart_for_each_port=hvr.reset_for_each_port,
                    )

            segment_ref = load_segment_refs_json(hs.segment_type.value)
            segment_value = bin(int('1'+base64.b64decode(hs.segment_value).hex(), 16))[3:]
            converted_fields = []

            for field in segment_ref.protocol_fields:
                converted_fields.append(
                    target_module.SegmentField.construct(
                        name=field.name,
                        value=segment_value[:field.bit_length],
                        bit_length=field.bit_length,
                        hw_modifier=hw_modifiers.get(field.name),
                        value_range=field_value_ranges.get(field.name),
                    )
                )
                segment_value = segment_value[field.bit_length:]

            segment = target_module.ProtocolSegment.construct(
                segment_type=target_module.SegmentType[hs.segment_type.name.lower()],
                fields=converted_fields,
                checksum_offset=segment_ref.checksum_offset,
            )
            header_segments.append(segment)

        protocol_segments_profile[profile.item_id] = target_module.ProtocolSegmentProfileConfig.construct(header_segments=header_segments)
    return protocol_segments_profile
