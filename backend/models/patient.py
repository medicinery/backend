from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Patient(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    medical_history: List[str] = Field(default_factory=list)
    
    _db = {}

    def save(self):
        Patient._db[self.user_id] = self.dict()

    @staticmethod
    def get(user_id):
        data = Patient._db.get(user_id)
        return Patient(**data) if data else None

    def add_medical_record(self, record):
        self.medical_history.append(record)
        self.save()

    def get_medical_history(self):
        return self.medical_history
