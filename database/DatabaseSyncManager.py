class DatabaseSyncManager:
    def __init__(self, mongodb, neo4j):
        self.mongodb = mongodb
        self.neo4j = neo4j

    def sync_user(self, user_data):
        """Synchronise uniquement les patients et les médecins vers Neo4j"""
        if user_data["role"] not in ["patient", "doctor"]:
            return  # Ignorer les autres rôles (ex: admin)

        with self.neo4j.driver.session() as session:
            session.run("""
                MERGE (u:User {mongo_id: $id})
                SET u.username = $username,
                    u.role = $role,
                    u.name = $name,
                    u.email = $email
            """,
                id=str(user_data['_id']),
                username=user_data['username'],
                role=user_data['role'],
                name=user_data.get('name', ''),
                email=user_data.get('email', '')
            )

    def sync_all(self):
        """Synchronise uniquement les patients et médecins"""
        users = self.mongodb.users.find({"role": {"$in": ["patient", "doctor"]}})
        for user in users:
            self.sync_user(user)

    def delete_user(self, user_id):
        """Supprime l'utilisateur de Neo4j si présent"""
        with self.neo4j.driver.session() as session:
            session.run("""
                MATCH (u:User {mongo_id: $id})
                DETACH DELETE u
            """, id=str(user_id))
    def sync_consultations(self):
        """Sync consultations from MongoDB to Neo4j as relationships with properties"""
        consultations = self.mongodb.consultations.find()

        for consultation in consultations:
            try:
                patient_id = str(consultation["patient_id"])
                doctor_id = str(consultation["doctor_id"])
                motif = consultation.get("motif", "")
                date = consultation.get("date", None)
                time = consultation.get("time", None)

                with self.neo4j.driver.session() as session:
                    session.run("""
                        MATCH (p:User {mongo_id: $patient_id, role: 'patient'})
                        MATCH (d:User {mongo_id: $doctor_id, role: 'doctor'})
                        MERGE (p)-[c:CONSULTED_WITH {date: $date, time: $time}]->(d)
                        SET c.motif = $motif
                    """, 
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    motif=motif,
                    date=date,
                    time=time)
            except Exception as e:
                print(f"Erreur lors de la synchronisation d'une consultation : {e}")
