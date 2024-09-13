from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
databasename = os.getenv("databasename")

# SQLAlchemy database URL (replace with your database URL)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(username,password,host,databasename)  # Or MySQL, depending on what you're using.

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
