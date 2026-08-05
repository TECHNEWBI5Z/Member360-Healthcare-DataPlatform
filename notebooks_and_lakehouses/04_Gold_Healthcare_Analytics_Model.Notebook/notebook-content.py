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
from pyspark.sql.functions import col
from pyspark.sql.types import *
from datetime import datetime
import uuid

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Defining Audit Schema**

# CELL ********************

audit_schema = StructType([

    StructField(
        "RunID",
        StringType(),
        False
    ),

    StructField(
        "TableName",
        StringType(),
        False
    ),

    StructField(
        "Layer",
        StringType(),
        False
    ),

    StructField(
        "StartTime",
        TimestampType(),
        False
    ),

    StructField(
        "EndTime",
        TimestampType(),
        False
    ),

    StructField(
        "RecordCount",
        LongType(),
        True
    ),

    StructField(
        "Status",
        StringType(),
        False
    ),

    StructField(
        "ErrorMessage",
        StringType(),
        True
    )

])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Create Date Dimension**

# CELL ********************

# from datetime import datetime, timedelta


# start_date = datetime(2020,1,1)
# end_date = datetime(2030,12,31)


# dates=[]

# current=start_date


# while current <= end_date:

#     dates.append(
#         (
#             int(current.strftime("%Y%m%d")),
#             current.date(),
#             current.year,
#             current.month,
#             f"Q{((current.month-1)//3)+1}"
#         )
#     )

#     current += timedelta(days=1)



# date_df = spark.createDataFrame(
#     dates,
#     [
#         "DateKey",
#         "Date",
#         "Year",
#         "Month",
#         "Quarter"
#     ]
# )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# (
# date_df
# .write
# .format("delta")
# .mode("overwrite")
# .saveAsTable(
#     "dim_date"
# )
# )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **create dimentional and fact table**

# CELL ********************

gold_config = {


"dim_patient":

{
    "source":
    "silver_patient",

    "columns":
    [
        "PatientID",
        "MRN",
        "FirstName",
        "LastName",
        "gender",
        "birthDate",
        "City",
        "State",
        "Country",
        "Phone"
    ]
},



"dim_provider":

{
    "source":
    "silver_practitioner",

    "columns":
    [
        "PractitionerID",
        "FirstName",
        "LastName"
    ]
},

"fact_allergy":
{
    "source":
    "silver_allergyintolerance",

    "columns":
    [
        "AllergyID",
        "PatientID",
        "Allergy",
        "Status"
    ]
},


"dim_organization":

{
    "source":
    "silver_organization",

    "columns":
    [
        "OrganizationID",
        "OrganizationName",
        "City",
        "State"
    ]
},



"fact_encounter":

{
    "source":
    "silver_encounter",

    "columns":
    [
        "EncounterID",
        "PatientID",
        "status",
        "EncounterClass",
        "StartTime",
        "EndTime",
        "EncounterDateKey"
    ]
},



"fact_observation":

{
    "source":
    "silver_observation",

    "columns":
    [
        "ObservationID",
        "PatientID",
        "LOINCCode",
        "ObservationName",
        "Value",
        "Unit"
    ]
},



"fact_condition":

{
    "source":
    "silver_condition",

    "columns":
    [
        "ConditionID",
        "PatientID",
        "Diagnosis",
        "Status"
    ]
},



"fact_medication":

{
    "source":
    "silver_medicationrequest",

    "columns":
    [
        "MedicationRequestID",
        "PatientID",
        "Medication",
        "status",
        "intent"
    ]
}

}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **crerate Relationship**

# CELL ********************

relationships = {

    "fact_encounter":
    {

        "dimensions":

        [

            {
                "dimension_table":
                "dim_patient",

                "fact_column":
                "PatientID",

                "dimension_column":
                "PatientID",

                "surrogate_key":
                "PatientKey"
            },


            {
                "dimension_table":
                "dim_date",

                "fact_column":
                "EncounterDateKey",

                "dimension_column":
                "DateKey",

                "surrogate_key":
                "DateKey"
            }

        ]

    },


    "fact_observation":
    {
        "dimension_table":
        "dim_patient",

        "fact_column":
        "PatientID",

        "dimension_column":
        "PatientID",

        "surrogate_key":
        "PatientKey"
    },


    "fact_condition":
    {
        "dimension_table":
        "dim_patient",

        "fact_column":
        "PatientID",

        "dimension_column":
        "PatientID",

        "surrogate_key":
        "PatientKey"
    },


    "fact_medication":
    {
        "dimension_table":
        "dim_patient",

        "fact_column":
        "PatientID",

        "dimension_column":
        "PatientID",

        "surrogate_key":
        "PatientKey"
    },

    "fact_allergy":
    {
        "dimension_table":
        "dim_patient",

        "fact_column":
        "PatientID",

        "dimension_column":
        "PatientID",

        "surrogate_key":
        "PatientKey"
    }

}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Generic Gold Table Creator**

