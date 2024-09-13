from sqlalchemy import Column, String, Integer, JSON, BigInteger, Boolean
from sqlalchemy.orm import relationship
from api.lib.db import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False,unique=True)
    status = Column(Integer, default=0, nullable=False)
    personal = Column(Boolean, default=False, nullable=True)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)
    
    # Relationships
    members = relationship("Member", back_populates="organization")
    roles = relationship("Role", back_populates="organization") 
