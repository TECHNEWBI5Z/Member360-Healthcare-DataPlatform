import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import os


fake = Faker()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "ndjson"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# -----------------------------
# Utility Functions
# -----------------------------

def save_ndjson(resource_name, records):

    file_path = os.path.join(
        OUTPUT_DIR,
        f"{resource_name}.ndjson"
    )

    with open(file_path, "w") as f:
        for record in records:
            f.write(
                json.dumps(record)
                + "\n"
            )

    print(
        f"Created {file_path} : {len(records)} records"
    )



# -----------------------------
# Patient Resource
# -----------------------------

def create_patients(count=100):

    patients=[]

    for i in range(count):

        patient_id = str(uuid.uuid4())

        patient = {

            "resourceType":"Patient",

            "id":patient_id,

            "identifier":[
                {
                    "system":
                    "https://hospital.demo/patient",
                    "value":
                    f"MRN-{10000+i}"
                }
            ],

            "name":[
                {
                    "use":"official",
                    "family":
                    fake.last_name(),

                    "given":[
                        fake.first_name()
                    ]
                }
            ],

            "gender":
                random.choice(
                    [
                    "male",
                    "female"
                    ]
                ),

            "birthDate":
                fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=90
                ).isoformat(),

            "address":[
                {
                    "city":
                    fake.city(),

                    "state":
                    fake.state(),

                    "country":
                    "USA"
                }
            ],

            "telecom":[
                {
                    "system":"phone",
                    "value":
                    fake.phone_number()
                }
            ]
        }


        patients.append(patient)


    return patients



# -----------------------------
# Encounter Resource
# -----------------------------

def create_encounters(patients):

    encounters=[]


    for patient in patients:


        encounter = {

            "resourceType":
            "Encounter",

            "id":
            str(uuid.uuid4()),


            "subject":
            {
                "reference":
                f"Patient/{patient['id']}"
            },


            "status":
            "finished",


            "class":
            {
                "code":
                random.choice(
                    [
                    "AMB",
                    "EMER",
                    "IMP"
                    ]
                )
            },


            "period":
            {
                "start":
                fake.date_time_this_year()
                .isoformat(),

                "end":
                datetime.now()
                .isoformat()
            }

        }


        encounters.append(encounter)


    return encounters



# -----------------------------
# Observation Resource
# -----------------------------

def create_observations(patients):

    observations=[]


    codes=[
        ("Heart Rate","8867-4"),
        ("Body Temperature","8310-5"),
        ("Blood Pressure","85354-9"),
        ("Oxygen Saturation","2708-6")
    ]


    for patient in patients:


        for _ in range(3):

            name,code=random.choice(codes)


            observation={

                "resourceType":
                "Observation",

                "id":
                str(uuid.uuid4()),


                "status":
                "final",


                "code":
                {
                    "coding":
                    [
                        {
                        "system":
                        "http://loinc.org",

                        "code":
                        code,

                        "display":
                        name
                        }
                    ]
                },


                "subject":
                {
                    "reference":
                    f"Patient/{patient['id']}"
                },


                "valueQuantity":
                {
                    "value":
                    random.randint(
                        60,
                        120
                    ),

                    "unit":
                    "bpm"
                }

            }


            observations.append(
                observation
            )


    return observations



# -----------------------------
# Condition Resource
# -----------------------------

def create_conditions(patients):

    conditions=[]


    diseases=[
        "Diabetes",
        "Hypertension",
        "Asthma",
        "COVID-19",
        "Heart Disease"
    ]


    for patient in patients:


        condition={

            "resourceType":
            "Condition",

            "id":
            str(uuid.uuid4()),


            "subject":
            {
                "reference":
                f"Patient/{patient['id']}"
            },


            "code":
            {
                "text":
                random.choice(diseases)
            },


            "clinicalStatus":
            {
                "text":
                "active"
            }

        }


        conditions.append(condition)


    return conditions

# -----------------------------
# Organization Resource
# -----------------------------

def create_organizations(count=5):

    organizations=[]


    for i in range(count):

        organization={

            "resourceType":
            "Organization",

            "id":
            str(uuid.uuid4()),


            "name":
            fake.company(),


            "type":[
                {
                    "text":
                    "Hospital"
                }
            ],


            "address":[
                {
                    "city":
                    fake.city(),

                    "state":
                    fake.state(),

                    "country":
                    "USA"
                }
            ]

        }


        organizations.append(
            organization
        )


    return organizations

# -----------------------------
# Practitioner Resource
# -----------------------------

def create_practitioners(count=20):

    practitioners=[]


    specialties=[
        "Cardiology",
        "Neurology",
        "Oncology",
        "General Medicine"
    ]


    for i in range(count):

        practitioner={


            "resourceType":
            "Practitioner",


            "id":
            str(uuid.uuid4()),


            "name":[
                {
                    "family":
                    fake.last_name(),

                    "given":
                    [
                        fake.first_name()
                    ]
                }
            ],


            "qualification":[

                {
                "code":
                {
                    "text":
                    random.choice(
                        specialties
                    )
                }
                }

            ]

        }


        practitioners.append(
            practitioner
        )


    return practitioners

# -----------------------------
# MedicatioRequest Resource
# -----------------------------

def create_medications(patients):

    medications=[]


    drugs=[
        "Metformin",
        "Lisinopril",
        "Aspirin",
        "Atorvastatin"
    ]


    for patient in patients:


        medication={


            "resourceType":
            "MedicationRequest",


            "id":
            str(uuid.uuid4()),


            "status":
            "active",


            "intent":
            "order",


            "subject":
            {
                "reference":
                f"Patient/{patient['id']}"
            },


            "medicationCodeableConcept":
            {
                "text":
                random.choice(drugs)
            }

        }


        medications.append(
            medication
        )


    return medications

def create_allergies(patients):

    allergies=[]


    allergy_list=[
        "Penicillin",
        "Peanuts",
        "Latex",
        "Sulfa drugs"
    ]

# -----------------------------
# Allergy Resource
# -----------------------------

    for patient in patients:


        allergy={


            "resourceType":
            "AllergyIntolerance",


            "id":
            str(uuid.uuid4()),


            "patient":
            {
                "reference":
                f"Patient/{patient['id']}"
            },


            "code":
            {
                "text":
                random.choice(allergy_list)
            },


            "clinicalStatus":
            {
                "text":
                "active"
            }

        }


        allergies.append(
            allergy
        )


    return allergies
# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":


    patients = create_patients(100)


    organizations = create_organizations()


    practitioners = create_practitioners()


    encounters = create_encounters(
        patients
    )


    observations = create_observations(
        patients
    )


    conditions = create_conditions(
        patients
    )


    medications = create_medications(
        patients
    )


    allergies = create_allergies(
        patients
    )


    save_ndjson(
        "Patient",
        patients
    )


    save_ndjson(
        "Organization",
        organizations
    )


    save_ndjson(
        "Practitioner",
        practitioners
    )


    save_ndjson(
        "Encounter",
        encounters
    )


    save_ndjson(
        "Observation",
        observations
    )


    save_ndjson(
        "Condition",
        conditions
    )


    save_ndjson(
        "MedicationRequest",
        medications
    )


    save_ndjson(
        "AllergyIntolerance",
        allergies
    )


    print(
        "Complete FHIR Dataset Generated"
    )