# Créer un nouveau patient dans la base de données
from auth.AuthManager import AuthManager
from database import MongoDBConnector  # Assurez-vous que cette classe est bien configurée
from database.Neo4jConnectionManager import Neo4jConnector  # Si vous utilisez Neo4j

# Initialisation des connecteurs
mongodb = MongoDBConnector()  # Adapter si besoin
neo4j = None  # Adapter si besoin
# Création de l'AuthManager
auth_manager = AuthManager(mongodb, neo4j)

user_data = {
    "username": "Patient",
    "password": "votre_mot_de_passe",  # sera hashé automatiquement
    "role": "patient",
    "email": "patient@example.com",
    "name": "Patient"
}

# Ajouter le patient à la base de données
auth_manager.add_user(patient_data)
