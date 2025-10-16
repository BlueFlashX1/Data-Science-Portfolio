# Healthcare Readmission Risk Prediction

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 521](https://img.shields.io/badge/INFO%20521-Foundation%20of%20DS-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data-yellow?style=flat-square&logo=pandas)](https://pandas.pydata.org)

> **Machine learning competition for predicting 30-day hospital readmissions using synthetic EHR data** • University of Arizona, INFO 521 (2024-2025)

**[Competition Platform](https://www.codabench.org/competitions/6813/#/results-tab)** (CodaBench - login required)

---

## Competition Results

### Final Placement: 5th → 13th Place

| Phase           | Ranking        | ROC AUC | Participants | Percentile |
| --------------- | -------------- | ------- | ------------ | ---------- |
| **Development** | **5th place**  | 0.9011  | 40           | Top 12.5%  |
| **Testing**     | **13th place** | 0.8581  | 35           | Top 37%    |

**Achievement**: Demonstrated robust model generalization with clinically meaningful predictive accuracy (ROC AUC > 0.85 on both phases)

## Project Overview

**Challenge**: Predict 30-day hospital readmissions to improve patient outcomes and reduce healthcare costs

**Dataset**: Synthetic Arizona patient records (Synthea-generated, 125,958 encounters) containing demographics, medical conditions, medications, procedures, and insurance data

**Impact**: Hospital readmissions cost the U.S. healthcare system billions annually - this model supports clinical decision-making for targeted interventions and resource allocation

## Key Insights

### Data Quality Challenges
- **Missing data**: Significant missing values in medication counts, procedure costs, pain scores, and patient height
- **Uninformative features**: All symptom columns (chronic pain, hypertension, diabetes, asthma, depression) had identical values (0) - dropped from analysis
- **Data leakage prevention**: Careful feature engineering to avoid using future information

### Critical Feature Engineering Decisions
- **Patient frequency encoding**: Transformed patient_id into count of encounters per patient (key predictor - patients with multiple encounters had higher readmission risk)
- **Dropped features**: zip code (not meaningful without distance calculation), encounter_id (unique identifiers), redundant symptom flags
- **Imputation strategy**: Mean imputation for numeric features due to large sample size

### Model Selection Process
- **9 algorithms compared**: LogisticRegression, DecisionTree, RandomForest, ExtraTrees, GradientBoosting, HistGradientBoosting, AdaBoost, Bagging, KNeighbors
- **Top 3 performers**: HistGradientBoosting (highest ROC AUC), RandomForest (close second, lower variance), GradientBoosting
- **Final choice**: Random Forest for balance of performance and simplicity

## Technical Implementation

### Machine Learning Pipeline

1. **Data Preprocessing**: Missing value imputation, feature encoding, temporal feature extraction
2. **Feature Engineering**: Patient frequency encoding, clinical risk features, dropped non-predictive columns
3. **Model Training**: Random Forest classifier with stratified cross-validation (compared 9 algorithms)
4. **Optimization**: Hyperparameter tuning for ROC AUC maximization
5. **Evaluation**: Imbalanced classification handling, model calibration

### Key Technical Skills

- **Healthcare Data Processing**: Synthetic EHR data with multiple entity relationships
- **Imbalanced Classification**: Binary prediction with ROC AUC optimization
- **Feature Engineering**: Domain-specific clinical features (patient frequency encoding)
- **Cross-validation**: Stratified sampling for robust performance estimation
- **Competition Strategy**: Model optimization across development and test phases

## Project Structure

```text
foundation-of-data-science/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── final_project_process.ipynb         # Main analysis notebook (EDA, preprocessing, modeling)
├── ds.py                              # Core data science utilities
├── train_predict.py                   # Model training and prediction pipeline
├── data/
│   ├── train.csv                      # Training dataset
│   ├── dev(real_one).csv             # Development/validation set
│   ├── test.csv                      # Test dataset (features only)
│   └── submission.csv                # Final predictions
├── scoring_program/                   # Competition evaluation scripts
└── scoring_program_dev/               # Development scoring tools
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run exploratory analysis
jupyter notebook final_project_process.ipynb

# Train model and generate predictions
python train_predict.py
```

**Requirements**: Python 3.9+, scikit-learn, pandas, numpy, matplotlib, seaborn

## Learning Outcomes

This project demonstrated the complete machine learning workflow from raw data to competition submission:

- **Data exploration**: Identifying missing values, uninformative features, and data quality issues
- **Feature engineering**: Critical importance of encoding strategies (frequency encoding > aggregation for preserving information)
- **Model comparison**: Systematic evaluation of multiple algorithms to find optimal balance of performance and interpretability
- **Avoiding pitfalls**: Preventing data leakage, managing class imbalance, and validating generalization with cross-validation
- **Competition strategy**: Optimizing for specific metrics (ROC AUC) while maintaining model robustness across evaluation phases

## Academic Information

**Course**: INFO 521 - Foundation of Data Science  
**Term**: 2024-2025  
**Institution**: University of Arizona, School of Information  
**Competition**: CodaBench Healthcare Equity Explorer
