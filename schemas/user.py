from marshmallow import Schema, fields

class UserSchema(Schema):
  # If the below Meta class is excluded, while fetching user information, we also fetch 
  # the user password. So, password is included in the load_only tuple so that password field
  # is only loaded and not displayed.
  class Meta:
    load_only = ("password", )  # makes 'password' field load_only
    dump_only = ("id", )  # makes 'id' field dump_only.
    
  id = fields.Int()
  username = fields.Str(required=True)
  password = fields.Str(required=True)
  