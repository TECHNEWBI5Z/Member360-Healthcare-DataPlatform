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

# ##### **Create Bronze table on files received via Local API push**

# MARKDOWN ********************

# **Import Libraries**

# CELL ********************

from pyspark.sql import functions as F

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Read and Create the tables for Individual resources present in Files section**

# CELL ********************

resources = [
    "Patient",
    "Encounter",
    "Observation",
    "Condition",
    "MedicationRequest",
    "Practitioner",
    "Organization",
    "AllergyIntolerance"
]


for resource in resources:

    path = f"Files/bronze/fhir/{resource}.ndjson"

    table_name = (
        "bronze_"
        + resource.lower()
    )


    df = spark.read.json(path)


    (
        df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(table_name)
    )


    print(
        f"{table_name} created"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
