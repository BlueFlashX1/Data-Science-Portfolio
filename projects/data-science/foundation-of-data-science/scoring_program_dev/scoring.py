import os
import sys
sys.path.append(
    os.path.abspath('/Users/matthewthompson/Documents/Academics/DS Masters Academics/Foundation of Data Science/Final Project/final-project-BlueFlashX1/venv/lib/python3.13/site-packages/')
)

import pandas as pd
from sklearn.metrics import roc_auc_score

input_dir = sys.argv[1]       # usually /app/input
output_dir = sys.argv[2]      # usually /app/output

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
log_path = os.path.join(output_dir, "stdout.txt")

def log(msg):
    with open(log_path, "a") as f:
        f.write(f"{msg}\n")

log("Scoring started.")
log(f"Searching {input_dir} recursively for dev.csv and submission.csv...")

# Search the entire input directory for both files
reference_file = None
submission_file = None

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower() == "dev.csv":
            reference_file = os.path.join(root, file)
            log(f"Found dev.csv at: {reference_file}")
        if file.lower() == "submission.csv":
            submission_file = os.path.join(root, file)
            log(f"Found submission.csv at: {submission_file}")
    if reference_file and submission_file:
        break

try:
    assert reference_file is not None, "Reference file not found."
    assert submission_file is not None, "Submission file not found."

    y_true = pd.read_csv(reference_file)["readmitted_within_30_days"]
    y_pred_df = pd.read_csv(submission_file)
    log("Loaded ground truth and predictions.")

    assert "readmitted_within_30_days" in y_pred_df.columns, "Missing 'readmitted_within_30_days' column in submission"

    y_pred = pd.to_numeric(y_pred_df["readmitted_within_30_days"], errors="coerce").fillna(0)

    roc_auc = roc_auc_score(y_true, y_pred)
    log(f"ROC AUC: {roc_auc:.4f}")
    status = "success"

except Exception as e:
    roc_auc = 0.0
    status = f"ERROR: {str(e)}"
    log(status)

# Always write scores.txt
with open(os.path.join(output_dir, "scores.txt"), "w") as f:
    f.write(f"roc_auc: {roc_auc:.4f}\n")

log("Wrote scores.txt")
log(f"Final status: {status}")
