from pydantic import BaseModel
from datetime import date

class Interaction(BaseModel):
    interaction_id: str
    doctor_id: str
    patient_id: str
    date: date
    notes: str

    _db = {}

    def save(self):
        Interaction._db[self.interaction_id] = self.dict()

    @staticmethod
    def get(interaction_id):
        data = Interaction._db.get(interaction_id)
        return Interaction(**data) if data else None

    @staticmethod
    def get_interactions_for_doctor(doctor_id):
        return [Interaction(**interaction) for interaction in Interaction._db.values() if interaction['doctor_id'] == doctor_id]
