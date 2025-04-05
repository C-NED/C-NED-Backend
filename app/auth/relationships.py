#db model 다형성(fk) 정의
from sqlalchemy.sql import and_
from sqlalchemy.orm import foreign

# User ↔ Navigation
def user_navigation_join(User=None,Navigation=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.navigation import Navigation as NavCls
    User = User or UserCls
    Navigation = Navigation or NavCls

    return and_(
        foreign(Navigation.principal_id) == User.user_id,
        Navigation.principal_type == 'USER'
    )

# Admin ↔ Navigation
def admin_navigation_join(Admin:None,Navigation:None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.navigation import Navigation as Navcls
    Admin = Admin or AdCls
    Navigation = Navigation or Navcls

    return and_(
        foreign(Navigation.principal_id) == Admin.admin_id,
        Navigation.principal_type == 'SERVICE_ADMIN'
    )


# User <=> Outbreak
def user_outbreak_join(User: None,Outbreak:None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.outbreak import Outbreak as OutCls
    User = User or UserCls
    Outbreak = Outbreak or OutCls

    return and_(
        foreign(Outbreak.principal_id) == User.user_id,
        Outbreak.principal_type == 'USER'
    )

# User <=> vsl
def user_vsl_join(User:None,Vsl:None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.vsl import Vsl as VslCls
    User = User or UserCls
    Vsl = Vsl or VslCls

    return and_(
        foreign(Vsl.principal_id) == User.user_id,
        Vsl.principal_type == 'USER'
    )

# User <=> caution
def user_caution_join(User:None,Caution:None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.caution import Caution as CauCls
    User = User or UserCls
    Caution = Caution or CauCls

    return and_(
        foreign(Caution.principal_id) == User.user_id,
        Caution.principal_type == 'USER'
    )

# User <=> dangerous_incident
def user_dangerous_join(User: None,DangerousIncident:None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.dangerous_incident import DangerousIncident as DangerCls
    User = User or UserCls
    DangerousIncident = DangerousIncident or DangerCls

    return and_(
        foreign(DangerousIncident.principal_id) == User.user_id,
        DangerousIncident.principal_type == 'USER'
    )


# Admin <=> Outbreak
def admin_outbreak_join(Admin:None,Outbreak:None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.outbreak import Outbreak as OutCls
    Admin = Admin or AdCls
    Outbreak = Outbreak or OutCls

    return and_(
        foreign(Outbreak.principal_id) == Admin.admin_id,
        Outbreak.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> vsl
def admin_vsl_join(Admin:None,Vsl:None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.vsl import Vsl as VslCls
    Admin = Admin or AdCls
    Vsl = Vsl or VslCls

    return and_(
        foreign(Vsl.principal_id) == Admin.admin_id,
        Vsl.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> caution
def admin_caution_join(Admin:None,Caution:None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.caution import Caution as CauCls
    Admin = Admin or AdCls
    Caution = Caution or CauCls

    return and_(
        foreign(Caution.principal_id) == Admin.admin_id,
        Caution.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> dangerout_incident
def admin_dangerous_join(Admin:None,DangerousIncident:None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.dangerous_incident import DangerousIncident as DangerCls
    Admin = Admin or AdCls
    DangerousIncident = DangerousIncident or DangerCls

    return and_(
        foreign(DangerousIncident.principal_id) == Admin.admin_id,
        DangerousIncident.principal_type == 'ROAD_ADMIN'
    )