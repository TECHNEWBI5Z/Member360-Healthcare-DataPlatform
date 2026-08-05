# Member360 Healthcare Data Platform

An end-to-end healthcare analytics platform built using **Microsoft Fabric**, **PySpark**, **Delta Lake**, and **HL7 FHIR** standards.

The project demonstrates how FHIR-based clinical data can be ingested, transformed using a Medallion Architecture (Bronze → Silver → Gold), modeled into a healthcare star schema, and exposed through a **Member360** analytical view for reporting and analytics.

---

# Project Overview

Healthcare organizations generate data across multiple clinical systems in the form of HL7 FHIR resources. Although FHIR provides interoperability, analytics often requires transforming these operational resources into a dimensional model optimized for reporting.

This project simulates a real-world healthcare data engineering solution by:

- Generating synthetic HL7 FHIR resources
- Loading FHIR NDJSON files into Microsoft Fabric Lakehouse
- Building a Medallion Architecture
- Implementing data quality validation
- Creating ETL audit logging
- Designing a Healthcare Star Schema
- Creating a Member360 analytical SQL View

---

# Business Problem

Healthcare data is typically distributed across many FHIR resources:

- Patient
- Encounter
- Observation
- Condition
- MedicationRequest
- Organization
- Practitioner
- AllergyIntolerance

Answering business questions such as:

- How many encounters has a patient had?
- What are the patient's current conditions?
- What medications are prescribed?
- What allergies are documented?
- When was the patient's last visit?

requires joining multiple clinical resources.

The objective of this project is to consolidate these resources into a **Member360 analytical model**.

---

# Solution Architecture

```
                 Python
           FHIR Data Generator
                     │
                     ▼
             FHIR NDJSON Files
                     │
                     ▼
          Microsoft Fabric OneLake
             (Lakehouse Files)
                     │
                     ▼
              Bronze Layer
          Raw FHIR Delta Tables
                     │
                     ▼
              Silver Layer
      FHIR Transformations & Validation
                     │
                     ▼
               Gold Layer
        Healthcare Star Schema
                     │
                     ▼
          SQL Analytics Endpoint
             Member360 SQL View

```

---

# Technologies Used

## Cloud Platform

- Microsoft Fabric
- OneLake
- Fabric Lakehouse
- Fabric SQL Analytics Endpoint

## Data Engineering

- PySpark
- Spark SQL
- Delta Lake
- Medallion Architecture

## Healthcare Standards

- HL7 FHIR R4
- NDJSON
- JSON

## Languages

- Python
- SQL

---

# Project Structure

```
Member360-Healthcare-Data-Platform
│
├── data
│   └── ndjson
│       ├── Patient.ndjson
│       ├── Encounter.ndjson
│       ├── Observation.ndjson
│       ├── Condition.ndjson
│       ├── MedicationRequest.ndjson
│       ├── Practitioner.ndjson
│       ├── Organization.ndjson
│       └── AllergyIntolerance.ndjson
│
├── scripts
│   └── generate_fhir_data.py
│
├── notebooks_and_lakehouses
│   ├── 01_Bronze_FHIR_Ingestion
│   ├── 02_Silver_FHIR_Transformations
│   ├── 03_Data_Quality_Framework
│   ├── 04_Gold_Healthcare_Analytics_Model
│   └── 05_Member360_SQL_View
│
├── diagrams
│
└── README.md
```

---

# Implemented FHIR Resources

| Resource | Description |
|----------|-------------|
| Patient | Patient demographics |
| Encounter | Patient visits |
| Observation | Clinical observations and vitals |
| Condition | Diagnoses |
| MedicationRequest | Prescribed medications |
| Practitioner | Healthcare providers |
| Organization | Hospitals and clinics |
| AllergyIntolerance | Patient allergies |

---

# Medallion Architecture

## Bronze Layer

Stores raw FHIR resources without transformation.

Tables

- bronze_patient
- bronze_encounter
- bronze_observation
- bronze_condition
- bronze_medicationrequest
- bronze_practitioner
- bronze_organization
- bronze_allergyintolerance

