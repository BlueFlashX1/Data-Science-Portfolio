# Matthew Thompson - Data Science Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/matthewqilanthompson/)
[![Email](https://img.shields.io/badge/Contact-Email-D14836?style=for-the-badge&logo=gmail)](mailto:matthewqilanthompson.work@gmail.com)

> **M.S. Data Science** · University of Arizona (May 2026) · B.S. Biology · [See full bio](https://github.com/matthewqilanthompson)

---

**Highlight**: 30-day hospital readmission prediction with a Random Forest classifier, ROC-AUC of 0.90 (a classifier accuracy score where 1.0 is perfect) across 125,958 synthetic electronic health record (EHR) encounters

**Navigation**: [Projects](#featured-projects) • [Skills](#skills) • [Connect](#connect)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-E34F26?style=for-the-badge&logo=r&logoColor=white)

## Featured Projects

Projects span healthcare analytics, machine learning, deep learning, database systems, and statistical visualization. Each shows skills applied to a real data problem, with documented model-selection rationale and outcome interpretation.

### [Healthcare Readmission Prediction Competition](./projects/data-science/foundation-of-data-science/)

**Class competition: 30-day hospital readmission prediction** • _INFO 521 Final Project_

Developed a Random Forest classifier with patient-frequency encoding on 125,958 synthetic electronic health record (EHR) encounters. Compared 9 algorithms with stratified cross-validation and achieved an ROC-AUC of 0.90 (a classifier accuracy score where 1.0 is perfect) on the development set.

**Why Random Forest over the other 8 algorithms**: EHR data is tabular with mixed numeric and categorical features, has missing medication counts, and shows class imbalance, all of which Random Forest handles natively without heavy preprocessing. RF also provides feature-importance rankings (which surfaced the patient-frequency encoding as the strongest predictor) and works as a robust default with minimal tuning. Gradient Boosting could have edged it out with extensive tuning, but Random Forest's stability across cross-validation folds was the deciding factor in a competition setting where overfitting to dev meant penalty on test.

**What I Applied**:

- **Feature engineering**: Engineered a patient-frequency encoding feature that emerged as the strongest readmission predictor
- **Data cleaning**: Removed uninformative features and used mean imputation for missing medication-count data
- **Model comparison**: Evaluated 9 machine-learning algorithms (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, HistGradientBoosting, AdaBoost, ExtraTrees, Bagging, K-Nearest Neighbors) with stratified cross-validation

**Result/Outcome**: An ROC-AUC of 0.90 means the model correctly ranks a high-risk patient above a low-risk one 9 times out of 10. A hospital using this for triage could identify the highest-risk encounters early, supporting targeted intervention to reduce preventable 30-day readmissions.

**Tech**: Python • Scikit-learn • Pandas • Random Forest • Feature Engineering • Stratified Cross-Validation

---

### [Healthcare Analytics with SQL & NoSQL](./projects/database-systems/sql-nosql-databases-info579/)

**Database design and SQL analytics for electronic health record (EHR) data** • _INFO 579 Final Project_

Designed and implemented Third Normal Form (3NF) database schemas to analyze 1,171 patients and 53,346 encounters from Synthea (an open-source synthetic patient data generator). Built 14 analytical SQL reports using multi-table joins, temporal analysis, Common Table Expressions (CTEs), and window functions.

**Why 3NF over a denormalized star schema**: Synthea's EHR data is transactional (frequent encounter inserts, patient updates) where update anomalies matter more than read latency. 8 entity tables + 2 junction tables for many-to-many relationships kept the data consistent while still supporting analytical queries via CTEs and window functions.

**What I Applied**:

- **Clinical Quality Analysis**: Identified viral sinusitis as the most prevalent condition (63%) and tracked emergency 30-day mortality rates
- **Provider Utilization**: Discovered workload imbalances and identified inactive specialties for resource reallocation
- **SQL Techniques**: Implemented CTEs, window functions, and multi-table joins (4+ tables) for temporal analysis
- **Database Design**: Designed normalized schemas (3NF) supporting 1,171 patients and 53,346 encounters

**Result/Outcome**: A working analytical database that translated raw EHR records into 14 actionable reports, the kind of output a clinical-quality team would use to decide staffing, condition prioritization, and resource reallocation.

**Tech**: MySQL • Complex SQL Joins • Temporal Analysis • Database Design • Python

---

### [Multi-Label Emotion Classification with Transformer Fine-Tuning](./projects/deep-learning/emotion-classification-info557/)

**14-label text classification competition** • _INFO 557 Graduate Project_

**Placed 8th/15** on the test set (F1-score 0.672, a balanced precision/recall metric where 1.0 is perfect), up from 10th/18 on dev with the 3rd-tightest dev-to-test generalization gap (-0.05) on the leaderboard. Built a multi-label emotion classifier on a 14-class GoEmotions subset of Reddit text using a 5-seed 1D convolutional neural network (Conv1D / CNN) with calibrated binary cross-entropy (BCE) loss and label smoothing.

**Why Conv1D with kernel 3, then a fine-tuned transformer in the follow-up study**: Reddit emotion text is short and the cues live in bigrams and trigrams (e.g., "fuming about", "irked when"), which Conv1D with kernel size 3 captures cleanly (kernel 3 won the dev sweep over kernels 5 and 7). For the post-grading study, I tested 4 pretrained-embedding variants on the same architecture: the win was fine-tuning a model already strong at language understanding (dev F1 0.65 to 0.83 with RoBERTa). Pretraining alone or model size alone wasn't the lever, letting gradients flow back through the encoder was.

**What I Applied**:

- **Calibration over dev-score chasing**: Chose an untuned 0.5 threshold + BCE label smoothing over focal loss to avoid dev-set leakage from threshold tuning
- **Rare-class diagnosis**: Identified vocabulary-level failure (1-3 occurrences) as the cause of three zero-F1 classes; Easy Data Augmentation (EDA) rescued the "anger" class off zero
- **Evaluation pipeline**: Built a `check.py` re-evaluator that predicted test F1 within 2 points while training logs over-predicted by 5
- **Post-grading study**: Tested 4 variants on the same architecture and showed that end-to-end fine-tuning, not pretraining or scale alone, was the bottleneck-breaker

**Result/Outcome**: The submitted model finished 8th of 15 with the 3rd-tightest dev-to-test generalization gap, validating that calibration-aware training generalizes better than chasing dev-set metrics. The post-grading study identified RoBERTa fine-tuning as the path to ~0.83 dev F1 (a hypothetical top-3 placement), confirming the rare-class problem was a representation issue, not an architecture one.

**Tech**: Python • Keras / TensorFlow • Conv1D CNN • Multi-label F1 • 5-seed ensemble • EDA augmentation • RoBERTa fine-tuning (post-grading study)

---

### [Trait-Based Animal Classification](./projects/data-science/data-mining-final-project/)

**Machine-learning classification of evolutionary traits across 1,087 animal families** • _INFO 523 Final Project_

Built classification models comparing binary trait presence/absence vs. evolutionary origin rates across 1,087 animal families. Applied SHAP (SHapley Additive exPlanations) for model explainability and used balanced metrics to handle class imbalance across 5 superphyla.

**Why Logistic Regression over Random Forest and Decision Trees**: The evolutionary-rate features were continuous and approximately linear with respect to taxonomic class, which Logistic Regression's linear decision boundary fits well. With ~1,087 families and class imbalance across 5 superphyla, Logistic Regression's calibrated probabilities and interpretable per-trait coefficients gave stronger signal than tree-based models, which over-fit on sparse rare-class samples. Random Forest still served a diagnostic role: SHAP showed the binary model collapsing onto a single feature, which is exactly the failure mode tree ensembles exhibit on sparse, imbalanced data.

**What I Applied**:

- **Data representation optimization**: Evolutionary rates provided stronger predictive signal than sparse binary data
- **Model comparison**: Evaluated Logistic Regression, Decision Trees, and Random Forest on both representations
- **Feature importance analysis**: Identified Visual, Competition, and Auditory traits as the strongest predictors via SHAP
- **Imbalanced classification**: Used balanced accuracy and macro F1-score (a balanced precision/recall metric where 1.0 is perfect) instead of standard accuracy

**Result/Outcome**: ~50% accuracy on 5-class taxonomy showed that sexually-selected traits carry real but limited predictive signal for taxonomic classification. The deeper finding: data representation (continuous evolutionary rates vs. sparse binary presence) mattered more than model choice. The method generalizes to any trait dataset where evolutionary rates are available.

**Tech**: Python • Scikit-learn • SHAP • Stratified K-fold cross-validation • Quarto • Jupyter

---

### [Statistical Data Visualization Portfolio](./projects/r-analytics/data-visualization-portfolio/)

**Statistical visualization portfolio across wildlife, safety, and economic domains** • _INFO 526 Portfolio_

Built comprehensive visualizations across three domains using R, ggplot2, and the tidyverse. Developed custom data-transformation functions, implemented advanced plot types (alluvial diagrams, faceted layouts), and established reproducible research workflows.

**Why these chart types**: Chose alluvial diagrams for occupational safety to show cause-to-effect flow (which stacked bar charts can't represent), line graphs for temporal trends in dangerous-job fatality rates (rejecting stacked area plots because they make quantifying exact values difficult), and grouped bar charts over stacked bars when more than ~10 categories made stacks unreadable. Chart selection was driven by the question being asked rather than chart popularity.

**What I Applied**:

- **Cougar Predation Analysis**: Identified wild ungulates as primary prey and analyzed temporal patterns in predation data
- **Occupational Safety**: Mapped fatality trends using alluvial diagrams to visualize cause-to-effect relationships
- **Economic Trends**: Analyzed regional housing-price volatility and recovery patterns across 4 U.S. regions

**Result/Outcome**: Three reproducible visualization analyses across distinct domains. The cause-to-effect insight in the occupational safety alluvial diagram would not have been visible in a standard bar or pie chart, and the chart-selection narrative demonstrates that the choice of visualization is itself an analytical decision.

**Tech**: R • ggplot2 • RMarkdown • dplyr • tidyverse • ggalluvial • Custom Functions

---

### [AI for Healthcare Capstone: Emergency Room Simulator Showcase Poster](./projects/capstone/ai4hc-info698/)

**Team capstone: poster and print pipeline for an emergency room training simulator** • _INFO 698 Graduate Capstone_

Healthcare AI training simulator built by a 6-person team capstone at the University of Arizona AI Core, AI for Healthcare program (AI4HC): a .NET 8 web app with a Retrieval-Augmented Generation (RAG) chat tutor, HeyGen streaming avatar, and multiple-choice quiz generator. My role was the showcase poster and the avatar source footage; team engineers built the app.

**My Contributions**:

- **Showcase poster**: Took Abhiram's initial HTML draft ([isjustabhi/AI4HC](https://github.com/isjustabhi/AI4HC)) and polished it into the team's final capstone poster, adding light + dark theme variants and iterating the layout / CSS. **View live:** [light theme](https://matthewqilanthompson.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_v1.html) · [dark theme](https://matthewqilanthompson.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_dark.html)
- **Print-PDF conversion pipeline**: Wrote a Python script (headless Chrome + img2pdf) that exports the HTML poster to a 4×3 ft print-ready PDF with print-shop metadata. The team printed from this PDF and the physical poster matched the on-screen render exactly.
- **Avatar source footage**: Recorded the 1-minute clip used to build the team's HeyGen avatar; the project coordinator wired the application programming interface (API)

**Result/Outcome**: The poster was physically printed and presented at the University of Arizona iShowcase event. The print pipeline ensured the on-screen render and the 4×3 ft physical poster matched exactly, a deliverable the team could trust without a proofing iteration.

**Tech**: HTML • CSS • Python (headless Chrome to img2pdf print pipeline) • Information design • Technical communication

---

## Skills

| Category             | Tools & Libraries                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Languages**        | Python (machine-learning pipelines, data processing) • R (statistical analysis, visualization) • SQL / Structured Query Language (database queries, analytics) |
| **Machine Learning** | Scikit-learn (model training, evaluation) • Random Forest (classification) • Logistic Regression • SHAP / SHapley Additive exPlanations (model explainability) |
| **Deep Learning**    | Keras / TensorFlow (convolutional neural network / CNN architecture) • Hugging Face Transformers • RoBERTa fine-tuning • Multi-label classification |
| **Data Analysis**    | Pandas (data manipulation, Extract-Transform-Load / ETL) • NumPy (numerical computing) • tidyverse (data transformation) • dplyr (data wrangling) |
| **Visualization**    | ggplot2 (statistical plots) • Matplotlib (data visualization) • ggalluvial (flow diagrams) • viridis (color palettes) |
| **Databases**        | MySQL (relational databases) • Database design (Third Normal Form / 3NF) • Common Table Expressions (CTEs) • Window functions (analytical queries) |
| **Development**      | Git (version control) • Jupyter (interactive analysis) • RMarkdown (reproducible reports) • Quarto (publishing workflows) |

### Domain Expertise

| Domain                   | Skills Applied                                                                                                                                  |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Healthcare Analytics** | Electronic health record (EHR) data processing for 125,958+ encounters • Readmission prediction models (ROC-AUC 0.90) • Clinical quality metrics analysis |
| **Machine Learning**     | Classification algorithms (Random Forest, Logistic Regression) • Model comparison across 9 algorithms • Cross-validation • SHAP explainability  |
| **Deep Learning / NLP**  | Multi-label text classification on 14-class GoEmotions • Fine-tuning transformers (RoBERTa via Hugging Face) • Keras / TensorFlow CNN architecture • Calibration-aware methodology (binary cross-entropy / BCE + label smoothing, -0.050 dev-to-test gap) |
| **Database Systems**     | Schema design (3NF) for 1,171 patients and 53,346 encounters • Multi-table joins (4+ tables) • Temporal analysis with CTEs and window functions |
| **Data Visualization**   | Advanced plots (alluvial diagrams, faceted layouts) • Custom R functions for automated exploratory data analysis (EDA) • Reproducible research workflows with RMarkdown |

---

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matthewqilanthompson/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/matthewqilanthompson)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:matthewqilanthompson.work@gmail.com)
