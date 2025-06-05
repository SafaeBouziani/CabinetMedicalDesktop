# models/admin.py
from .UserModel import User

class Admin(User):
    def __init__(self, username, password, email, **kwargs):
        super().__init__(username, password, email, role="admin", **kwargs)
        self.permissions = kwargs.get('permissions', ['all'])
        
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "permissions": self.permissions
        })
        return base_dict