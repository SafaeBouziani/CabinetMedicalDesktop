from PySide6.QtWidgets import QApplication
from database import MongoDBConnector, Neo4jConnector, DatabaseSyncManager
from auth import AuthManager
from views import MainWindow
from Backend import Database

import sys

def main():
    try:
        app = QApplication(sys.argv)
        
        mongodb = MongoDBConnector()
        neo4j = Neo4jConnector()
        
           
        sync_manager = DatabaseSyncManager(mongodb, neo4j)
        auth_manager = AuthManager(mongodb, neo4j)
        database = Database(mongodb)
        window = MainWindow(mongodb, neo4j, sync_manager, auth_manager, database)
        window.show()
        
        return app.exec()
    except Exception as e:
        print(f"Erreur critique : {str(e)}")
        return 1
    finally:
        if 'mongodb' in locals():
            mongodb.close()
        if 'neo4j' in locals():
            neo4j.close()

if __name__ == "__main__":
    sys.exit(main())