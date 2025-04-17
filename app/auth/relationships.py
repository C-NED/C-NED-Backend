#db model 다형성(fk) 정의
from sqlalchemy.sql import and_
from sqlalchemy.orm import foreign,remote

# User ↔ Navigation
def user_navigation_join(User=None,Navigation=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.navigation import Navigation as NavCls
    User = User or UserCls
    Navigation = Navigation or NavCls

    return and_(
        foreign(Navigation.principal_id) == remote(User.user_id),
        Navigation.principal_type == 'USER'
    )

# Admin ↔ Navigation
def admin_navigation_join(Admin=None,Navigation=None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.navigation import Navigation as Navcls
    Admin = Admin or AdCls
    Navigation = Navigation or Navcls

    return and_(
        foreign(Navigation.principal_id) == remote(Admin.admin_id),
        Navigation.principal_type == 'SERVICE_ADMIN'
    )


# User <=> Outbreak
def user_outbreak_join(User= None,Outbreak=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.outbreak import Outbreak as OutCls
    User = User or UserCls
    Outbreak = Outbreak or OutCls

    return and_(
        foreign(Outbreak.principal_id) == remote(User.user_id),
        Outbreak.principal_type == 'USER'
    )

# User <=> vsl
def user_vsl_join(User=None,Vsl=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.vsl import Vsl as VslCls
    User = User or UserCls
    Vsl = Vsl or VslCls

    return and_(
        foreign(Vsl.principal_id) == remote(User.user_id),
        Vsl.principal_type == 'USER'
    )

# User <=> caution
def user_caution_join(User=None,Caution=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.caution import Caution as CauCls
    User = User or UserCls
    Caution = Caution or CauCls

    return and_(
        foreign(Caution.principal_id) == remote(User.user_id),
        Caution.principal_type == 'USER'
    )

# User <=> dangerous_incident
def user_dangerous_join(User=None,DangerousIncident=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.dangerous_incident import DangerousIncident as DangerCls
    User = User or UserCls
    incident_Cls = DangerousIncident or DangerCls

    return and_(
        foreign(incident_Cls.principal_id) == remote(User.user_id),
        incident_Cls.principal_type == 'USER'
    )


# Admin <=> Outbreak
def admin_outbreak_join(Admin=None,Outbreak=None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.outbreak import Outbreak as OutCls
    Admin = Admin or AdCls
    Outbreak = Outbreak or OutCls

    return and_(
        foreign(Outbreak.principal_id) == remote(Admin.admin_id),
        Outbreak.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> vsl
def admin_vsl_join(Admin=None,Vsl=None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.vsl import Vsl as VslCls
    Admin = Admin or AdCls
    Vsl = Vsl or VslCls

    return and_(
        foreign(Vsl.principal_id) == remote(Admin.admin_id),
        Vsl.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> caution
def admin_caution_join(Admin=None,Caution=None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.caution import Caution as CauCls
    Admin = Admin or AdCls
    Caution = Caution or CauCls

    return and_(
        foreign(Caution.principal_id) == remote(Admin.admin_id),
        Caution.principal_type == 'ROAD_ADMIN'
    )

# Admin <=> dangerout_incident
def admin_dangerous_join(Admin=None,DangerousIncident=None):
    from app.models.db_model.admin import Admin as AdCls
    from app.models.db_model.dangerous_incident import DangerousIncident as DangerCls
    Admin = Admin or AdCls
    incident_Cls = DangerousIncident or DangerCls

    return and_(
        foreign(incident_Cls.principal_id) == remote(Admin.admin_id),
        incident_Cls.principal_type == 'ROAD_ADMIN'
    )


#user - refresh_token

def user_refresh_join(User=None,RefreshToken=None):
    from app.models.db_model.user import User as UserCls
    from app.models.db_model.refresh_token import RefreshToken as RefreshCls
    User = User or UserCls
    RefreshToken = RefreshToken or RefreshCls

    return and_(
        foreign(RefreshToken.principal_id) == remote(User.user_id),
        RefreshToken.principal_type == 'USER'
    )

def admin_refresh_join(Admin=None,RefreshToken=None):
    from app.models.db_model.admin import Admin as AdsCls
    from app.models.db_model.refresh_token import RefreshToken as RefreshCls
    Admin = Admin or AdsCls
    RefreshToken = RefreshToken or RefreshCls

    return and_(
        foreign(RefreshToken.principal_id) == remote(Admin.admin_id),
        RefreshToken.principal_type == 'ADMIN'
    )

def roadinfo_caution_join(RoadInfo=None,Caution=None):
    from app.models.db_model.road_info import RoadInfo as RoadInfoCls
    from app.models.db_model.caution import Caution as CautionCls
    RoadInfo = RoadInfo or RoadInfoCls
    Caution = Caution or CautionCls

    return and_(
        foreign(Caution.route_no) == remote(RoadInfo.route_no),
        Caution.route_no == remote(RoadInfo.route_no)
    )

def roadinfo_outbreak_join(RoadInfo=None,Outbreak=None):
    from app.models.db_model.road_info import RoadInfo as RoadInfoCls
    from app.models.db_model.outbreak import Outbreak as OutbreakCls
    RoadInfo = RoadInfo or RoadInfoCls
    Outbreak = Outbreak or OutbreakCls

    return and_(
        foreign(Outbreak.road_no) == remote(RoadInfo.road_no),
        Outbreak.road_no == remote(RoadInfo.road_no)
    )

def roadinfo_vsl_join(RoadInfo=None,Vsl=None):
    from app.models.db_model.road_info import RoadInfo as RoadInfoCls
    from app.models.db_model.vsl import Vsl as VslCls
    RoadInfo = RoadInfo or RoadInfoCls
    Vsl = Vsl or VslCls

    return and_(
        foreign(Vsl.road_no) == remote(RoadInfo.road_no),
        Vsl.road_no == remote(RoadInfo.road_no)
    )