# Trait-Based Prediction of Animal Taxa

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://info-523-su25.github.io/final-project-thompson/)
[![INFO 523](https://img.shields.io/badge/INFO%20523-Data%20Mining-red?style=for-the-badge)](https://datamineaz.org/)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF6B6B?style=flat-square)
![Quarto](https://img.shields.io/badge/Quarto-Website-75AADB?style=flat-square&logo=quarto&logoColor=white)

> **Course project exploring whether sexually selected traits can predict animal taxonomy** — University of Arizona, INFO 523

**[View Live Website](https://info-523-su25.github.io/final-project-thompson/)** | **[Analysis Notebook](./index.ipynb)**

---

## Research Question

**Can sexually selected traits predict higher-level taxonomic groups (superphyla), and which traits matter most?**

This project compared binary presence/absence data vs. evolutionary origin rates across 1,087 animal families to determine which data representation works best for taxonomic classification.

---

## Results Preview

### SHAP Feature Importance (Evolutionary Rates Model)

<p align="center">
  <img src="./images/Plots/SHAP_evolution.png" alt="SHAP values showing Visual and Competition traits as top predictors" width="700">
</p>

_Visual (V), Competition (C), and Auditory (A) traits had the strongest predictive power for classifying superphyla._

### Trait Distribution Across Phyla

<p align="center">
  <img src="./images/Plots/phylum_distribution.png" alt="Distribution of families across phyla" width="700">
</p>

---

## What I Learned

This was a course project where I practiced machine learning classification on real biological data. Here's what I found:

| Finding                              | Detail                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Evolutionary rates > Binary data** | Continuous origin rates provided a stronger signal than sparse binary presence/absence data |
| **Modest accuracy (~50%)**           | The classification task was challenging due to data sparsity and class imbalance            |
| **Key predictors**                   | Visual, Competition, and Auditory traits (identified via SHAP analysis)                     |
| **Class imbalance matters**          | Used balanced accuracy and macro F1 instead of regular accuracy                             |

### Models Tested

| Model                   | Data Type          | Result                     |
| ----------------------- | ------------------ | -------------------------- |
| **Logistic Regression** | Evolutionary rates | Best performance           |
| Random Forest           | Evolutionary rates | Lower accuracy             |
| Decision Tree           | Evolutionary rates | Lower but interpretable    |
| All models              | Binary data        | Poor (insufficient signal) |

---

## Technical Skills Practiced

**Machine Learning Pipeline**

1. Preprocessing: Missing value handling, feature scaling, label encoding
2. Cross-validation: Stratified K-fold for handling class imbalance
3. Model training: Logistic Regression, Decision Trees, Random Forest
4. Explainability: SHAP values for feature importance interpretation
5. Evaluation: Balanced accuracy and macro F1 (critical for imbalanced classes)

**Concepts Applied**

- Imbalanced classification with balanced metrics
- Model explainability with SHAP
- Domain-driven feature engineering (grouping phyla into superphyla)
- Reproducible research with Quarto

---

## Dataset

| File                                                                  | Records        | Description                   |
| --------------------------------------------------------------------- | -------------- | ----------------------------- |
| [`family_related_data.csv`](./data/family_related_data.csv)           | 1,087 families | Binary trait presence/absence |
| [`animals_rateof_evolution.csv`](./data/animals_rateof_evolution.csv) | 84 estimates   | Evolutionary origin rates     |

**Traits analyzed**: Auditory (A), Gustatory (G), Olfactory (O), Tactile (T), Visual (V), Male competition (C), Female competition (K), Intersexual conflict (S), Female choice (F), Male choice (M)

**Classification target**: 5 superphyla — Ecdysozoa, Lophotrochozoa, Deuterostomia, Basal Metazoa, Basal Bilateria

Full codebook: [`data/README.md`](./data/README.md)

---

## Quick Start

```bash
# Clone the portfolio repository
git clone https://github.com/BlueFlashX1/portfolio.git
cd portfolio/projects/data-science/data-mining-final-project

# Install dependencies
pip install -r requirements.txt

# Open the analysis notebook
jupyter notebook index.ipynb
```

**Requirements**: Python 3.12+, scikit-learn, shap, pandas, numpy, matplotlib, seaborn

---

## Project Structure

```
data-mining-final-project/
├── README.md                 # This file
├── index.ipynb               # Main analysis notebook (99 cells)
├── requirements.txt          # Python dependencies
├── _quarto.yml               # Website configuration
├── data/
│   ├── family_related_data.csv       # Binary traits (1,087 families)
│   ├── animals_rateof_evolution.csv  # Evolutionary rates (84 estimates)
│   └── README.md                     # Data codebook
├── images/
│   └── Plots/                # Generated visualizations
│       ├── SHAP_evolution.png
│       ├── SHAP_family.png
│       └── ...
├── docs/                     # Generated Quarto website (don't edit)
├── proposal.qmd              # Research proposal
├── presentation.qmd          # Results presentation
└── citations.qmd             # Bibliography
```

---

## Project Resources

| Resource                                                                | Description                                 |
| ----------------------------------------------------------------------- | ------------------------------------------- |
| [Live Website](https://info-523-su25.github.io/final-project-thompson/) | Full interactive analysis and presentation  |
| [Analysis Notebook](./index.ipynb)                                      | Jupyter notebook with all code (99 cells)   |
| [Proposal](./proposal.qmd)                                              | Original research questions and methodology |
| [Presentation](./presentation.qmd)                                      | Key findings and visualizations             |
| [Data Codebook](./data/README.md)                                       | Complete variable descriptions              |

---

## Academic Information

**Course**: INFO 523 - Data Mining & Machine Learning  
**Term**: Summer 2025  
**Institution**: University of Arizona  
**Acknowledgment**: Project template inspired by Mine Çetinkaya-Rundel @ Duke University

---

<p align="center">
  <a href="https://info-523-su25.github.io/final-project-thompson/">View the Full Interactive Analysis</a>
</p>
