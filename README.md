# Matthew Thompson - Data Science Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/matthewqilanthompson/)
[![Email](https://img.shields.io/badge/Contact-Email-D14836?style=for-the-badge&logo=gmail)](mailto:matthewqilanthompson.work@gmail.com)

> **M.S. Data Science** · University of Arizona (May 2026) · B.S. Biology · [See full bio](https://github.com/matthewqilanthompson)

---

**Highlight**: 30-day hospital readmission prediction with a Random Forest classifier on a class competition. ROC AUC 0.901 on the dev-phase leaderboard (5th of 40) and 0.858 on the final held-out test (13th of 35), across 587,801 training and 125,958 dev rows of synthetic electronic health record (EHR) data. ROC AUC is a classifier ranking score where 1.0 is perfect.

**Navigation**: [Projects](#featured-projects) • [Skills](#skills) • [Connect](#connect)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-E34F26?style=for-the-badge&logo=r&logoColor=white)

## Featured Projects

Each project below documents a deliberate model-selection decision and the real-world outcome it produced. Full methodology, code, and reproducibility details live in each project's own README.

### [Healthcare Readmission Prediction Competition](./projects/data-science/foundation-of-data-science/)

**30-day hospital readmission prediction** · _INFO 521 Final Project_

Random Forest classifier with patient-frequency encoding on synthetic electronic health record (EHR) data: 587,801 training encounters and 125,958 dev encounters. Scored ROC AUC 0.901 on the dev-phase leaderboard (5th of 40) and 0.858 on the final held-out test (13th of 35) after comparing 9 algorithms with stratified cross-validation.

**Why Random Forest**: EHR data is tabular with mixed numeric and categorical features, has missing medication counts, and shows class imbalance, all of which Random Forest handles natively. RF also surfaces feature importance (which exposed patient-frequency as the strongest predictor) and proved more stable across cross-validation folds than Gradient Boosting in a competition setting.

**Outcome**: ROC AUC 0.858 on the held-out test means the model correctly ranks a high-risk patient above a low-risk one about 86% of the time. The 5-point drop from the dev leaderboard (0.901) to the test (0.858) was honest generalization: cross-validated AUC (~0.86) predicted the test result almost exactly, so the model held up on unseen data while higher-dev-scoring competitors dropped further.

**Tech**: Python • Scikit-learn • Pandas • Random Forest • Stratified Cross-Validation · [Read the project →](./projects/data-science/foundation-of-data-science/)

---

### [Multi-Label Emotion Classification with Transformer Fine-Tuning](./projects/deep-learning/emotion-classification-info557/)

**14-label text classification competition** · _INFO 557 Graduate Project_

Placed 8th/15 on the test set (F1-score 0.672, a balanced precision/recall metric where 1.0 is perfect) with the 3rd-tightest dev-to-test generalization gap (-0.05) on the leaderboard. Built a 5-seed 1D convolutional neural network (Conv1D / CNN) on a 14-class GoEmotions subset of Reddit text with calibrated binary cross-entropy (BCE) loss and label smoothing.

**Why Conv1D, then RoBERTa fine-tuning in the post-grading study**: Reddit emotion cues live in bigrams and trigrams, which Conv1D with kernel size 3 captures cleanly (kernel 3 won the dev sweep over 5 and 7). The follow-up 4-variant study showed end-to-end fine-tuning of RoBERTa (not pretraining or model size alone) was the lever that pushed dev F1 from 0.65 to 0.83.

**Outcome**: The submitted model finished 8th/15 with the 3rd-tightest dev-to-test gap, validating calibration-aware training over dev-score chasing. The post-grading study identified RoBERTa fine-tuning as a path to ~0.83 dev F1 (a hypothetical top-3 placement), confirming the rare-class problem was a representation issue, not an architecture one.

**Tech**: Python • Keras / TensorFlow • Conv1D CNN • 5-seed ensemble • EDA augmentation • RoBERTa fine-tuning (post-grading study) · [Read the project →](./projects/deep-learning/emotion-classification-info557/)

---

### [Trait-Based Animal Classification](./projects/data-science/data-mining-final-project/)

**Machine-learning classification of evolutionary traits across 1,087 animal families** · _INFO 523 Final Project_

Classification across 5 superphyla comparing binary trait presence/absence vs. continuous evolutionary origin rates. Applied SHAP (SHapley Additive exPlanations) for feature importance and balanced metrics to handle class imbalance.

**Why Logistic Regression over Random Forest and Decision Trees**: Evolutionary-rate features were continuous and approximately linear with respect to taxonomic class, which Logistic Regression's decision boundary fits well. With ~1,087 families and class imbalance across 5 superphyla, Logistic Regression's calibrated probabilities and interpretable per-trait coefficients gave stronger signal than tree-based models, which over-fit on sparse rare-class samples.

**Outcome**: ~50% accuracy on 5-class taxonomy showed that sexually-selected traits carry real but limited predictive signal for taxonomic classification. The deeper finding: data representation (continuous evolutionary rates vs. sparse binary presence) mattered more than model choice. The method generalizes to any trait dataset where evolutionary rates are available.

**Tech**: Python • Scikit-learn • SHAP • Stratified K-fold cross-validation · [Read the project →](./projects/data-science/data-mining-final-project/)

---

## Other Projects

| Project | What it shows | Tech |
|---|---|---|
| [**Healthcare Analytics with SQL**](./projects/database-systems/sql-nosql-databases-info579/) | Third Normal Form (3NF) schema design and 14 analytical SQL reports across 1,171 patients and 53,346 encounters from Synthea synthetic EHR data, covering clinical quality, provider utilization, and readmissions. End-to-end reproducible via Docker. | MySQL · Python · CTEs · window functions |
| [**Data Visualization Portfolio**](./projects/r-analytics/data-visualization-portfolio/) | Wildlife predation, occupational safety, and housing economics analyses with chart-selection rationale (alluvial diagrams, line graphs, grouped bars) | R · ggplot2 · ggalluvial · RMarkdown |
| [**AI4HC Capstone: ER Simulator Showcase Poster**](./projects/capstone/ai4hc-info698/) | Light/dark theme HTML poster and Python print-export pipeline (headless Chrome → 48×36 in PDF) for a 6-person team capstone at the University of Arizona AI Core | HTML · CSS · Python |

---

## Skills

| Category             | Tools & Libraries                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Languages**        | Python (machine-learning pipelines, data processing) • R (statistical analysis, visualization) • SQL / Structured Query Language (database queries, analytics) |
| **Machine Learning** | Scikit-learn (model training, evaluation) • Random Forest (classification) • Logistic Regression • SHAP / SHapley Additive exPlanations (model explainability) |
| **Deep Learning**    | Keras / TensorFlow (neural network architecture) • Hugging Face Transformers • RoBERTa fine-tuning • Convolutional neural networks (CNNs) • Multi-label classification |
| **Data Analysis**    | Pandas (data manipulation, Extract-Transform-Load / ETL) • NumPy (numerical computing) • tidyverse (data transformation) • dplyr (data wrangling) |
| **Visualization**    | ggplot2 (statistical plots) • Matplotlib (data visualization) • ggalluvial (flow diagrams) • viridis (color palettes) |
| **Databases**        | MySQL (relational databases) • Database design (Third Normal Form / 3NF) • Common Table Expressions (CTEs) • Window functions (analytical queries) |
| **Development**      | Git (version control) • Jupyter (interactive analysis) • RMarkdown (reproducible reports) • Quarto (publishing workflows) |

### Domain Experience

| Domain | Where applied |
|---|---|
| **Healthcare Analytics** | Readmission prediction (synthetic electronic health record data, ROC AUC 0.858 on held-out test, 0.901 on dev) and Third Normal Form (3NF) database design (1,171 patients, 53,346 encounters, 14 analytical SQL reports) |
| **Biological / Life-sciences Data** | Trait-based classification across 1,087 animal families (Master's project) and quantitative research at Oklahoma State University (NSF ON-RaMP, grasshopper coloration and behavior) and Maryland Sea Grant (NSF REU, marine microbial abundance) |

---

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matthewqilanthompson/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/matthewqilanthompson)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:matthewqilanthompson.work@gmail.com)
