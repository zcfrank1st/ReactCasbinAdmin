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

class User(BaseModel):
    id: int
    user_name: str
    password: str

class UserIn(BaseModel):
    user_name: Optional[str]
    password: Optional[str]

class Role(BaseModel):
    id: int
    role_name: str

class RoleIn(BaseModel):
    role_name: Optional[str]

class UserRoleRelation(BaseModel):
    id: int
    user_id: int
    role_id: int

class UserRoleRelationIn(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]