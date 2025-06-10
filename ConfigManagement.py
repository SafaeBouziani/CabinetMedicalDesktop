# config.py

class Config:
    # MongoDB configuration
    MONGODB_URI = "mongodb+srv://fzboujrad:boujrad2003@cluster0.dnu3pdi.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "mydatabase"

    # Neo4j configuration (à remplacer par vos identifiants)
    NEO4J_URI = "neo4j+s://447894b9.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "SRH-EPsI_mIX5gx5rFttY_6NHpj-DzuVl3jQgu5dDBg"


    # Application configuration
    APP_NAME = "Système de Gestion Médicale"
    WINDOW_SIZE = {
        'width': 1200,
        'height': 800
    }