from sqlalchemy.orm import Session
from sqlalchemy import func
from api.schemas.user import User
from api.schemas.organization import Organization
from api.schemas.member import Member
from api.schemas.role import Role

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Organization-related CRUD functions

def create_organization(db: Session, org_data: dict):
    new_org = Organization(**org_data)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

def get_organization_by_id(db: Session, org_id: int):
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_organization_name(db: Session, org_name: str):
    return db.query(Organization).filter(Organization.name == org_name).first()

def create_default_role(db:Session,org_id:int):
    owner_role = Role(name="Owner", description="Organization Owner", org_id=org_id)
    db.add(owner_role)
    db.commit()
    db.refresh(owner_role)
    return owner_role

# Member-related CRUD functions

def add_member(db: Session, invite_data: dict):
    new_member = Member(
        user_id=invite_data['user_id'],
        org_id=invite_data['org_id'],
        role_id=invite_data['role_id'],
        status=1  # Active status by default
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def get_member_by_user_id(db: Session, user_id: int):
    return db.query(Member).filter(Member.user_id == user_id).first()

def delete_member(db: Session, user_id: int):
    member = get_member_by_user_id(db, user_id)
    db.delete(member)
    db.commit()

def update_member_role(db: Session, user_id: int, new_role_id: int):
    member = get_member_by_user_id(db, user_id)
    member.role_id = new_role_id
    db.commit()
    return member


# Role-related CRUD functions

def create_role(db: Session, role_data: dict):
    new_role = Role(**role_data)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.name == role_name).first()

def get_member_by_user_and_org(db: Session, user_id: int, org_id: int):
    return db.query(Member).filter(Member.user_id == user_id, Member.org_id == org_id).first()

def update_member_role(db: Session, user_id: int, org_id: int, new_role_id: int):
    member = get_member_by_user_and_org(db, user_id, org_id)
    member.role_id = new_role_id
    db.commit()
    return member

# Stats-related CRUD functions

def get_role_wise_user_stats(db: Session):
    # Query to count users per role
    stats = (
        db.query(Role.name, func.count(Member.user_id))
        .join(Member, Member.role_id == Role.id)
        .group_by(Role.name)
        .all()
    )
    return [{"role": role, "user_count": user_count} for role, user_count in stats]

def get_organization_wise_member_stats(db: Session):
    # Query to count members per organization
    stats = (
        db.query(Organization.name, func.count(Member.user_id))
        .join(Member, Member.org_id == Organization.id)
        .group_by(Organization.name)
        .all()
    )
    return [{"organization": org_name, "member_count": member_count} for org_name, member_count in stats]

def get_organization_role_wise_user_stats(db: Session):
    # Query to count users per role per organization
    stats = (
        db.query(Organization.name, Role.name, func.count(Member.user_id))
        .join(Member, Member.org_id == Organization.id)
        .join(Role, Member.role_id == Role.id)
        .group_by(Organization.name, Role.name)
        .all()
    )
    return [
        {"organization": org_name, "role": role_name, "user_count": user_count}
        for org_name, role_name, user_count in stats
    ]

def get_filtered_stats(db: Session, from_time: int, to_time: int, status: int):
    # Query to get stats within a time range and status filter
    stats = (
        db.query(Organization.name, Role.name, func.count(Member.user_id))
        .join(Member, Member.org_id == Organization.id)
        .join(Role, Member.role_id == Role.id)
        .join(User, Member.user_id == User.id)
        .filter(User.created_at >= from_time, User.created_at <= to_time)
        .filter(Member.status == status)
        .group_by(Organization.name, Role.name)
        .all()
    )
    return [
        {"organization": org_name, "role": role_name, "user_count": user_count}
        for org_name, role_name, user_count in stats
    ]
