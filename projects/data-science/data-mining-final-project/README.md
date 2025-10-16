# Trait-Based Prediction of Animal Taxa

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 523](https://img.shields.io/badge/INFO%20523-Data%20Mining%20%26%20ML-red?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.7.1-green?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![SHAP](https://img.shields.io/badge/SHAP-0.48.0-red?style=flat-square)](https://shap.readthedocs.io)
[![Quarto](https://img.shields.io/badge/Quarto-Website-75AADB?style=flat-square&logo=quarto)](https://quarto.org)

> **Machine learning classification of animal superphyla using sexually selected traits** • University of Arizona, INFO 523 (Summer 2025)

**[🌐 View Live Website](https://info-523-su25.github.io/final-project-thompson/)** | **[📊 Analysis Notebook](./index.ipynb)**

---

## Research Question

**Can sexually selected traits predict higher-level taxonomic groups (superphyla), and which traits matter most?**

Compared binary presence/absence data vs. evolutionary origin rates across 1,087 animal families to determine optimal data representation for taxonomic classification.

## Key Findings

### 🏆 Best Model: Logistic Regression + Evolutionary Rates

| Finding | Detail |
|---------|--------|
| **Data Quality Impact** | Evolutionary rates **dramatically outperformed** binary data (sparse, Arthropoda-dominated) |
| **Top Predictors (SHAP)** | Visual traits > Competition > Auditory > Female choice |
| **Classification Target** | 5 superphyla: Ecdysozoa, Lophotrochozoa, Deuterostomia, Basal Metazoa, Basal Bilateria |
| **Evaluation Strategy** | Balanced accuracy & macro F1 (handles class imbalance) |

### Performance Comparison

| Model | Data Type | Result |
|-------|-----------|--------|
| **Logistic Regression** | **Evolutionary** | ✅ **Best Performance** |
| Random Forest | Evolutionary | ⚠️ Moderate |
| Decision Tree | Evolutionary | ⚠️ Lower but interpretable |
| All Models | Binary | ❌ Poor (insufficient signal) |

## Technical Implementation

### Data Engineering
- **Superphyla grouping**: Reduced sparsity by consolidating 10+ phyla → 5 superphyla
- **Feature comparison**: Binary (10 traits) vs. continuous evolutionary rates (9 traits)
- **Sample sizes**: 1,087 families (binary), 84 phylogenetic estimates (rates)

### Machine Learning Pipeline
1. **Preprocessing**: Missing value handling, feature scaling, label encoding
2. **Cross-validation**: Stratified K-fold for robust performance estimation
3. **Model training**: Logistic Regression, Decision Trees, Random Forest
4. **Explainability**: SHAP values for feature importance and model interpretation
5. **Evaluation**: Balanced accuracy, macro F1 (critical for imbalanced classes)

### Key Technical Skills Demonstrated
- ✅ **Imbalanced classification**: Balanced metrics, stratified sampling
- ✅ **Model explainability**: SHAP analysis for biological insights
- ✅ **Cross-validation**: Proper generalization assessment
- ✅ **Feature engineering**: Domain-driven data transformation (superphyla grouping)
- ✅ **Comparative analysis**: Binary vs. continuous feature evaluation
- ✅ **Reproducible research**: Quarto website with full analysis pipeline

## Dataset

| File | Size | Records | Description |
|------|------|---------|-------------|
| [`family_related_data.csv`](./data/family_related_data.csv) | 50KB | 1,087 families | Binary trait presence/absence |
| [`animals_rateof_evolution.csv`](./data/animals_rateof_evolution.csv) | 12KB | 84 estimates | Evolutionary origin rates |

**Traits**: Auditory (A), Gustatory (G), Olfactory (O), Tactile (T), Visual (V), Male competition (C), Female competition (K), Intersexual conflict (S), Female choice (F), Male choice (M)

*Full data codebook: [`data/README.md`](./data/README.md)*

## Quick Start

```bash
# Clone and install
git clone <repository-url>
cd data-mining-final-project
pip install -r requirements.txt

# Launch analysis
jupyter notebook index.ipynb
```

**Requirements**: Python 3.12+, scikit-learn 1.7.1, SHAP 0.48.0, pandas 2.2.2, matplotlib 3.10.1

## Project Resources

- **[Live Website](https://info-523-su25.github.io/final-project-thompson/)** - Full interactive analysis
- **[Main Analysis](./index.ipynb)** - Jupyter notebook (99 cells, comprehensive)
- **[Proposal](./proposal.qmd)** - Research questions and methodology
- **[Presentation](./presentation.qmd)** - Key findings and visualizations
- **[Data Documentation](./data/README.md)** - Complete codebook

## Project Structure

```
data-mining-final-project/
├── index.ipynb              # Main analysis (99 cells, 1.2MB)
├── _quarto.yml              # Website configuration
├── requirements.txt         # Python dependencies
├── data/
│   ├── family_related_data.csv          # Binary traits (1,087 families)
│   ├── animals_rateof_evolution.csv     # Evolutionary rates (84 estimates)
│   └── README.md                        # Data codebook
├── docs/                    # Generated Quarto website
├── proposal.qmd             # Research proposal (236 lines)
├── presentation.qmd         # Results presentation (795 lines)
└── citations.qmd            # Bibliography
```

## Academic Information

**Course**: INFO 523 - Data Mining & Machine Learning  
**Term**: Summer 2025  
**Institution**: University of Arizona  
**Acknowledgment**: Methodology inspired by Mine Çetinkaya-Rundel @ Duke University

---

**[🌐 View Interactive Analysis](https://info-523-su25.github.io/final-project-thompson/)** | Course final project exploring evolutionary biology through machine learning
