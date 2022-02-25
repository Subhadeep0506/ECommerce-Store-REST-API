from ma import ma
from models.user import UserModel

class UserSchema(ma.ModelSchema):
    # If the below Meta class is excluded, while fetching user information, we also fetch
    # the user password. So, password is included in the load_only tuple so that password field
    # is only loaded and not displayed.
    class Meta:
        model = UserModel
        load_only = ("password",)  # makes 'password' field load_only
        dump_only = ("id",)  # makes 'id' field dump_only.
