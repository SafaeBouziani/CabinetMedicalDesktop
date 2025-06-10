
# database/mongodb_connector.py
from ConfigManagement import Config
from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime


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

    def add_consultation(self, consultation_data):
        """Ajouter une nouvelle consultation"""
        try:
            # Vérifier que le patient et le médecin existent
            patient = self.mongodb.users.find_one({"_id": ObjectId(consultation_data["patient_id"])})
            doctor = self.mongodb.users.find_one({"_id": ObjectId(consultation_data["doctor_id"])})
            
            if not patient:
                raise ValueError("Patient introuvable")
            if not doctor:
                raise ValueError("Médecin introuvable")
            
            # Créer la consultation
            consultation = {
                "patient_id": ObjectId(consultation_data["patient_id"]),
                "doctor_id": ObjectId(consultation_data["doctor_id"]),
                "date": consultation_data["date"],
                "motif": consultation_data["motif"],
                "status": consultation_data.get("status", "programmé"),
                "diagnostic": consultation_data.get("diagnostic"),
                "prescriptions": consultation_data.get("prescriptions", []),
                "created_at": consultation_data.get("created_at", datetime.utcnow())
            }
            
            result = self.mongodb.consultations.insert_one(consultation)
            return result.inserted_id
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout de la consultation: {str(e)}")
    
    def get_consultations_by_doctor(self, doctor_id, status_filter=None):
        """Récupérer les consultations d'un médecin"""
        try:
            query = {"doctor_id": ObjectId(doctor_id)}
            if status_filter:
                query["status"] = status_filter
            
            consultations = list(self.mongodb.consultations.find(query).sort("date", -1))
            return consultations
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des consultations: {str(e)}")
    
    def get_consultations_by_patient(self, patient_id):
        """Récupérer les consultations d'un patient"""
        try:
            consultations = list(self.mongodb.consultations.find(
                {"patient_id": ObjectId(patient_id)}
            ).sort("date", -1))
            return consultations
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des consultations: {str(e)}")
    
    def update_consultation(self, consultation_id, updated_data):
        """Mettre à jour une consultation"""
        try:
            # Préparer les données de mise à jour
            update_fields = {}
            for key, value in updated_data.items():
                if key in ["date", "motif", "status", "diagnostic", "prescriptions"]:
                    update_fields[key] = value
            
            if not update_fields:
                raise ValueError("Aucune donnée valide à mettre à jour")
            
            update_fields["updated_at"] = datetime.utcnow()
            
            result = self.mongodb.consultations.update_one(
                {"_id": ObjectId(consultation_id)},
                {"$set": update_fields}
            )
            
            if result.matched_count == 0:
                raise ValueError("Consultation introuvable")
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la consultation: {str(e)}")
    
    def delete_consultation(self, consultation_id):
        """Supprimer une consultation"""
        try:
            result = self.mongodb.consultations.delete_one({"_id": ObjectId(consultation_id)})
            
            if result.deleted_count == 0:
                raise ValueError("Consultation introuvable")
            
            return True
            
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression de la consultation: {str(e)}")
    
    def get_consultation_by_id(self, consultation_id):
        """Récupérer une consultation par son ID"""
        try:
            consultation = self.mongodb.consultations.find_one({"_id": ObjectId(consultation_id)})
            return consultation
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la consultation: {str(e)}")
    
    def get_user_by_id(self, user_id):
        """Récupérer un utilisateur par son ID"""
        try:
            if isinstance(user_id, str):
                user_id = ObjectId(user_id)
            user = self.mongodb.users.find_one({"_id": user_id})
            return user
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
    
    def get_all_consultations(self):
        """Récupérer toutes les consultations (pour admin)"""
        try:
            consultations = list(self.mongodb.consultations.find().sort("date", -1))
            return consultations
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des consultations: {str(e)}")
    
    def get_consultations_stats(self, doctor_id=None):
        """Récupérer les statistiques des consultations"""
        try:
            match_stage = {}
            if doctor_id:
                match_stage = {"doctor_id": ObjectId(doctor_id)}
            
            pipeline = [
                {"$match": match_stage},
                {"$group": {
                    "_id": "$status",
                    "count": {"$sum": 1}
                }}
            ]
            
            stats = list(self.mongodb.consultations.aggregate(pipeline))
            return {stat["_id"]: stat["count"] for stat in stats}
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques: {str(e)}")