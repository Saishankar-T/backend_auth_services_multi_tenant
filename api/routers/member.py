from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.lib import crud, utils,db
from api.models.member import InviteMember, UpdateRole

router = APIRouter()

@router.post("/invite")
def invite_member(invite_data: InviteMember, db: Session = Depends(db.get_db)):
    # Invite logic
    user = crud.get_user_by_email(db, invite_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Add member entry in Member table
    invite_data = invite_data.model_dump()
    invite_data["user_id"] = user.id
    member = crud.add_member(db, invite_data)
    # Send invite email
    utils.send_invite_email(invite_data["email"])
    return {"message": "Member invited successfully"}

@router.delete("/delete/{user_id}")
def delete_member(user_id: int, db: Session = Depends(db.get_db)):
    member = crud.get_member_by_user_id(db, user_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_member(db, user_id)
    return {"message": "Member deleted successfully"}

@router.put("/update-role/{user_id}/{org_id}")
def update_user_role(user_id: int, org_id: int, new_role_id: int, db: Session = Depends(db.get_db)):
    # Get the member record for the user in the organization
    member = crud.get_member_by_user_and_org(db, user_id, org_id)
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in this organization")

    # Update the role of the user in this organization
    crud.update_member_role(db, user_id, org_id, new_role_id)

    return {"message": "User role updated successfully"}

