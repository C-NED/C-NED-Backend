#db model 다형성(fk) 정의
# User ↔ Navigation
def user_navigation_join():
    return and_(
        foreign(Navigation.principal_id) == User.user_id,
        Navigation.principal_type == 'USER'
    )

# User ↔ Navigation
def admin_navigation_join():
    return and_(
        foreign(Navigation.principal_id) == Admin.admin_id,
        Navigation.principal_type == 'SERVICE_ADMIN'
    )