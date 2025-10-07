# Trait-Based Prediction of Animal Taxa

[![Course Project](https://img.shields.io/badge/Course-Final%20Project-blue?style=for-the-badge)](https://github.com)
[![INFO 523](https://img.shields.io/badge/INFO%20523-Data%20Mining%20%26%20ML-red?style=for-the-badge)](https://github.com)
[![Summer 2025](https://img.shields.io/badge/Summer-2025-green?style=for-the-badge)](https://github.com)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

[![Python](https://img.shields.io/badge/Python-3.12.9-blue?style=flat-square&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)](https://jupyter.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.7.1-green?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![SHAP](https://img.shields.io/badge/SHAP-0.48.0-red?style=flat-square)](https://shap.readthedocs.io)
[![Quarto](https://img.shields.io/badge/Quarto-Website-75AADB?style=flat-square&logo=quarto)](https://quarto.org)

> **COURSE FINAL PROJECT**: Machine learning analysis of sexually selected traits for animal taxonomic classification

**Academic Context**: This is a final project for INFO 523 (Data Mining & Machine Learning) at the University of Arizona, Summer 2025. The project demonstrates application of machine learning techniques to biological data for taxonomic classification.

## Project Overview

This project investigates a fundamental question in evolutionary biology: **Can sexually selected traits predict higher-level taxonomic groups, and which traits matter most?**

The analysis compares binary presence/absence data against evolutionary origin rates using multiple machine learning approaches to determine which data type provides better predictive power for animal classification.

### Key Research Questions
- Can machine learning models classify animal taxa based on sexually selected traits?
- Which type of data provides better predictive power: binary presence/absence or evolutionary rates?
- What specific traits are most important for taxonomic classification?

### Methodology

**Data Preparation:**
- Grouped phyla into 5 superphyla to reduce sparsity:
  - Ecdysozoa
  - Lophotrochozoa  
  - Deuterostomia
  - Basal Metazoa & Non-Bilaterians
  - Basal Bilateria

**Machine Learning Models:**
- **Logistic Regression** - Linear classification with regularization
- **Decision Trees** - Interpretable tree-based classification
- **Random Forest** - Ensemble method with feature importance

**Model Evaluation:**
- Balanced accuracy and macro F1 to handle class imbalance
- Cross-validation for robust performance estimation
- SHAP analysis for model explainability

## Key Findings

### Best Performance: Evolutionary Rates + Logistic Regression
- **Binary data**: Poor performance across all models (sparse, Arthropoda-dominated)
- **Evolutionary rates**: Strong predictive signal with balanced feature importance
- **SHAP insights**: Evolutionary models use visual, competition, auditory, and female choice traits effectively

## Dataset Information

### Data Files

| File | Size | Rows | Description |
|------|------|------|-------------|
| [`family_related_data.csv`](./data/family_related_data.csv) | 50KB | 1,087 | Binary presence/absence data for sexually selected traits at family level |
| [`animals_rateof_evolution.csv`](./data/animals_rateof_evolution.csv) | 12KB | 84 | Continuous evolutionary origin rates for traits at phylum level |
| [`data/README.md`](./data/README.md) | 2.5KB | - | Complete data codebook and variable descriptions |

### Data Schema

#### Binary Family Dataset (1,087 families)
**Trait Categories:**
- **Sensory**: Auditory (A), Gustatory (G), Olfactory (O), Tactile (T), Visual (V)
- **Competition**: Male-male (C), Female-female (K), Intersexual conflict (S)
- **Choice**: Female choice (F), Male choice (M)
- **Overall**: Any sexually selected trait (SS)

#### Evolutionary Rates Dataset (84 phylogenetic estimates)
**Same traits as above, but as continuous rates of evolutionary origin**

**Variables in Both Datasets:**
- **Tree_Label / Tree**: Phylogenetic identifier
- **Phylum**: Taxonomic phylum name
- **A**: Auditory traits
- **G**: Gustatory traits
- **O**: Olfactory traits
- **T**: Tactile traits
- **V**: Visual traits
- **C**: Male-male competition
- **F**: Female choice
- **K**: Female-female competition
- **M**: Male choice
- **S**: Intersexual conflict
- **SS**: Overall sexually selected trait presence (binary dataset only)

*Full variable descriptions and data types available in [`data/README.md`](./data/README.md)*

## Quick Start

### Prerequisites
```bash
# Python 3.12+ required
python --version
```

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd data-mining-final-project

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter notebook
jupyter notebook index.ipynb
```

### Dependencies
```
jupyter>=1.0.0          # Notebook environment
numpy>=2.2.4            # Numerical computing
pandas>=2.2.2           # Data manipulation
scikit-learn>=1.7.1     # Machine learning
shap>=0.48.0            # Model explainability
matplotlib>=3.10.1      # Plotting
seaborn>=0.13.2         # Statistical visualization
statsmodels>=0.14.0     # Statistical modeling
```

## Results Summary

### Model Performance
| Model | Data Type | Balanced Accuracy | Macro F1 | Key Insights |
|-------|-----------|-------------------|----------|-------------|
| **Logistic Regression** | **Evolutionary** | **Highest** | **Highest** | Best overall performance |
| Random Forest | Evolutionary | Moderate | Moderate | Good feature importance |
| Decision Tree | Evolutionary | Lower | Lower | Most interpretable |
| All Models | Binary | Poor | Poor | Insufficient signal |

### Feature Importance (SHAP Analysis)
- **Visual traits**: Strongest predictor across superphyla
- **Competition traits**: Important for distinguishing groups
- **Auditory traits**: Significant but secondary importance
- **Female choice**: Consistent moderate importance

## Project Links

- **[Live Website](https://info-523-su25.github.io/final-project-thompson/)** - Interactive project presentation
- **[Main Analysis](./index.ipynb)** - Complete Jupyter notebook with all code and results
- **[Data Documentation](./data/README.md)** - Comprehensive data codebook
- **[Project Proposal](./proposal.qmd)** - Original research questions and methodology
- **[Presentation](./presentation.qmd)** - Key findings and visualizations

## Project Structure

```
.
├── index.ipynb              # Main analysis notebook (1.2MB)
├── _quarto.yml              # Website configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # Datasets and documentation
│   ├── family_related_data.csv      # Binary trait data (50KB)
│   ├── animals_rateof_evolution.csv # Evolutionary rates (12KB)
│   └── README.md                   # Data codebook
├── docs/                   # Generated website
├── about.qmd              # Project information
├── proposal.qmd           # Research proposal
├── presentation.qmd       # Results presentation
├── data.qmd              # Data description
└── citations.qmd         # Bibliography
```

## Technical Details

### Environment
- **Python**: 3.12.9
- **Key Libraries**: scikit-learn 1.7.1, SHAP 0.48.0, pandas 2.2.2
- **Development**: Jupyter notebooks with Quarto publishing

### Analysis Pipeline
1. **Data preprocessing**: Missing value handling, feature encoding
2. **Exploratory analysis**: Distribution analysis, correlation studies
3. **Model training**: Cross-validation with stratified sampling
4. **Evaluation**: Balanced metrics for imbalanced classes
5. **Interpretation**: SHAP values for feature importance

## Academic Information

**Course**: INFO 523 - Data Mining & Machine Learning  
**Term**: Summer 2025  
**Institution**: University of Arizona  
**Project Type**: Final Course Project  
**Acknowledgment**: Methodology derived from data visualization course by Mine Çetinkaya-Rundel @ Duke University

## Future Directions

- **Enhanced data quality**: Address sparsity in binary dataset
- **Advanced modeling**: Deep learning approaches for complex trait interactions
- **Phylogenetic integration**: Incorporate evolutionary relationships directly
- **Broader taxonomy**: Extend beyond current superphyla groupings

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

---

<div align="center">

**[View Interactive Analysis](https://info-523-su25.github.io/final-project-thompson/)**

*A course final project exploring the intersection of evolutionary biology and machine learning*

</div>
