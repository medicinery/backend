class Doctor:
    _db = {}

    def __init__(self, doctor_id, name, specialization, type, organization_id=None):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.type = type
        self.organization_id = organization_id

    def save(self):
        Doctor._db[self.doctor_id] = self

    @staticmethod
    def get(doctor_id):
        return Doctor._db.get(doctor_id)

    def request_patient_history(self, patient):
        return patient.get_medical_history()
