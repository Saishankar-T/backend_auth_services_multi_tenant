from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.lib import crud, utils,db

router = APIRouter()

@router.get("/role-wise-users")
def role_wise_number_of_users(db: Session = Depends(db.get_db)):
    stats = crud.get_role_wise_user_stats(db)
    return stats

@router.get("/organization-wise-members")
def organization_wise_number_of_members(db: Session = Depends(db.get_db)):
    stats = crud.get_organization_wise_member_stats(db)
    return stats

@router.get("/organization-role-users")
def organization_role_wise_number_of_users(db: Session = Depends(db.get_db)):
    stats = crud.get_organization_role_wise_user_stats(db)
    return stats

# Adding filters to the above endpoints for "from" and "to" time and "status"
@router.get("/filtered-stats")
def filtered_stats(from_time: int, to_time: int, status: int, db: Session = Depends(db.get_db)):
    stats = crud.get_filtered_stats(db, from_time, to_time, status)
    return stats
