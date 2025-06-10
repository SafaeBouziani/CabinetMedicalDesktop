# Backend.py
from models import User, Patient, Doctor, Admin, Consultation
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime

class Database:
    def __init__(self, mongodb):
        self.mongodb = mongodb
    def add_user(self, user_data, role):
        # Generate a shared _id
        shared_id = ObjectId()
        user_data["_id"] = shared_id  # Apply same _id across all

        if role == "patient":
            if "age" not in user_data:
                raise ValueError("L'âge est requis pour un patient")
            user = Patient(**user_data)
            patient_data = user.to_dict()
            patient_data["_id"] = shared_id
            patient_data["password"] = generate_password_hash(patient_data["password"])
            self.mongodb.patients.insert_one(patient_data)
        elif role == "doctor":
            user = Doctor(**user_data)
            doctor_data = user.to_dict()
            doctor_data["_id"] = shared_id
            doctor_data["password"] = generate_password_hash(doctor_data["password"])
            self.mongodb.doctors.insert_one(doctor_data)
        elif role == "admin":
            user = Admin(**user_data)
        else:
            raise ValueError("Rôle invalide")

        user_data = user.to_dict()
        user_data["_id"] = shared_id
        user_data["password"] = generate_password_hash(user_data["password"])
        result = self.mongodb.users.insert_one(user_data)

        return str(shared_id)

    def get_user_by_role(self, role):
        return list(self.mongodb.users.find({"role": role}))

    def get_all_users(self):
        return list(self.mongodb.users.find())


    def update_user(self, user_id, new_data):
        user = self.mongodb.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("Utilisateur introuvable")

        if "password" in new_data:
            new_data["password"] = generate_password_hash(new_data["password"])

        role = user.get("role")

        if role == "patient":
            self.mongodb.patients.update_one({"_id": ObjectId(user_id)}, {"$set": new_data})
        elif role == "doctor":
            self.mongodb.doctors.update_one({"_id": ObjectId(user_id)}, {"$set": new_data})


        self.mongodb.users.update_one({"_id": ObjectId(user_id)}, {"$set": new_data})


    def delete_user(self, user_id):
        user = self.mongodb.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("Utilisateur introuvable")

        role = user.get("role")


        if role == "patient":
            self.mongodb.patients.delete_one({"_id": ObjectId(user_id)})
        elif role == "doctor":
            self.mongodb.doctors.delete_one({"_id": ObjectId(user_id)})


        self.mongodb.users.delete_one({"_id": ObjectId(user_id)})
    def get_user_consultations(self, user_id):
        user = self.mongodb.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("Utilisateur introuvable")

        role = user.get("role")

        if role == "patient":
            return list(self.mongodb.consultations.find({"patient_id": str(user_id)}))
        elif role == "doctor":
            return list(self.mongodb.consultations.find({"doctor_id": str(user_id)}))
        elif role == "admin":
            return list(self.mongodb.consultations.find())  # or return [] if admins don't need this
        else:
            raise ValueError("Rôle utilisateur non reconnu")
    def get_patient_consultations2(self, mongo_id):
        query = """
        MATCH (p:User {mongo_id: $mongo_id, role: 'patient'})-[c:CONSULTED_WITH]->(d:User {role: 'doctor'})
        RETURN 
            c.motif AS motif,
            c.date AS date,
            c.status AS status,
            c.diagnostic AS diagnostic,
            c.prescriptions AS prescriptions,
            d.name AS doctor
        ORDER BY c.date DESC
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, mongo_id=mongo_id)
                return [record.data() for record in result]
        except Exception as e:
            print(f"Erreur lors de la récupération des consultations pour le patient {mongo_id} : {e}")
            return []

    # CONSULTATION METHODS
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