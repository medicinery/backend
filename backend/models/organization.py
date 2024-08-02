from pydantic import BaseModel
from typing import List
from .doctor import Doctor
from .patient import Patient
from .interaction import Interaction

class Organization(BaseModel):
    organization_id: str
    name: str
    type: str  # e.g., 'hospital', 'clinic'
    doctors: List[Doctor] = []

    def add_doctor(self, doctor: Doctor):
        self.doctors.append(doctor)

    def get_doctors(self) -> List[Doctor]:
        return self.doctors

    def get_doctor_interactions(self, interactions: List[Interaction]) -> List[Interaction]:
        org_doctor_ids = {doctor.doctor_id for doctor in self.doctors}
        return [interaction for interaction in interactions if interaction.doctor_id in org_doctor_ids]

    def get_patient_history_for_doctor(self, doctor_id: str, interactions: List[Interaction], patients: List[Patient]) -> dict:
        patient_histories = {}
        for interaction in interactions:
            if interaction.doctor_id == doctor_id:
                patient = next((p for p in patients if p.user_id == interaction.patient_id), None)
                if patient:
                    patient_histories[patient.user_id] = patient.get_medical_history()
        return patient_histories
