# Matthew Thompson - Data Science Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/matthewqilanthompson/)
[![Email](https://img.shields.io/badge/Contact-Email-D14836?style=for-the-badge&logo=gmail)](mailto:matthewqilanthompson.work@gmail.com)

> **Master's Student in Data Science** | University of Arizona  
> _Seeking Data Scientist or Analyst positions in healthcare, biological sciences, or related domains_

**Core Competencies**: `R` `Python` `SQL/NoSQL` `Machine Learning` `Healthcare Analytics` `Data Visualization` `Statistical Computing`

**Specialization**: Computational methods for biological and healthcare challenges • EHR systems • Predictive modeling • Database design • Ecological analysis

---

**Competition Achievement**: **5th place** (dev) / **13th place** (test) in healthcare readmission prediction • 40 & 35 participants respectively • ROC AUC >0.85 both phases

**Navigation**: [Projects](#featured-projects) • [Technical Skills](#skills--technical-stack) • [Connect](#connect)

## Skills & Technical Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-E34F26?style=for-the-badge&logo=r&logoColor=white)

**Languages**: R • Python • SQL/NoSQL • JavaScript • Shell  
**Data Science**: Tidyverse • ggplot2 • Pandas • NumPy • Scikit-learn • SHAP • Quarto  
**Databases**: MySQL • Database Design • Healthcare Analytics • Temporal Analysis  
**Development**: VS Code • Positron • Git/GitHub • RMarkdown • Jupyter • Docker

### Domain Expertise

| **Domain**                    | **Applied Skills & Demonstrated Capabilities**                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Healthcare Analytics**      | EHR data processing (Synthea, 67MB+) • Hospital readmission prediction (ROC AUC >0.85) • Clinical quality metrics • Provider utilization analysis • 30-day mortality tracking  |
| **Machine Learning**          | Competition experience (5th/40 participants) • Model explainability (SHAP) • Imbalanced classification • Hyperparameter tuning • Feature engineering • Cross-validation        |
| **Biological Data Science**   | Taxonomic classification (1,087 families) • Evolutionary trait analysis • Ecological modeling (wildlife predation) • Sparse data handling • Domain-driven feature engineering  |
| **Database Systems**          | Normalized schema design (3NF) • Complex multi-table joins (4+ tables) • CTEs & window functions • Temporal analysis • 14 analytical reports • 53K+ record processing          |
| **Statistical Visualization** | ggplot2 expertise • Advanced plot types (alluvial, faceted) • Custom R functions • Reproducible research (RMarkdown/Quarto) • Multi-domain analysis (ecology/safety/economics) |
| **Data Engineering**          | Data transformation (tidyverse, pandas) • Missing data strategies • Data cleaning & preprocessing • Feature scaling • Large dataset processing (67MB+ EHR, 28MB safety data)   |

## Featured Projects

### [Healthcare Analytics with SQL & NoSQL](./projects/database-systems/sql-nosql-databases-info579/)

**Advanced database design for EHR data analysis** • _INFO 579 Final Project_

Built normalized database schemas (3NF) to analyze 1,171 patients and 53,346 encounters from Synthea synthetic EHR data (67MB across 6 entities). Created 14 analytical reports using complex multi-table joins, temporal analysis, CTEs, and window functions. Addressed 5 business objectives: profitability, clinical quality, provider utilization, readmission reduction, and strategic expansion.

**Key Findings**:

- **Clinical Quality**: Viral sinusitis most prevalent (63%), emergency 30-day mortality (3.57/1,000 encounters)
- **Provider Utilization**: Severe workload imbalance (top provider: 3,000+ encounters vs <2,000 for others), 5 inactive specialties identified
- **Profitability**: High-cost patients up to $1.1M, 1,000+ occurrences for top procedures (medication reconciliation, renal dialysis)
- **Readmissions**: Flagged high-risk ER patients (≥3 visits) for intervention

**Tech**: MySQL • Complex SQL Joins • Temporal Analysis • Database Design • Python • CTEs • Window Functions

---

### [Trait-Based Animal Classification](./projects/data-science/data-mining-final-project/)

**Machine learning for taxonomic prediction using sexually selected traits** • _INFO 523 Final Project_

Classified animal superphyla (5 groups: Ecdysozoa, Lophotrochozoa, Deuterostomia, Basal Metazoa, Basal Bilateria) across 1,087 families using sexually selected traits. Discovered evolutionary rate data dramatically outperformed binary presence/absence data. SHAP analysis identified visual, competition, auditory, and female choice traits as strongest predictors.

**Key Findings**:

- **Best Model**: Logistic regression with evolutionary rates (highest balanced accuracy & macro F1)
- **Data Quality Impact**: Evolutionary rates provided stronger signal than sparse binary data
- **Critical Predictors**: Visual, competition, auditory traits (SHAP analysis)
- **Evaluation Strategy**: Balanced accuracy & macro F1 for handling class imbalance

**Tech**: Python • Scikit-learn • SHAP • Machine Learning • Quarto • Jupyter

---

### [Healthcare Readmission Prediction Competition](./projects/data-science/foundation-of-data-science/)

**ML competition for 30-day hospital readmission risk prediction** • _INFO 521 Final Project_

**Competition Results: 5th place (dev) / 13th place (test)** among 40 and 35 participants respectively. Developed Random Forest classifier (n_estimators=200, class_weight='balanced') with patient frequency encoding from 125,958 synthetic EHR encounters. Compared 9 algorithms, applied stratified cross-validation for robust generalization. Achieved ROC AUC 0.9011 (dev) / 0.8581 (test).

**Key Insights**:

- **Critical Feature**: Patient frequency encoding (encounter count per patient) strongest readmission predictor
- **Data Quality**: Dropped uninformative features (all symptom columns had identical values), handled missing data in medication counts/procedure costs
- **Model Selection**: Random Forest outperformed HistGradientBoosting for balance of performance and stability

**Tech**: Python • Scikit-learn • Pandas • Random Forest • Feature Engineering • Stratified Cross-Validation

---

### [Statistical Data Visualization Portfolio](./projects/r-analytics/data-visualization-portfolio/)

**Ecological and economic analysis with advanced R visualization** • _INFO 526 Portfolio_

Created comprehensive visualizations across three analysis domains using R, ggplot2, and tidyverse. Demonstrated custom data transformation strategies, advanced plot types (alluvial diagrams, faceted layouts), and reproducible research workflow (RMarkdown → PDF). Developed custom `data_dict()` function for automated data exploration.

**Key Findings**:

- **Cougar Predation (2012-2016)**: Wild ungulates primary prey (mule deer, bighorn sheep, pronghorn), domestic animals least common, 2016 showed zero domestic kills, temporal gaps 2012-2015
- **Occupational Safety**: Identified top 5 most dangerous occupations with fatality trends, alluvial diagrams mapped common causes per occupation
- **Housing Price Index**: Midwest/Northeast/South similar trends, West higher volatility, all regions showed 2005 decline → post-2010 recovery

**Tech**: R • ggplot2 • RMarkdown • dplyr • tidyverse • ggalluvial • Custom Functions

---

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matthewqilanthompson/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BlueFlashX1)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:matthewqilanthompson.work@gmail.com)

**Open to**: Data Scientist or Data Analyst positions in healthcare, biological sciences, and related fields
