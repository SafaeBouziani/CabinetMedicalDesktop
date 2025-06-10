# Backend.py
from models import User, Patient, Doctor, Admin, Consultation
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

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
