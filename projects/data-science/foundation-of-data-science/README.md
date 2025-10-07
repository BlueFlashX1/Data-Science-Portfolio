# Foundation of Data Science - Final Project

**Course:** INFO 521 - Foundation of Data Science  
**Institution:** University of Arizona, School of Information  
**Student:** Matthew Thompson  
**Academic Year:** 2024-2025  
**Project Type:** Final Course Project

## Course Overview

This course provided comprehensive foundations in data science methodology, covering:

- **Data Science Fundamentals:** Scientific method applied to data analysis
- **Python Programming:** NumPy, Pandas, and core data manipulation libraries
- **Statistical Analysis:** Descriptive and inferential statistics
- **Machine Learning:** Supervised learning algorithms and model evaluation
- **Data Visualization:** Creating effective visualizations for data exploration
- **Project Workflow:** End-to-end data science project methodology

## Healthcare Readmission Risk Prediction

### Project Overview
This project tackles a critical healthcare challenge: **predicting 30-day hospital readmissions to improve patient outcomes and reduce healthcare costs**. Using machine learning techniques on synthetic electronic health records, the project demonstrates end-to-end data science methodology in a healthcare context.

**Project Type:** Final Course Project (INFO 521 - Foundation of Data Science)  
**Competition Platform:** [CodaBench - Healthcare Equity Explorer](https://www.codabench.org/competitions/6813/#/results-tab) (login required)

### Practical Application
Hospital readmissions are a major concern in healthcare, costing the U.S. healthcare system billions annually. This project addresses:

- **Clinical Decision Support:** Early identification of high-risk patients for targeted interventions
- **Resource Allocation:** Optimizing discharge planning and follow-up care scheduling
- **Healthcare Equity:** Exploring disparities in readmission patterns across patient populations
- **Quality Improvement:** Supporting value-based care initiatives and quality metrics

### Technical Implementation

**Dataset:** Synthetic Arizona patient records (generated via Synthea) containing:
- Patient demographics and socioeconomic factors
- Medical conditions, diagnoses, and comorbidities
- Medication histories and treatment protocols
- Medical procedures and interventions
- Insurance and payer information

**Target:** Binary classification - readmission within 30 days (0/1)
**Evaluation:** ROC AUC metric optimized for imbalanced healthcare data

**Machine Learning Pipeline:**
1. **Data Preprocessing:** Missing value imputation, feature encoding, temporal feature extraction
2. **Feature Engineering:** Clinical risk scores, medication complexity indices, comorbidity measures
3. **Model Selection:** Ensemble methods with cross-validation for robust performance
4. **Performance Optimization:** Hyperparameter tuning and model calibration for healthcare applications

### Competition Performance

**Development Phase Results:**
- **Ranking:** 5th place out of 40 participants (Top 12.5%)
- **ROC AUC Score:** 0.9011
- **Achievement:** Strong model performance with excellent discrimination capability

**Final Testing Results:**
- **Final Ranking:** 13th place out of 35 participants (Top 37%)
- **ROC AUC Score:** 0.8581
- **Outcome:** Robust model generalization with clinically meaningful predictive accuracy

### Key Insights & Impact

**Model Performance:**
- Achieved ROC AUC > 0.85 indicating strong predictive capability for clinical decision-making
- Demonstrated model stability across development and testing phases
- Successfully handled complex healthcare data with multiple entity relationships

**Technical Learnings:**
- Mastered healthcare data preprocessing challenges (missing values, temporal features)
- Implemented feature engineering techniques specific to clinical prediction tasks
- Applied rigorous cross-validation strategies for reliable performance estimation
- Gained experience with imbalanced classification in healthcare contexts

**Healthcare Domain Expertise:**
- Understanding of readmission risk factors and clinical workflows
- Experience with synthetic healthcare data generation and validation
- Appreciation for healthcare data privacy and ethical considerations
- Knowledge of healthcare quality metrics and value-based care initiatives

### Key Components

#### 1. Data Analysis & Exploration (`final_project_process.ipynb`)
- Comprehensive exploratory data analysis (EDA)
- Data preprocessing and feature engineering
- Statistical analysis and visualization
- Jupyter notebook documenting the complete analytical process

#### 2. Model Implementation (`ds.py`, `train_predict.py`)
- Implementation of machine learning algorithms
- Model training and hyperparameter tuning
- Cross-validation and performance evaluation
- Production-ready prediction pipeline

#### 3. Competition Framework
- **Live Platform:** CodaBench competition with public leaderboard
- **Scoring System:** Automated evaluation using custom metrics
- **Data Split:** Training, development, and test sets
- **Submission Format:** CSV predictions for real-time leaderboard ranking
- **Peer Competition:** Direct comparison with other data science students

### Project Structure

```
foundation-of-data-science/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── final_project_process.ipynb         # Main analysis notebook
├── ds.py                              # Core data science functions
├── train_predict.py                   # Model training and prediction
├── data/                              # Dataset files
│   ├── train.csv                      # Training dataset
│   ├── dev(real_one).csv             # Development/validation set
│   ├── test.csv                      # Test dataset (features only)
│   ├── submission.csv                # Final predictions
│   └── README.md                     # Data documentation
├── scoring_program/                   # Competition evaluation
│   ├── scoring.py                    # Scoring algorithms
│   └── metadata.yaml                # Competition metadata
└── scoring_program_dev/               # Development scoring
```

## Technical Implementation

### Programming Languages & Libraries
- **Python 3.9+**
- **Core Libraries:** NumPy, Pandas, Scikit-learn
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** XGBoost, Random Forest, Linear Models
- **Development:** Jupyter Notebooks, pytest for testing

### Machine Learning Approach
1. **Data Preprocessing**
   - Missing value imputation
   - Feature scaling and normalization
   - Categorical variable encoding

2. **Feature Engineering**
   - Domain-specific feature creation
   - Feature selection techniques
   - Dimensionality reduction where appropriate

3. **Model Selection**
   - Multiple algorithm comparison
   - Ensemble methods implementation
   - Hyperparameter optimization using grid search

4. **Evaluation & Validation**
   - Cross-validation strategies
   - Performance metrics appropriate to problem type
   - Model interpretation and explainability

## Key Files Description

### Core Analysis Files
- **`final_project_process.ipynb`**: Complete data science workflow from data exploration to final model
- **`ds.py`**: Reusable data science functions and utilities
- **`train_predict.py`**: Production model training and prediction pipeline

### Data Files
- **`data/train.csv`**: Training dataset with features and target variables
- **`data/dev(real_one).csv`**: Development set for model validation
- **`data/test.csv`**: Final test set for competition predictions
- **`data/submission.csv`**: Final model predictions in competition format

### Competition Infrastructure
- **`scoring_program/`**: Official competition scoring system
- **`scoring_program_dev/`**: Development version for local testing
- **`requirements.txt`**: All Python dependencies for reproducibility

## Learning Outcomes Demonstrated

### Technical Skills
- **Data Manipulation:** Advanced Pandas operations for data cleaning and transformation
- **Statistical Analysis:** Application of statistical methods for data understanding
- **Machine Learning:** Implementation of supervised learning algorithms
- **Code Organization:** Modular, well-documented, and testable Python code
- **Version Control:** Proper project structure and documentation practices

### Analytical Skills
- **Problem Formulation:** Converting business problems into data science tasks
- **Feature Engineering:** Creating meaningful predictors from raw data
- **Model Evaluation:** Comprehensive assessment of model performance
- **Communication:** Clear documentation and explanation of methodology

### Best Practices
- **Reproducible Research:** Clear documentation and dependency management
- **Code Quality:** PEP 8 compliance, proper function documentation
- **Testing:** Unit tests for critical functions
- **Ethics:** Consideration of model bias and fairness

## Results & Achievements

### Competition Performance
- **Development Phase:** 5th place out of 40 participants (ROC AUC: 0.9011)
- **Testing Phase:** 13th place out of 35 participants (ROC AUC: 0.8581)
- **Overall Performance:** Consistently placed in top third of competition
- **Live Competition Results:** [View on CodaBench](https://www.codabench.org/competitions/6813/#/results-tab) (login required)

### Technical Achievements
- **Machine Learning Mastery:** Successfully implemented end-to-end ML pipeline for healthcare prediction
- **Model Performance:** Achieved strong ROC AUC scores (>0.85) on both development and test phases
- **Healthcare Analytics:** Applied ML to synthetic EHR data for readmission prediction
- **Competition Strategy:** Demonstrated ability to optimize models for different evaluation phases
- **Code Quality:** Clean, well-documented, production-ready codebase
- **Academic Excellence:** Successfully completed course with strong performance

## How to Run This Project

### Prerequisites
```bash
# Install required Python packages
pip install -r requirements.txt
```

### Exploratory Analysis
```bash
# Launch Jupyter notebook for data exploration
jupyter notebook final_project_process.ipynb
```

### Model Training & Prediction
```bash
# Train model and generate predictions
python train_predict.py

# Or use the modular approach
python -c "from ds import *; # Run specific functions"
```

### Testing
```bash
# Run any custom tests you create
python -m pytest test_*.py
```

## Future Enhancements

- **Advanced Models:** Deep learning approaches for improved performance
- **Feature Engineering:** Additional domain-specific feature creation
- **Hyperparameter Optimization:** Automated tuning using Bayesian optimization
- **Model Interpretation:** SHAP values and feature importance analysis
- **Production Deployment:** API wrapper for real-time predictions

## Related Projects

- **[Data Mining Final Project](../data-mining-final-project/):** Advanced ML techniques and ensemble methods
- **[R Analytics Portfolio](../../r-analytics/):** Statistical analysis and visualization in R
- **[Database Projects](../../database-systems/):** Data engineering and management

## Academic Integrity Statement

This project was completed as part of the Foundation of Data Science course requirements. All code and analysis represent original work, with appropriate citations for any external resources or methodologies used. The project demonstrates mastery of course learning objectives and data science best practices.

---

---

<div align="center">

**Advanced machine learning project demonstrating healthcare analytics and competitive data science skills**

*Applied data science methodology to real-world healthcare prediction challenges*

</div>
