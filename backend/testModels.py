from UserModel import Patient, Doctor, Organization, Interaction
def test_models():
    # Create and save Patient (which also creates a User)
    patient = Patient('patient1', 'Jane Smith', 'jane.smith@example.com')
    patient.save()

    # Add medical records
    record1 = {
        'date': '2024-01-15',
        'illness': 'Flu',
        'specialist': 'Dr. Alice Johnson',
        'notes': 'Diagnosed with flu. Prescribed rest and fluids.'
    }

    record2 = {
        'date': '2024-03-22',
        'illness': 'Headache',
        'specialist': 'Dr. Robert Smith',
        'notes': 'Headaches due to tension. Recommended physiotherapy.'
    }

    patient.add_medical_record(record1)
    patient.add_medical_record(record2)

    # print Patient history
    patient_data = Patient.get('patient1')
    if patient_data:
        print(f"Patient History: {patient_data.get_medical_history()}")

    # Create and save Doctor
    doctor = Doctor('doctor1', 'Dr. Alice Johnson', 'General Practitioner', 'organization', 'org1')
    doctor.save()

    # Create and save Organization
    organization = Organization('org1', 'Health Clinic', 'clinic')
    organization.save()
    organization.add_doctor('doctor1')

    # Create and save Interaction
    interaction = Interaction('interaction1', 'doctor1', 'patient1', '2024-07-27', 'Routine check-up.')
    interaction.save()

    interaction_data = Interaction.get('interaction1')
    if interaction_data:
        print(f"Interaction Data: {interaction_data.__dict__}")

    # print doctor interactions within the organization
    interactions = organization.get_doctor_interactions()
    print(f"Doctor Interactions: {interactions}")

    # print patient history for a specific doctor
    patient_histories = organization.get_patient_history_for_doctor('doctor1')
    print(f"Patient Histories for Doctor 'doctor1': {patient_histories}")

# Run test
test_models()