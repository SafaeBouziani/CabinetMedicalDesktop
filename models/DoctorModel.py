# models/doctor.py
from .UserModel import User

class Doctor(User):
    def __init__(self, username, password, email, name, specialty, **kwargs):
        kwargs.pop("role", None)
        super().__init__(username, password, email, role="doctor", **kwargs)
        self.name = name
        self.specialty = specialty
        self.disponibilite = kwargs.get('disponibilite', [])
        self.consultations = []  # Liste des consultations du médecin
        
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "specialty": self.specialty,
            "disponibilite": self.disponibilite
        })
        return base_dict