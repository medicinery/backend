import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(r'addpath to firebase credentials here')# i dont have path to our firebase creds just add it here#
firebase_admin.initialize_app(cred)
db = firestore.client()

#Patient Model creates a user and patient collection thought would make it more flexible
class Patient:
    def __init__(self, user_id, name, email, medical_history=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.medical_history = medical_history if medical_history is not None else []

    def save(self):
        try:
            # Save user and patient data
            user_ref = db.collection('users').document(self.user_id)
            user_ref.set({
                'name': self.name,
                'email': self.email
            })

            patient_ref = db.collection('patients').document(self.user_id)
            patient_ref.set({
                'name': self.name,
                'email': self.email,
                'medical_history': self.medical_history
            })
        except Exception as e:
            print(f"An error occurred while saving patient: {e}")

    @staticmethod
    def get(user_id):
        try:
            patient_ref = db.collection('patients').document(user_id)
            patient = patient_ref.get()
            if patient.exists:
                data = patient.to_dict()
                return Patient(
                    user_id=user_id,
                    name=data.get('name', ''),
                    email=data.get('email', ''),
                    medical_history=data.get('medical_history', [])
                )
            else:
                raise ValueError("Patient does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving patient: {e}")
            return None

    def add_medical_record(self, record):
        """Add a new medical record to the patient's history."""
        self.medical_history.append(record)
        self.save()  

    def get_medical_history(self):
        """Retrieve the patient's medical history."""
        return self.medical_history

class Doctor:
    def __init__(self, doctor_id, name, specialization, type, organization_id=None):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.type = type  
        self.organization_id = organization_id

    def save(self):
        try:
            doctor_ref = db.collection('doctors').document(self.doctor_id)
            doctor_ref.set({
                'name': self.name,
                'specialization': self.specialization,
                'type': self.type,
                'organization_id': self.organization_id
            })
        except Exception as e:
            print(f"An error occurred while saving doctor: {e}")

    @staticmethod
    def get(doctor_id):
        try:
            doctor_ref = db.collection('doctors').document(doctor_id)
            doctor = doctor_ref.get()
            if doctor.exists:
                return Doctor(
                    doctor_id,
                    doctor.to_dict()['name'],
                    doctor.to_dict()['specialization'],
                    doctor.to_dict()['type'],
                    doctor.to_dict().get('organization_id')
                )
            else:
                raise ValueError("Doctor does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving doctor: {e}")
            return None

    def request_patient_history(self, patient_id):
        try:
            patient = Patient.get(patient_id)
            if patient:
                return patient.get_medical_history()
            else:
                raise ValueError("Patient does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving patient history: {e}")
            return None

# Organization Model
class Organization:
    def __init__(self, organization_id, name, type):
        self.organization_id = organization_id
        self.name = name
        self.type = type  

    def save(self):
        try:
            org_ref = db.collection('organizations').document(self.organization_id)
            org_ref.set({
                'name': self.name,
                'type': self.type
            })
        except Exception as e:
            print(f"An error occurred while saving organization: {e}")

    @staticmethod
    def get(organization_id):
        try:
            org_ref = db.collection('organizations').document(organization_id)
            organization = org_ref.get()
            if organization.exists:
                return Organization(
                    organization_id,
                    organization.to_dict()['name'],
                    organization.to_dict()['type']
                )
            else:
                raise ValueError("Organization does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving organization: {e}")
            return None

    def add_doctor(self, doctor_id):
        try:
            org_ref = db.collection('organizations').document(self.organization_id)
            org_ref.update({
                'doctors': firestore.ArrayUnion([doctor_id])
            })
        except Exception as e:
            print(f"An error occurred while adding doctor to organization: {e}")

    def get_doctors(self):
        try:
            org_ref = db.collection('organizations').document(self.organization_id)
            org = org_ref.get()
            if org.exists:
                return org.to_dict().get('doctors', [])
            else:
                raise ValueError("Organization does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving doctors for organization: {e}")
            return []

    def get_doctor_interactions(self):
        try:
            # Get the list of doctors in the organization
            doctor_ids = self.get_doctors()
            interactions = []
            
            # Retrieve all interactions involving these doctors
            if doctor_ids:
                interaction_refs = db.collection('interactions').where(
                    'doctor_id', 'in', doctor_ids).stream()
                for interaction in interaction_refs:
                    interactions.append(interaction.to_dict())

            return interactions
        except Exception as e:
            print(f"An error occurred while retrieving doctor interactions: {e}")
            return []

    def get_patient_history_for_doctor(self, doctor_id):
        try:
            # Get all interactions for the given doctor
            interaction_refs = db.collection('interactions').where(
                'doctor_id', '==', doctor_id).stream()
            patient_ids = set()
            
            for interaction in interaction_refs:
                patient_ids.add(interaction.to_dict()['patient_id'])

            # Retrieve medical history for each patient
            patient_histories = {}
            for patient_id in patient_ids:
                patient = Patient.get(patient_id)
                if patient:
                    patient_histories[patient_id] = patient.get_medical_history()

            return patient_histories
        except Exception as e:
            print(f"An error occurred while retrieving patient history for doctor: {e}")
            return {}

# Interaction class to store record of interaction between user and doctors to be monitored by organisation lol needs to only be viewable by relevant doctor and organisations
class Interaction:
    def __init__(self, interaction_id, doctor_id, patient_id, date, notes):
        self.interaction_id = interaction_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date = date
        self.notes = notes

    def save(self):
        try:
            interaction_ref = db.collection('interactions').document(self.interaction_id)
            interaction_ref.set({
                'doctor_id': self.doctor_id,
                'patient_id': self.patient_id,
                'date': self.date,
                'notes': self.notes
            })
        except Exception as e:
            print(f"An error occurred while saving interaction: {e}")

    @staticmethod
    def get(interaction_id):
        try:
            interaction_ref = db.collection('interactions').document(interaction_id)
            interaction = interaction_ref.get()
            if interaction.exists:
                data = interaction.to_dict()
                return Interaction(
                    interaction_id=data['interaction_id'],
                    doctor_id=data['doctor_id'],
                    patient_id=data['patient_id'],
                    date=data['date'],
                    notes=data['notes']
                )
            else:
                raise ValueError("Interaction does not exist")
        except Exception as e:
            print(f"An error occurred while retrieving interaction: {e}")
            return None
