from sqlalchemy.orm import Session
from app.models.db_model.admin import Admin
from app.models.db_model.user import User

def get_auth_type(principal_type: str, principal_id: int, db: Session):
    if principal_type == "USER":
        return db.query(User).filter(User.user_id == principal_id).first()
    elif principal_type == "ADMIN":
        return db.query(Admin).filter(Admin.admin_id == principal_id).first()
    return None
