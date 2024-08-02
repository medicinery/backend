import unittest
from datetime import date
from models.patient import Patient
from models.doctor import Doctor
from models.organization import Organization
from models.interaction import Interaction

class TestModels(unittest.TestCase):
    
    def setUp(self):
        # Clear the in-memory "databases"
        Patient._db.clear()
        Doctor._db.clear()
        Organization._db.clear()
        Interaction._db.clear()

        # Create instances
        self.patient1 = Patient(user_id="p1", name="Alice", email="alice@example.com")
        self.patient2 = Patient(user_id="p2", name="Bob", email="bob@example.com")
        self.doctor1 = Doctor(doctor_id="d1", name="Dr. Smith", specialization="Cardiology", type="specialist")
        self.organization = Organization(organization_id="org1", name="HealthCare Inc.", type="hospital")
        self.interaction1 = Interaction(interaction_id="i1", doctor_id="d1", patient_id="p1", date=date.today(), notes="Checkup for Alice")
        self.interaction2 = Interaction(interaction_id="i2", doctor_id="d1", patient_id="p2", date=date.today(), notes="Checkup for Bob")
        
        # Save instances to the "database"
        self.patient1.save()
        self.patient2.save()
        self.doctor1.save()
        self.organization.save()
        self.interaction1.save()
        self.interaction2.save()
        
        self.organization.add_doctor(self.doctor1)
    
    def test_add_medical_record(self):
        self.patient1.add_medical_record("Medical record 1 for Alice")
        self.assertIn("Medical record 1 for Alice", self.patient1.medical_history)
    
    def test_get_medical_history(self):
        self.patient2.add_medical_record("Medical record for Bob")
        medical_history = self.patient2.get_medical_history()
        self.assertEqual(medical_history, ["Medical record for Bob"])
    
    def test_request_patient_history(self):
        self.patient1.add_medical_record("Medical record 1 for Alice")
        history = self.doctor1.request_patient_history(self.patient1)
        self.assertEqual(history, ["Medical record 1 for Alice"])
    
    def test_add_doctor(self):
        self.assertIn(self.doctor1, self.organization.get_doctors())
    
    def test_get_doctors(self):
        doctors = self.organization.get_doctors()
        self.assertEqual(doctors, [self.doctor1])
    
    def test_get_doctor_interactions(self):
        doctor_interactions = self.organization.get_doctor_interactions([self.interaction1, self.interaction2])
        self.assertEqual(doctor_interactions, [self.interaction1, self.interaction2])
    
    def test_get_patient_history_for_doctor(self):
        self.patient1.add_medical_record("Medical record 1 for Alice")
        self.patient2.add_medical_record("Medical record for Bob")
        patient_histories = self.organization.get_patient_history_for_doctor("d1", [self.interaction1, self.interaction2], [self.patient1, self.patient2])
        self.assertEqual(patient_histories, {
            "p1": ["Medical record 1 for Alice"],
            "p2": ["Medical record for Bob"]
        })
    
    def test_get_interactions_for_doctor(self):
        doctor_interactions = Interaction.get_interactions_for_doctor("d1")
        self.assertEqual(doctor_interactions, [self.interaction1, self.interaction2])

if __name__ == "__main__":
    unittest.main()
