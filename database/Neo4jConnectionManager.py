# database/neo4j_connector.py
from neo4j import GraphDatabase
from ConfigManagement import Config

class Neo4jConnector:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
            )
            self._create_constraints()
            print("Neo4j : connexion OK")
        except Exception as e:
            print(f"Erreur de connexion à Neo4j : {e}")
            self.driver = None
# database/neo4j_connector.py
    def _create_constraints(self):
        with self.driver.session() as session:
            try:
                session.run("CREATE CONSTRAINT FOR (u:User) REQUIRE u.mongo_id IS UNIQUE")
            except Exception:
                pass

    def close(self):
        if self.driver:
            self.driver.close()