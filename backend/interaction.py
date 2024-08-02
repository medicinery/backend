from pydantic import BaseModel
from datetime import date

class Interaction(BaseModel):
    interaction_id: str
    doctor_id: str
    patient_id: str
    date: date
    notes: str

    @staticmethod
    def get_interactions_for_doctor(doctor_id: str, interactions: list) -> list:
        return [interaction for interaction in interactions if interaction.doctor_id == doctor_id]
