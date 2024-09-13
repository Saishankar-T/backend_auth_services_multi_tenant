from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.lib import crud, utils, db
from api.models.user import UserCreate, UserResponse
from api.models.organization import OrganizationCreate
from api.lib.utils import create_jwt_token

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, organization: OrganizationCreate, db: Session = Depends(db.get_db)):
    # Check if the user already exists
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving the user
    hashed_password = utils.hash_password(user.password)
    user_data = user.model_dump()
    user_data['password'] = hashed_password

    #check if organization already exists
    db_org = crud.get_organization_name(db,organization.name)
    org_data = organization.model_dump()
    if not db_org:
        # raise HTTPException(status_code=400,detail="Organization already registered")
        # Create the organization
        created_organization = crud.create_organization(db, org_data)
    else :
        created_organization = db_org
    
    created_role = crud.create_default_role(db,created_organization.id)

    # Create the user
    created_user = crud.create_user(db, user_data)

    member_data = {
        "user_id": created_user.id,
        "org_id": created_organization.id,
        "role_id": created_role.id,
    }
    crud.add_member(db, member_data)

    # Generate JWT token after signup
    access_token = create_jwt_token({"sub": created_user.email})
    
    utils.send_welcome_email(str(user.email))

    return UserResponse(email=created_user.email, access_token=access_token)

@router.post("/signin")
def signin(email: str, password: str, db: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(db, email)
    if not user or not utils.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = create_jwt_token({"sub": user.email})
    return {"access_token": access_token}

@router.post("/reset-password")
def reset_password(email: str, db: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Reset password logic
    new_password = utils.generate_random_password()
    user.password = utils.hash_password(new_password)
    db.commit()
    
    # Send reset password email
    utils.send_password_reset_email(email, new_password)
    
    return {"message": "Password reset successfully","new_password":new_password}
