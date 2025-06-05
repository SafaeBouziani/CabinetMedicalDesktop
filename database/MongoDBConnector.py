
# database/mongodb_connector.py
from ConfigManagement import Config
from pymongo import MongoClient, errors

class MongoDBConnector:
    def __init__(self):
        self.client = None
        try:
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client[Config.DB_NAME]
            self.users = self.db["users"]
            self.patients = self.db["patients"]
            self.doctors = self.db["doctors"]
            self.consultations = self.db["consultations"]

            # Création des index
            self.users.create_index("username", unique=True)
            self.users.create_index("email", unique=True)
            self.users.create_index("role")
            self.patients.create_index("email", unique=True)
            self.doctors.create_index("email", unique=True)
            self.consultations.create_index([("patient_id", 1), ("doctor_id", 1)])

            self.client.admin.command('ping')
            print("MongoDB : connexion OK")

        except errors.ServerSelectionTimeoutError as err:
            print(f"Erreur de connexion à MongoDB : {err}")
            self.client = None

    def close(self):
        """Ferme la connexion à MongoDB"""
        if self.client:
            self.client.close()