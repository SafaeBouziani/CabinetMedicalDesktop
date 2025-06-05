from werkzeug.security import check_password_hash, generate_password_hash
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, mongodb, neo4j):
        self.mongodb = mongodb
        self.neo4j = neo4j

    def login(self, username, password):
        logger.debug(f"Tentative de connexion pour l'utilisateur : {username}")
        
        user = self.mongodb.users.find_one({"username": username})
        if user:
            logger.debug(f"Utilisateur trouvé : {username}")
            logger.debug(f"Rôle de l'utilisateur : {user.get('role', 'Non défini')}")
            
            if check_password_hash(user['password'], password):
                logger.debug("Authentification réussie")
                # On ne log pas le mot de passe hashé pour des raisons de sécurité
                user_info = {k:v for k,v in user.items() if k != 'password'}
                logger.debug(f"Données utilisateur : {user_info}")
                return user
            else:
                logger.debug("Mot de passe incorrect")
                raise ValueError("Nom d'utilisateur ou mot de passe incorrect")
        else:
            logger.debug(f"Aucun utilisateur trouvé avec le nom : {username}")
            raise ValueError("Nom d'utilisateur ou mot de passe incorrect")

    def add_user(self, user_data):
        # Vérifier si l'utilisateur existe déjà
        if self.mongodb.users.find_one({"username": user_data["username"]}):
            raise ValueError("Nom d'utilisateur déjà utilisé")
        if self.mongodb.users.find_one({"email": user_data["email"]}):
            raise ValueError("Email déjà utilisé")

        # Hasher le mot de passe
        user_data["password"] = generate_password_hash(user_data["password"])
        
        # Insérer l'utilisateur
        result = self.mongodb.users.insert_one(user_data)
        return str(result.inserted_id)