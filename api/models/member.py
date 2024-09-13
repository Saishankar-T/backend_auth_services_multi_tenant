from pydantic import BaseModel
from typing import Optional

class InviteMember(BaseModel):
    email: str
    org_id: int
    role_id: int

    class Config:
        from_attributes = True

class UpdateRole(BaseModel):
    new_role_id: int

class MemberResponse(BaseModel):
    id: int
    user_id: int
    org_id: int
    role_id: int
    status: int
    settings: Optional[dict] = {}

    class Config:
        from_attributes = True
