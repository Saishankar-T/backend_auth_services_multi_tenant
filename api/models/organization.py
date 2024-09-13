from pydantic import BaseModel
from typing import Optional

class OrganizationCreate(BaseModel):
    name: str
    status: Optional[int] = 0  
    personal: Optional[bool] = False
    settings: Optional[dict] = {}

    class Config:
        from_attributes = True
