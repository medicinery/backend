from pydantic import BaseModel
from typing import Optional

class Doctor(BaseModel):
    doctor_id: str
    name: str
    specialization: str
    type: str
    organization_id: Optional[str] = None

    _db = {}

    def save(self):
        Doctor._db[self.doctor_id] = self.dict()

    @staticmethod
    def get(doctor_id):
        data = Doctor._db.get(doctor_id)
        return Doctor(**data) if data else None

    def request_patient_history(self, patient):
        return patient.get_medical_history()
