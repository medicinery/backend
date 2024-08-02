from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Patient(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    medical_history: Optional[List[str]] = []

    def add_medical_record(self, record: str):
        """Add a new medical record to the patient's history."""
        self.medical_history.append(record)

    def get_medical_history(self) -> List[str]:
        """Retrieve the patient's medical history."""
        return self.medical_history
