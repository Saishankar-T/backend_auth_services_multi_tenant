from sqlalchemy import Column, Integer, JSON, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from api.lib.db import Base

class Member(Base):
    __tablename__ = "member"
    
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey('organization.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="organizations")
    organization = relationship("Organization", back_populates="members")
    role = relationship("Role", back_populates="members")
