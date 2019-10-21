import chronos_sdk
def Fgs_user_define(Fgs_logincode, Fgs_password, Fgs_type):
    fgs_user = chronos_sdk.FgsUser
    fgs_user.login_code = Fgs_logincode
    fgs_user.password = Fgs_password
    fgs_user.login_type = Fgs_type
    return fgs_user