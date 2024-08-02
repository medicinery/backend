from pydantic import BaseModel
from typing import Optional
from .patient import Patient

class Doctor(BaseModel):
    doctor_id: str
    name: str
    specialization: str
    type: str  # e.g., 'primary', 'specialist'
    organization_id: Optional[str] = None

    def request_patient_history(self, patient: Patient) -> list:
        return patient.get_medical_history()