# CELL ********************

def write_audit_log(
    table_name,
    layer,
    start_time,
    end_time,
    record_count,
    status,
    error_message=None
):


    audit_record = [

        (
            str(uuid.uuid4()),

            table_name,

            layer,

            start_time,

            end_time,

            record_count,

            status,

            error_message

        )

    ]


    audit_df = spark.createDataFrame(
        audit_record,
        audit_schema
    )


    (
    audit_df
    .write
    .format("delta")
    .mode("append")
    .saveAsTable(
        "etl_audit_log"
    )
    )


    print(
        f"Audit logged: {table_name}"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from datetime import datetime


def create_gold_table(
        table_name,
        source_table,
        columns):


    start_time = datetime.now()


    print(
        f"Creating {table_name}"
    )


    try:


        # ---------------------------------
        # Read Source Table
        # ---------------------------------

        df = (
            spark.table(source_table)
            .select(
                [
                    col(c)
                    for c in columns
                ]
            )
        )



        # ---------------------------------
        # Dimension Tables
        # ---------------------------------

        if table_name.startswith("dim_"):


            surrogate_key = (
                table_name
                .replace(
                    "dim_",
                    ""
                )
                .title()
                +
                "Key"
            )


            df = (
                df
                .withColumn(

                    surrogate_key,

                    F.monotonically_increasing_id()

                )
            )



        # ---------------------------------
        # Fact Tables
        # ---------------------------------

        elif table_name.startswith("fact_"):


            table_relation = relationships.get(
                table_name,
                {}
            )


            dimensions = table_relation.get(
                "dimensions",
                []
            )


            # -----------------------------
            # Join All Dimensions
            # -----------------------------

            for relation in dimensions:


                dim_table = relation["dimension_table"]


                print(
                    f"Joining {dim_table}"
                )


                dim_df = spark.table(
                    dim_table
                )


                surrogate_column = (
                    relation["surrogate_key"]
                )


                df = (

                    df.alias("fact")

                    .join(

                        dim_df.alias("dim"),

                        col(
                            "fact."
                            +
                            relation["fact_column"]
                        )
                        ==
                        col(
                            "dim."
                            +
                            relation["dimension_column"]
                        ),

                        "left"

                    )

                    .select(

                        "fact.*",

                        col(
                            "dim."
                            +
                            surrogate_column
                        )
                        .alias(
                            surrogate_column
                        )

                    )

                )



            # Fact surrogate key

            fact_key = (
                table_name
                .replace(
                    "fact_",
                    ""
                )
                .title()
                +
                "Key"
            )


            df = (
                df
                .withColumn(

                    fact_key,

                    F.monotonically_increasing_id()

                )
            )



        # ---------------------------------
        # Write Gold Delta Table
        # ---------------------------------

        (
            df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(
                table_name
            )
        )



        # ---------------------------------
        # Audit Success
        # ---------------------------------

        record_count = df.count()


        end_time = datetime.now()


        write_audit_log(

            table_name=table_name,

            layer="Gold",

            start_time=start_time,

            end_time=end_time,

            record_count=record_count,

            status="SUCCESS"

        )


        print(
            f"{table_name} created successfully"
        )



    except Exception as e:


        end_time=datetime.now()


        write_audit_log(

            table_name=table_name,

            layer="Gold",

            start_time=start_time,

            end_time=end_time,

            record_count=0,

            status="FAILED",

            error_message=str(e)

        )


        print(
            f"Failed creating {table_name}"
        )


        raise e

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Execute Dynamically**

# CELL ********************

for table_name, metadata in gold_config.items():


    create_gold_table(

        table_name,

        metadata["source"],

        metadata["columns"]

    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
