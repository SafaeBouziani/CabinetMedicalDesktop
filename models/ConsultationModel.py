# models/consultation.py
from datetime import datetime
from bson import ObjectId

class Consultation:
    def __init__(self, patient, doctor, date, motif, **kwargs):
        self.id = kwargs.get('_id', None)
        self.patient_id = patient.id if isinstance(patient, ObjectId) else patient
        self.doctor_id = doctor.id if isinstance(doctor, ObjectId) else doctor
        self.date = date
        self.motif = motif
        self.status = kwargs.get('status', 'programmé')
        self.diagnostic = kwargs.get('diagnostic', None)
        self.prescriptions = kwargs.get('prescriptions', [])
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "motif": self.motif,
            "status": self.status,
            "diagnostic": self.diagnostic,
            "prescriptions": self.prescriptions,
            "created_at": self.created_at
        }