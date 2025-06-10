from bson import ObjectId, errors as bson_errors

from database.Neo4jConnectionManager import Neo4jConnector

class ConsultationService:
    def __init__(self, mongodb):
        self.mongodb = mongodb
        self.neo4j = Neo4jConnector()

    def get_consultations(self, mongo_id):
        if not self.neo4j.driver:
            print("[WARN] Neo4j not connected.")
            return []

        query = """
        MATCH (p:User {mongo_id: $mongo_id, role: 'patient'})-[c:CONSULTED_WITH]->(d:User {role: 'doctor'})
        RETURN 
            c.motif AS motif,
            c.date AS date,
            c.status AS status,
            c.diagnostic AS diagnostic,
            c.prescriptions AS prescriptions,
            d.name AS doctor_name
        ORDER BY c.date DESC
        """

        try:
            with self.neo4j.driver.session() as session:
                result = session.run(query, mongo_id=mongo_id)
                consultations = [record.data() for record in result]

                # Convert string IDs to ObjectId only if valid
                doctor_ids = []
                for c in consultations:
                    doc_id = c.get("doctor_id")
                    try:
                        doctor_ids.append(ObjectId(doc_id))
                    except (bson_errors.InvalidId, TypeError):
                        print(f"[WARN] Invalid doctor_id: {doc_id}")

                # Fetch doctor names from MongoDB
                doctor_map = {
                    str(doc["_id"]): doc.get("name", "Nom indisponible")
                    for doc in self.mongodb.doctors.find({"_id": {"$in": doctor_ids}}, {"name": 1})
                }

                # Add doctor names back to consultations
                for c in consultations:
                    c["doctor"] = c.get("doctor_name", "Docteur inconnu")

                return consultations

        except Exception as e:
            print(f"[ERROR] Neo4j consultation fetch failed: {e}")
            return []
