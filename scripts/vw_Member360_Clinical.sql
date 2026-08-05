CREATE OR ALTER VIEW vw_Member360_Clinical
AS

WITH EncounterSummary AS
(
    SELECT
        PatientID,

        COUNT(*) AS TotalEncounters,

        MIN(StartTime) AS FirstEncounterDate,

        MAX(StartTime) AS LastEncounterDate

    FROM fact_encounter

    GROUP BY PatientID
),


ConditionSummary AS
(
    SELECT
        PatientID,

        COUNT(*) AS TotalConditions

    FROM fact_condition

    GROUP BY PatientID
),


MedicationSummary AS
(
    SELECT
        PatientID,

        COUNT(*) AS TotalMedications

    FROM fact_medication

    GROUP BY PatientID
),


AllergySummary AS
(
    SELECT
        PatientID,

        COUNT(*) AS TotalAllergies

    FROM fact_allergy

    GROUP BY PatientID
),


ObservationSummary AS
(
    SELECT
        PatientID,


        MAX(
            CASE
                WHEN ObservationName = 'Heart Rate'
                THEN Value
            END
        ) AS LatestHeartRate,


        MAX(
            CASE
                WHEN ObservationName = 'Body Temperature'
                THEN Value
            END
        ) AS LatestTemperature,


        MAX(
            CASE
                WHEN ObservationName = 'Oxygen Saturation'
                THEN Value
            END
        ) AS LatestOxygenSaturation


    FROM fact_observation

    GROUP BY PatientID
)


SELECT

    p.patientKey,

    p.PatientID,

    p.FirstName,

    p.LastName,

    p.gender,

    p.birthDate,


    DATEDIFF(
        YEAR,
        p.birthDate,
        GETDATE()
    ) AS Age,


    p.City,

    p.State,


    -- Encounter Metrics

    ISNULL(
        e.TotalEncounters,
        0
    ) AS TotalEncounters,


    e.FirstEncounterDate,

    e.LastEncounterDate,


    -- Clinical Metrics

    ISNULL(
        c.TotalConditions,
        0
    ) AS TotalConditions,


    ISNULL(
        m.TotalMedications,
        0
    ) AS TotalMedications,


    ISNULL(
        a.TotalAllergies,
        0
    ) AS TotalAllergies,


    -- Latest Vitals

    o.LatestHeartRate,

    o.LatestTemperature,

    o.LatestOxygenSaturation


FROM dim_patient p


LEFT JOIN EncounterSummary e

ON p.PatientID = e.PatientID


LEFT JOIN ConditionSummary c

ON p.PatientID = c.PatientID


LEFT JOIN MedicationSummary m

ON p.PatientID = m.PatientID


LEFT JOIN AllergySummary a

ON p.PatientID = a.PatientID


LEFT JOIN ObservationSummary o

ON p.PatientID = o.PatientID;