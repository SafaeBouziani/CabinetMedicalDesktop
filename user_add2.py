# Créer un nouvel utilisateur admin correctement
from auth.AuthManager import AuthManager
from database import MongoDBConnector  # Assurez-vous d'importer votre classe de base de données

# Créer une instance de la base de données
mongodb = MongoDBConnector()  # Ajustez selon votre configuration
neo4j = None  # Si vous utilisez Neo4j, initialisez-le ici

# Créer une instance de AuthManager
auth_manager = AuthManager(mongodb, neo4j)

user_data = {
    "username": "testadmin",
    "password": "votre_mot_de_passe",  # sera hashé automatiquement
    "role": "admin",
    "email": "admin@example.com",
    "name": "Admin Test"
}

# Utiliser l'instance pour appeler add_user
auth_manager.add_user(user_data)