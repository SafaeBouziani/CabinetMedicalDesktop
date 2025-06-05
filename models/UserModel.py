# models/user.py
class User:
    def __init__(self, username, password, email, role, **kwargs):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.last_login = kwargs.get('last_login', None)
        self._id = kwargs.get('_id', None)  # Pour MongoDB
        
    def to_dict(self):
        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role,
            "last_login": self.last_login
        }
        if self._id:
            data['_id'] = self._id
        return data