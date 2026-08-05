# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "14c76d8b-f872-4b9f-a22a-d9e10ddc3c14",
# META       "default_lakehouse_name": "HealthcareLakehouse",
# META       "default_lakehouse_workspace_id": "2b558bb6-aefb-4342-a27b-56457f13dfc0",
# META       "known_lakehouses": [
# META         {
# META           "id": "14c76d8b-f872-4b9f-a22a-d9e10ddc3c14"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# **Import Libraries**

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.functions import col, explode, regexp_extract
from datetime import datetime

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Configuration**

# CELL ********************

BRONZE_PREFIX = "bronze_"
SILVER_PREFIX = "silver_"


resources = [
    "patient",
    "encounter",
    "observation",
    "condition",
    "medicationrequest",
    "practitioner",
    "organization",
    "allergyintolerance"
]


print("Resources loaded:")
print(resources)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Helper Function**

# CELL ********************

def transform_patient():

    df = spark.table(
        "bronze_patient"
    )


    result = (
        df
        .withColumn(
            "name",
            explode("name")
        )
        .withColumn(
            "address",
            explode("address")
        )
        .select(

            col("id")
            .alias("PatientID"),

            col("identifier")[0]["value"]
            .alias("MRN"),

            col("name.given")[0]
            .alias("FirstName"),

            col("name.family")
            .alias("LastName"),

            col("gender"),

            col("birthDate"),

            col("address.city")
            .alias("City"),

            col("address.state")
            .alias("State"),

            col("address.country")
            .alias("Country"),

            col("telecom")[0]["value"]
            .alias("Phone")

        )
    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_encounter():

    df = spark.table(
        "bronze_encounter"
    )


    result = (

        df.select(

            col("id")
            .alias("EncounterID"),


            regexp_extract(
                col("subject.reference"),
                "Patient/(.*)",
                1
            )
            .alias("PatientID"),


            col("status"),


            col("class.code")
            .alias("EncounterClass"),


            col("period.start")
            .alias("StartTime"),


            col("period.end")
            .alias("EndTime")

        )

        .withColumn(

            "EncounterDate",

            F.to_date(
                col("StartTime")
            )

        )

        .withColumn(

            "EncounterDateKey",

            F.date_format(
                col("EncounterDate"),
                "yyyyMMdd"
            )
            .cast("int")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_observation():

    df = spark.table(
        "bronze_observation"
    )


    result = (

        df.select(

            col("id")
            .alias("ObservationID"),


            regexp_extract(
                col("subject.reference"),
                "Patient/(.*)",
                1
            )
            .alias("PatientID"),


            col("code.coding")[0]["code"]
            .alias("LOINCCode"),


            col("code.coding")[0]["display"]
            .alias("ObservationName"),


            col("valueQuantity.value")
            .alias("Value"),


            col("valueQuantity.unit")
            .alias("Unit")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_condition():

    df = spark.table(
        "bronze_condition"
    )


    result = (

        df.select(

            col("id")
            .alias("ConditionID"),


            regexp_extract(
                col("subject.reference"),
                "Patient/(.*)",
                1
            )
            .alias("PatientID"),


            col("code.text")
            .alias("Diagnosis"),


            col("clinicalStatus.text")
            .alias("Status")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_medicationrequest():

    df = spark.table(
        "bronze_medicationrequest"
    )


    result = (

        df.select(

            col("id")
            .alias("MedicationRequestID"),


            regexp_extract(
                col("subject.reference"),
                "Patient/(.*)",
                1
            )
            .alias("PatientID"),


            col(
                "medicationCodeableConcept.text"
            )
            .alias("Medication"),


            col("status"),


            col("intent")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_practitioner():

    df = spark.table(
        "bronze_practitioner"
    )


    result = (

        df
        .withColumn(
            "name",
            explode("name")
        )
        .select(

            col("id")
            .alias("PractitionerID"),


            col("name.given")[0]
            .alias("FirstName"),


            col("name.family")
            .alias("LastName")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_organization():

    df = spark.table(
        "bronze_organization"
    )


    result = (

        df
        .withColumn(
            "address",
            explode("address")
        )
        .select(

            col("id")
            .alias("OrganizationID"),


            col("name")
            .alias("OrganizationName"),


            col("address.city")
            .alias("City"),


            col("address.state")
            .alias("State")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def transform_allergyintolerance():

    df = spark.table(
        "bronze_allergyintolerance"
    )


    result = (

        df.select(

            col("id")
            .alias("AllergyID"),


            regexp_extract(
                col("patient.reference"),
                "Patient/(.*)",
                1
            )
            .alias("PatientID"),


            col("code.text")
            .alias("Allergy"),


            col("clinicalStatus.text")
            .alias("Status")

        )

    )


    return result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Execute Dynamically**

# CELL ********************

transformations = {

"patient":
transform_patient,

"encounter":
transform_encounter,

"observation":
transform_observation,

"condition":
transform_condition,

"medicationrequest":
transform_medicationrequest,

"practitioner":
transform_practitioner,

"organization":
transform_organization,

"allergyintolerance":
transform_allergyintolerance

}


def save_silver(df, table_name):

    (
        df
        .withColumn(
            "_silver_load_timestamp",
            F.current_timestamp()
        )
        .write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(table_name)
    )


    print(f"Created {table_name}")
    
for resource, func in transformations.items():

    print(
        f"Processing {resource}"
    )


    silver_df = func()


    save_silver(
        silver_df,
        f"{SILVER_PREFIX}{resource}"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
