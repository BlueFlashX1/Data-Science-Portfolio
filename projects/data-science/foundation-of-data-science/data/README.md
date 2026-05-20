# Data — Healthcare Readmission

Synthetic Arizona patient encounter records (Synthea-generated EHR data) used in the INFO 521 class competition to predict 30-day hospital readmission.

## Files

| File | Records | Contents |
|------|---------|----------|
| `train.csv` | 587,801 | Training set — features + target |
| `dev.csv` | 125,958 | Development / validation set — features + target |
| `test.csv` | features only | Held-out test set |
| `submission.csv` | — | Model predictions on the test set |

Full raw dataset as a single `.zip`: [CyVerse download](https://data.cyverse.org/dav-anon/iplant/home/gchism/courses/info511/final_project_health/data.zip)

## Target variable

`readmitted_within_30_days` — binary; whether the patient was readmitted to a hospital within 30 days of an encounter.

## Notable features

- **`patient_id`** — record key; engineered into a patient-frequency count, which became the strongest predictor.
- **Clinical measures** — medication counts, procedure costs, pain scores, patient height; contained substantial missing data (mean-imputed).
- **Symptom flags** — chronic pain, hypertension, diabetes, asthma, depression; constant-valued in this dataset and dropped as uninformative.
- **Zip code** — dropped (not meaningful without distance calculations).

See the [project README](../README.md) for the full feature-engineering rationale and modeling decisions.
