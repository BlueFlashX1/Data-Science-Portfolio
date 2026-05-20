# Matthew Thompson - Data Science Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/matthewqilanthompson/)
[![Email](https://img.shields.io/badge/Contact-Email-D14836?style=for-the-badge&logo=gmail)](mailto:matthewqilanthompson.work@gmail.com)

> **M.S. in Data Science**, University of Arizona (completed May 2026) · B.S. Biology  
> _Seeking entry-level Data Analyst roles — biological, life-sciences, and environmental data_

**Interests**: Biological & life-sciences data • Environmental & ecological analysis • Automation

---

**Highlight**: 30-day hospital readmission prediction — Random Forest classifier, ROC AUC 0.90 across 125,958 synthetic EHR encounters

**Navigation**: [Projects](#academic-projects) • [Skills](#skills) • [Connect](#connect)

## Skills

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-E34F26?style=for-the-badge&logo=r&logoColor=white)

| Category             | Tools & Libraries                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Languages**        | Python (ML pipelines, data processing) • R (statistical analysis, visualization) • SQL (database queries, analytics)                |
| **Machine Learning** | Scikit-learn (model training, evaluation) • Random Forest (classification) • Logistic Regression • SHAP (model explainability)      |
| **Deep Learning**    | Keras / TensorFlow (CNN architecture) • Hugging Face Transformers • RoBERTa fine-tuning • Multi-label classification                 |
| **Data Analysis**    | Pandas (data manipulation, ETL) • NumPy (numerical computing) • tidyverse (data transformation) • dplyr (data wrangling)            |
| **Visualization**    | ggplot2 (statistical plots) • Matplotlib (data visualization) • ggalluvial (flow diagrams) • viridis (color palettes)               |
| **Databases**        | MySQL (relational databases) • Database Design (3NF normalization) • CTEs (complex queries) • Window Functions (analytical queries) |
| **Development**      | Git (version control) • Jupyter (interactive analysis) • RMarkdown (reproducible reports) • Quarto (publishing workflows)           |

### Domain Expertise

| Domain                   | Skills Applied                                                                                                                                  |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Healthcare Analytics** | EHR data processing for 125,958+ encounters • Readmission prediction models (ROC AUC 0.90) • Clinical quality metrics analysis                  |
| **Machine Learning**     | Classification algorithms (Random Forest, Logistic Regression) • Model comparison across 9 algorithms • Cross-validation • SHAP explainability  |
| **Deep Learning / NLP**  | Multi-label text classification on 14-class GoEmotions • Fine-tuning transformers (RoBERTa via Hugging Face) • Keras / TensorFlow CNN architecture • Calibration-aware methodology (BCE + label smoothing, −0.050 dev→test gap) |
| **Database Systems**     | Schema design (3NF) for 1,171 patients and 53,346 encounters • Multi-table joins (4+ tables) • Temporal analysis with CTEs and window functions |
| **Data Visualization**   | Advanced plots (alluvial diagrams, faceted layouts) • Custom R functions for automated EDA • Reproducible research workflows with RMarkdown     |

## Academic Projects

These academic projects demonstrate my data science capabilities across healthcare analytics, machine learning, deep learning, database systems, and statistical visualization. Each project showcases skills I've applied to solve real data problems.

### [Healthcare Analytics with SQL & NoSQL](./projects/database-systems/sql-nosql-databases-info579/)

**Database design and SQL analytics for EHR analysis** • _INFO 579 Final Project_

Designed and implemented normalized database schemas (3NF) to analyze 1,171 patients and 53,346 encounters from Synthea synthetic EHR data. Built 14 analytical reports using complex multi-table joins, temporal analysis, CTEs, and window functions.

**What I Applied**:

- **Clinical Quality Analysis**: Identified viral sinusitis as most prevalent condition (63%) and tracked emergency 30-day mortality rates
- **Provider Utilization**: Discovered workload imbalances and identified inactive specialties for resource reallocation
- **SQL Techniques**: Implemented CTEs, window functions, and complex multi-table joins (4+ tables) for temporal analysis
- **Database Design**: Designed normalized schemas (3NF) supporting 1,171 patients and 53,346 encounters

**Tech**: MySQL • Complex SQL Joins • Temporal Analysis • Database Design • Python

---

### [Trait-Based Animal Classification](./projects/data-science/data-mining-final-project/)

**ML classification project using biological data** • _INFO 523 Final Project_

Built machine learning classification models using real biological data, comparing binary trait presence/absence vs. evolutionary origin rates across 1,087 animal families. Applied SHAP for model explainability and implemented balanced metrics to handle class imbalance.

**What I Applied**:

- **Data representation optimization**: Discovered evolutionary rates provided stronger predictive signal than sparse binary data
- **Model selection**: Evaluated multiple algorithms and determined Logistic Regression outperformed tree-based models for this dataset
- **Feature importance analysis**: Identified Visual, Competition, and Auditory traits as strongest predictors using SHAP analysis
- **Imbalanced classification**: Implemented balanced accuracy and macro F1 metrics to properly evaluate model performance

**Tech**: Python • Scikit-learn • SHAP • Stratified K-fold • Quarto • Jupyter

---

### [Healthcare Readmission Prediction Competition](./projects/data-science/foundation-of-data-science/)

**Class competition for 30-day hospital readmission prediction** • _INFO 521 Final Project_

Developed a Random Forest classifier with patient-frequency encoding on 125,958 synthetic EHR encounters. Compared 9 algorithms with stratified cross-validation and achieved ROC AUC 0.90 on the development set.

**What I Applied**:

- **Feature engineering**: Engineered patient frequency encoding feature that emerged as the strongest readmission predictor
- **Data cleaning**: Removed uninformative features and implemented mean imputation for missing medication count data
- **Model comparison**: Evaluated 9 ML algorithms and selected Random Forest for optimal performance-stability balance

**Tech**: Python • Scikit-learn • Pandas • Random Forest • Feature Engineering • Stratified Cross-Validation

---

### [Statistical Data Visualization Portfolio](./projects/r-analytics/data-visualization-portfolio/)

**Statistical visualization portfolio across wildlife, safety, and economic domains** • _INFO 526 Portfolio_

Built comprehensive visualizations across three domains using R, ggplot2, and tidyverse. Developed custom data transformation functions, implemented advanced plot types (alluvial diagrams, faceted layouts), and established reproducible research workflows.

**What I Applied**:

- **Cougar Predation Analysis**: Identified wild ungulates as primary prey and analyzed temporal patterns in predation data
- **Occupational Safety**: Mapped fatality trends using alluvial diagrams to visualize cause-effect relationships
- **Economic Trends**: Analyzed regional housing price volatility and recovery patterns across 4 U.S. regions

**Tech**: R • ggplot2 • RMarkdown • dplyr • tidyverse • ggalluvial • Custom Functions

---

### [Multi-Label Emotion Classification with Transformer Fine-Tuning](./projects/deep-learning/emotion-classification-info557/)

**14-label text classification competition** • _INFO 557 Graduate Project_

**Placed 8th/15** on test in class competition (F1 0.672), up from 10th/18 on dev with the 3rd-tightest dev→test gap (−0.05) on the leaderboard. Built a multi-label emotion classifier on a 14-class GoEmotions subset of Reddit text using a 5-seed Conv1D CNN with calibrated BCE + label smoothing.

**What I Applied**:

- **Calibration over dev-score chasing**: Chose untuned 0.5 threshold + BCE label smoothing over focal loss to avoid dev-set leakage from threshold tuning
- **Rare-class diagnosis**: Identified vocabulary-level failure as the cause of three zero-F1 classes; EDA-style augmentation rescued anger off zero
- **Honest evaluation pipeline**: Built a `check.py` re-evaluator that predicted test F1 within 2 points while training logs over-predicted by 5
- **Pretrained-embedding comparison (post-grading)**: Tested 4 variants on the same architecture; the win was fine-tuning a model already strong at language understanding (dev F1 0.65 → 0.83 with RoBERTa). Pretraining alone or model size alone wasn't enough.

**Tech**: Python • Keras / TensorFlow • Conv1D CNN • Multi-label F1 • 5-seed ensemble • EDA augmentation • RoBERTa fine-tuning (post-grading study)

---

### [AI4HC Capstone — ER Simulator Showcase Poster](./projects/capstone/ai4hc-info698/)

**Team capstone — ER simulator showcase poster** • _INFO 698 Graduate Capstone_

Healthcare AI training simulator built by a 6-person team capstone at the UofA AI Core: .NET 8 web app with a RAG-backed chat tutor, HeyGen streaming avatar, and a multiple-choice quiz generator. I wasn't on the engineering side; my role was the showcase poster and the avatar source footage.

**My Contributions**:

- **Showcase poster**: Took Abhiram's initial HTML draft ([isjustabhi/AI4HC](https://github.com/isjustabhi/AI4HC)) and polished it into the team's final capstone poster — added light + dark theme variants and iterated the layout/CSS. **View live:** [light theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_v1.html) · [dark theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_dark.html)
- **Print-PDF conversion pipeline**: Wrote a Python script (headless Chrome + img2pdf) that exports the HTML poster to a 4×3 ft print-ready PDF with print-shop metadata. The team printed from this PDF and the physical poster matched the on-screen render exactly.
- **Avatar source footage**: Recorded the 1-minute clip used to build the team's HeyGen avatar; project coordinator wired the API

**Tech**: HTML • CSS • Python (headless Chrome → img2pdf print pipeline) • Information design • Technical communication

---

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matthewqilanthompson/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BlueFlashX1)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:matthewqilanthompson.work@gmail.com)

**Looking for**: Entry-level Data Analyst roles — biological, life-sciences, and environmental data
