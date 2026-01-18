# Healthcare Readmission Risk Prediction

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://www.codabench.org/competitions/6813/)
[![INFO 521](https://img.shields.io/badge/INFO%20521-Foundation%20of%20DS-red?style=for-the-badge)](https://arizona.edu)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> **Class competition for predicting 30-day hospital readmissions using synthetic EHR data** — University of Arizona, INFO 521

**[Competition Platform](https://www.codabench.org/competitions/6813/#/results-tab)** (CodaBench - login required)

---

## Competition Results

**Placed 5th/40** in class competition (development phase)

| Phase           | Ranking    | ROC AUC | Participants |
| --------------- | ---------- | ------- | ------------ |
| **Development** | 5th place  | 0.9011  | 40           |
| **Testing**     | 13th place | 0.8581  | 35           |

---

## Project Overview

**Challenge**: Predict 30-day hospital readmissions to improve patient outcomes and reduce healthcare costs

**Best Model**: Random Forest (n_estimators=200, class_weight='balanced')  
**Dataset**: Synthetic Arizona patient records (Synthea-generated, 125,958 encounters)

Hospital readmissions cost the U.S. healthcare system billions annually. This project demonstrates building a predictive model to support clinical decision-making for targeted interventions.

---

## What I Applied

### Feature Engineering

| Decision                       | Reasoning                                                               |
| ------------------------------ | ----------------------------------------------------------------------- |
| **Patient frequency encoding** | Transformed patient_id into encounter count per patient — key predictor |
| **Dropped zip code**           | Not meaningful without distance calculation                             |
| **Dropped symptom columns**    | All values were identical (0) — uninformative                           |
| **Mean imputation**            | Large sample size made mean imputation appropriate                      |

### Data Quality Challenges

- **Missing data**: Identified and handled significant gaps in medication counts, procedure costs, pain scores, patient height
- **Uninformative features**: Removed symptom columns (chronic pain, hypertension, diabetes, asthma, depression) with identical values

### Model Comparison

Evaluated 9 algorithms: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, HistGradientBoosting, AdaBoost, ExtraTrees, Bagging, KNeighbors

**Random Forest** provided the best balance of performance and stability for this dataset.

---

## Skills Applied

**Machine Learning Pipeline**

1. Data preprocessing: Missing value imputation, feature encoding
2. Feature engineering: Patient frequency encoding, dropped non-predictive columns
3. Model training: Random Forest with stratified cross-validation
4. Hyperparameter tuning: n_estimators, max_depth, min_samples_split
5. Evaluation: ROC AUC optimization, imbalanced classification handling

**Concepts Applied**

- Stratified cross-validation for robust evaluation
- Handling class imbalance with class_weight='balanced'
- Feature engineering to create meaningful predictors
- Avoiding data leakage in competition settings

---

## Project Structure

```text
foundation-of-data-science/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── final_project_process.ipynb         # Main analysis notebook (1,272 lines)
├── ds.py                               # Core data science utilities (4.8KB)
├── train_predict.py                    # Model training pipeline (6.7KB)
├── data/
│   ├── train.csv                       # Training dataset (587,801 records)
│   ├── dev(real_one).csv               # Development/validation set (125,958 records)
│   ├── test.csv                        # Test dataset (features only)
│   ├── submission.csv                  # Final predictions
│   └── README.md                       # Data documentation
├── scoring_program/                    # Competition evaluation scripts
└── scoring_program_dev/                # Development scoring tools
```

---

## Quick Start

```bash
# Clone the portfolio repository
git clone https://github.com/BlueFlashX1/Data-Science-Portfolio.git
cd Data-Science-Portfolio/projects/data-science/foundation-of-data-science

# Install dependencies
pip install -r requirements.txt

# Run exploratory analysis
jupyter notebook final_project_process.ipynb

# Train model and generate predictions
python train_predict.py
```

**Requirements**: Python 3.9+, scikit-learn, pandas, numpy, matplotlib, seaborn

---

## Academic Information

**Course**: INFO 521 - Foundation of Data Science  
**Term**: 2024-2025  
**Institution**: University of Arizona  
**Competition**: CodaBench Healthcare Equity Explorer

---

<p align="center">
  <em>University of Arizona — Graduate Student Data Science Portfolio</em>
</p>
