from fastapi import FastAPI
from api.routers import auth, member, stats
from api.lib.db import Base, engine

description ="""
AUTH  
- user can signup ,signin,reset password \n
MEMBERS
- invite member , delete member, update member role \n
STATS
- role wise users , organization wise members , organization wise role users , filtered stats
"""

app = FastAPI(version="1.0.0",title="backend auth service multi tenant",description=description)

Base.metadata.create_all(bind=engine)

app.include_router(router=auth.router, prefix="/auth", tags=["AUTH"])
app.include_router(router=member.router, prefix="/members", tags=["MEMBERS"])
app.include_router(router=stats.router, prefix="/stats", tags=["STATS"])

