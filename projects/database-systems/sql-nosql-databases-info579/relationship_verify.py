import pandas as pd

# Load the CSV files (adjust paths as needed)
conditions = pd.read_csv("conditions.csv")
procedures = pd.read_csv("procedures.csv")

#Patient ⇄ Condition 
#how many unique conditions each patient has
unique_conditions_per_patient = conditions.groupby("PATIENT")["CODE"].nunique()

#how many patients are linked to each condition
patients_per_condition = conditions.groupby("CODE")["PATIENT"].nunique()

#Patient ⇄ Procedure
# unique procedures for each patient
unique_procedures_per_patient = procedures.groupby("PATIENT")["CODE"].nunique()

#how many patients are linked to each procedure
patients_per_procedure = procedures.groupby("CODE")["PATIENT"].nunique()

#Summary
print("Patient ⇄ Condition")
print(f"Total unique patients: {unique_conditions_per_patient.shape[0]}")
print(f"Patients with >1 condition: {(unique_conditions_per_patient > 1).sum()}")
print(f"Total unique condition codes: {patients_per_condition.shape[0]}")
print(f"Conditions assigned to >1 patient: {(patients_per_condition > 1).sum()}")

print("\nPatient ⇄ Procedure")
print(f"Total unique patients: {unique_procedures_per_patient.shape[0]}")
print(f"Patients with >1 procedure: {(unique_procedures_per_patient > 1).sum()}")
print(f"Total unique procedure codes: {patients_per_procedure.shape[0]}")
print(f"Procedures assigned to >1 patient: {(patients_per_procedure > 1).sum()}")
