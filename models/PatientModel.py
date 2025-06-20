from .UserModel import User

class Patient(User):
    def __init__(self, username, password, email, name, age, **kwargs):
        kwargs.pop("role", None)
        super().__init__(username, password, email, role="patient", **kwargs)
        self.name = name
        self.age = age
        self.consultations = []  # Liste des consultations du patient

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "age": self.age,
            "consultations": self.consultations
        })
        return base_dict
