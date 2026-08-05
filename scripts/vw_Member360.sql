CREATE OR ALTER VIEW vw_Member360
AS

SELECT

    p.patientKey,
    p.PatientID,
    p.FirstName,
    p.LastName,
    p.gender,
    p.birthDate,
    p.City,
    p.State,
    p.Country,

    COALESCE(e.TotalEncounters,0)      AS TotalEncounters,
    e.LastEncounter,

    COALESCE(o.TotalObservations,0)    AS TotalObservations,

    COALESCE(c.TotalConditions,0)      AS TotalConditions,

    COALESCE(m.TotalMedications,0)     AS TotalMedications,

    COALESCE(a.TotalAllergies,0)       AS TotalAllergies

FROM dim_patient p

LEFT JOIN
(
    SELECT

        PatientKey,

        COUNT(*) AS TotalEncounters,

        MAX(StartTime) AS LastEncounter

    FROM fact_encounter

    GROUP BY PatientKey

) e

ON p.patientKey = e.PatientKey


LEFT JOIN
(
    SELECT

        PatientID,

        COUNT(*) AS TotalObservations

    FROM fact_observation

    GROUP BY PatientID

) o

ON p.PatientID = o.PatientID


LEFT JOIN
(
    SELECT

        PatientID,

        COUNT(*) AS TotalConditions

    FROM fact_condition

    GROUP BY PatientID

) c

ON p.PatientID = c.PatientID


LEFT JOIN
(
    SELECT

        PatientID,

        COUNT(*) AS TotalMedications

    FROM fact_medication

    GROUP BY PatientID

) m

ON p.PatientID = m.PatientID


LEFT JOIN
(
    SELECT

        PatientID,

        COUNT(*) AS TotalAllergies

    FROM fact_allergy

    GROUP BY PatientID

) a

ON p.PatientID = a.PatientID;