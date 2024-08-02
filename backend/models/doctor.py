from pydantic import BaseModel
from typing import Optional

class Doctor(BaseModel):
    doctor_id: str
    name: str
    specialization: str
    type: str  # This indicates whether the doctor is freelance or registered
    organization_id: Optional[str] = None  # This will be None if the doctor is freelance

    _db = {}

    def save(self):
        Doctor._db[self.doctor_id] = self.dict()

    @staticmethod
    def get(doctor_id):
        data = Doctor._db.get(doctor_id)
        return Doctor(**data) if data else None

    def is_freelance(self):
        return self.organization_id is None

    def is_registered(self):
        return self.organization_id is not None
