from sqlalchemy import Column, String, Integer, JSON, BigInteger
from sqlalchemy.orm import relationship
from api.lib.db import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile = Column(JSON, default={}, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)
    
    # Relationships
    organizations = relationship("Member", back_populates="user", cascade="all, delete-orphan")
