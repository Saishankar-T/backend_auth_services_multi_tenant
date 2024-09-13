from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.lib.db import Base

class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=True)
    org_id = Column(Integer, ForeignKey('organization.id'), nullable=False)

    # Relationships
    members = relationship("Member", back_populates="role")
    organization = relationship("Organization", back_populates="roles") 
