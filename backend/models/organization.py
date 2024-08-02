from pydantic import BaseModel
from typing import List

class Organization(BaseModel):
    organization_id: str
    name: str
    type: str
    doctors: List[str] = []  # List of doctor IDs registered under this organization

    _db = {}

    def save(self):
        Organization._db[self.organization_id] = self.dict()

    @staticmethod
    def get(organization_id):
        data = Organization._db.get(organization_id)
        return Organization(**data) if data else None

    def add_doctor(self, doctor):
        if not doctor.is_freelance():
            self.doctors.append(doctor.doctor_id)
            self.save()

    def get_doctors(self):
        return [Doctor.get(doctor_id) for doctor_id in self.doctors]

    def get_doctor_interactions(self, interactions):
        org_doctor_ids = self.doctors
        return [interaction for interaction in interactions if interaction.doctor_id in org_doctor_ids]

    def get_patient_history_for_doctor(self, doctor_id, interactions, patients):
        doctor_patient_ids = {interaction.patient_id for interaction in interactions if interaction.doctor_id == doctor_id}
        return {patient.user_id: patient.get_medical_history() for patient in patients if patient.user_id in doctor_patient_ids}