---

## Silver Layer

Transforms raw FHIR JSON into structured analytical tables.

Implemented transformations include:

- JSON parsing
- Nested field extraction
- Patient reference extraction
- Clinical attribute normalization
- Data validation
- Null handling

Tables

- silver_patient
- silver_encounter
- silver_observation
- silver_condition
- silver_medicationrequest
- silver_practitioner
- silver_organization
- silver_allergyintolerance

---

## Gold Layer

Healthcare dimensional model.

### Dimension Tables

- dim_patient
- dim_provider
- dim_organization
- dim_date

### Fact Tables

- fact_encounter
- fact_observation
- fact_condition
- fact_medication
- fact_allergy

Relationships are implemented using surrogate keys to support analytical reporting.

---

# Member360 SQL View

The project creates a Member360 analytical view using the Fabric SQL Analytics Endpoint.

Example:

```
vw_Member360_Clinical
```

The view combines:

- Patient demographics
- Healthcare utilization
- Encounter history
- Clinical conditions
- Medication summary
- Allergy summary
- Observation metrics

This provides a single longitudinal analytical view of each patient.

---

# Data Quality Framework

Implemented automated validation checks including:

- Missing Patient IDs
- Null value detection
- Record count validation
- Duplicate checks
- Transformation validation

Results are stored in:

```
silver_data_quality_results
```

---

# ETL Audit Framework

An audit framework tracks every pipeline execution.

Audit information includes:

- Table Name
- Processing Layer
- Start Time
- End Time
- Duration
- Record Count
- Status
- Error Message

Audit Table

```
etl_audit_log
```

---

# Data Flow

```
FHIR Resources
      │
      ▼
NDJSON Files
      │
      ▼
Fabric Lakehouse Files
      │
      ▼
Bronze Tables
      │
      ▼
Silver Transformations
      │
      ▼
Healthcare Star Schema
      │
      ▼
Member360 SQL View
      │
      ▼
Semantic Model
      │
      ▼
ER Diagram
```

---

# Key Features

- End-to-End Healthcare Data Engineering Pipeline
- HL7 FHIR Resource Processing
- Microsoft Fabric Lakehouse
- PySpark Transformations
- Medallion Architecture
- Delta Lake Storage
- Healthcare Star Schema
- Dynamic Gold Layer Framework
- Data Quality Framework
- ETL Audit Logging
- SQL Analytics Views
- Member360 Healthcare Analytics

---

# Sample Analytics

The platform can answer questions such as:

- Total encounters per patient
- Latest patient encounter
- Total clinical observations
- Total diagnosed conditions
- Medication summary
- Allergy summary
- Population demographics
- Healthcare utilization trends

---

# Learning Outcomes

This project demonstrates practical experience with:

- Microsoft Fabric
- Fabric Lakehouse
- Fabric SQL Endpoint
- PySpark
- Spark SQL
- Delta Lake
- Healthcare Data Engineering
- HL7 FHIR
- Medallion Architecture
- Data Modeling
- Healthcare Star Schema Design
- SQL View Development
- Data Quality Validation
- ETL Audit Logging

---

# Future Enhancements

Potential future improvements include:

- Integration with Azure Health Data Services (AHDS)
- Real-time FHIR ingestion
- Incremental loading using MERGE
- Slowly Changing Dimensions (SCD Type 2)
- Patient Risk Scoring
- Readmission Analytics
- Population Health Dashboards
- Power BI Executive Dashboard
- Clinical KPI Dashboard
- Healthcare Cost Analytics
- Predictive Analytics using Machine Learning

---

# Author

**Mahammed Faizan**

Data Engineer

Specializing in:

- Microsoft Fabric
- Azure Data Engineering
- PySpark
- Delta Lake
- Healthcare Analytics
- Data Warehousing

---

## If you found this project helpful

⭐ Star this repository if you found it useful.

Contributions, feedback, and suggestions are always welcome.
