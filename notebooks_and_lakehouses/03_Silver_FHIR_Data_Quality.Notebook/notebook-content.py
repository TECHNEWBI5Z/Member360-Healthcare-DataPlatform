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

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Record Count Validation**

# CELL ********************

def count_table(table_name):

    count = (
        spark.table(table_name)
        .count()
    )

    print(
        f"{table_name}: {count}"
    )

    return count

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

tables = [
    "bronze_patient",
    "silver_patient",
    "bronze_observation",
    "silver_observation",
    "bronze_condition",
    "silver_condition"
]


for table in tables:
    count_table(table)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Patient Duplicate Check**

# CELL ********************

patient_duplicate = (
    spark.table(
        "silver_patient"
    )
    .groupBy(
        "PatientID"
    )
    .count()
    .filter(
        "count > 1"
    )
)

display(patient_duplicate)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Patient Mandatory Field Check**

# CELL ********************

missing_patient = (
spark.table(
    "silver_patient"
)
.filter(
    """
    PatientID IS NULL
    OR Gender IS NULL
    OR BirthDate IS NULL
    """
)
)

display(missing_patient)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Referential Integrity Check**

# CELL ********************

observation_patient_check = (

spark.table(
    "silver_observation"
)

.alias("obs")

.join(

    spark.table(
        "silver_patient"
    )

    .alias("pat"),

    F.col(
        "obs.PatientID"
    )
    ==
    F.col(
        "pat.PatientID"
    ),

    "left"

)

.filter(

    F.col(
        "pat.PatientID"
    ).isNull()

)

.select(

    "obs.ObservationID",
    "obs.PatientID"

)

)


display(
    observation_patient_check
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Create Data Quality Summary Table**

# CELL ********************

dq_results = [

("silver_patient",
 "Duplicate PatientID",
 "PASS"),

("silver_observation",
 "Invalid Patient Reference",
 "PASS"),

("silver_condition",
 "Invalid Patient Reference",
 "PASS")

]


dq_df = spark.createDataFrame(
    dq_results,
    [
        "TableName",
        "CheckName",
        "Result"
    ]
)


(
dq_df
.write
.format("delta")
.mode("overwrite")
.saveAsTable(
    "silver_data_quality_results"
)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
