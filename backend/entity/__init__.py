from typing import List
from pydantic import BaseModel
from pydantic.schema import Optional

class PolicyIn(BaseModel):
    ptype: Optional[str]
    v0: Optional[str]
    v1: Optional[str]
    v2: Optional[str]
    v3: Optional[str]
    v4: Optional[str]
    v5: Optional[str]


class Policy(BaseModel):
    id: int
    ptype: str
    v0: str
    v1: str
    v2: str
    v3: Optional[str]
    v4: Optional[str]
    v5: Optional[str]

