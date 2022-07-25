from typing import (
    Dict, 
    Set, 
)
from pydantic import BaseModel
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
