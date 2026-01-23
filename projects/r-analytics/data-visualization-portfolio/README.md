# Data Visualization Portfolio

[![Course Project](https://img.shields.io/badge/Course-Final%20Portfolio-blue?style=for-the-badge)](./MatthewThompson_Final_Portfolio.pdf)
[![INFO 526](https://img.shields.io/badge/INFO%20526-Data%20Visualization-red?style=for-the-badge)](https://arizona.edu)
[![R](https://img.shields.io/badge/R-4.x-276DC3?style=for-the-badge&logo=r)](https://r-project.org)
[![RMarkdown](https://img.shields.io/badge/RMarkdown-Portfolio-FF6B35?style=for-the-badge&logo=r)](https://rmarkdown.rstudio.com)

> **Course portfolio demonstrating R programming and ggplot2 across ecological, safety, and economic datasets** — University of Arizona, INFO 526

**[View Complete Portfolio (PDF)](./MatthewThompson_Final_Portfolio.pdf)** | **[Source Code (.Rmd)](<./Final%20Portfolio%20Assignment(Finished).Rmd>)**

---

## Project Overview

I built comprehensive visualizations for INFO 526 using R, ggplot2, and tidyverse. I analyzed wildlife predation patterns, workplace safety trends, and housing market dynamics, implementing data transformation, categorical grouping, and multi-plot layouts.

---

## Skills Applied

**Languages & Libraries**: R 4.x • RMarkdown • ggplot2 • tidyverse (dplyr, tidyr) • lubridate  
**Specialized Packages**: ggalluvial (alluvial diagrams) • viridis (color palettes)  
**Visualization Types**: Pie charts • Grouped bar charts • Line plots • Alluvial diagrams • Faceted area plots  
**Techniques**: Data transformation • Categorical grouping • Custom color palettes • Temporal analysis

---

## Visualizations & What I Applied

### 1. Cougar Predation Ecology

**Dataset**: 168KB cougar killsite data with prey species and temporal information  
**Visualizations**: Pie chart (prey distribution) • Grouped bar chart (temporal trends)

I developed a grouping strategy for prey species into 4 ecological categories (Wild Ungulates, Small Animals, Domestic Animals, Carnivores) to avoid overlapping classifications.

**Findings**:

- Wild ungulates (mule deer, bighorn sheep, pronghorn) are primary prey
- Domestic animals represent least common prey category
- Temporal patterns show data gaps between 2012-2015
- Year 2016: No domestic animal kills recorded

**What I applied**: Custom grouping strategies • Categorical data transformation with dplyr • Color palette design

---

### 2. Occupational Safety Analysis

**Dataset**: 28MB comprehensive workplace fatality data (146K+ records)  
**Visualizations**: Line graph (temporal trends) • Alluvial diagram (cause-effect relationships)

I identified why stacked plots can be problematic for quantifying values and implemented line graphs for clearer temporal trends. I built alluvial diagrams to effectively visualize cause-effect relationships.

**Findings**:

- Identified most dangerous occupations with fatality trends over time
- Alluvial diagram reveals common causes of fatalities for each occupation
- Line plots show clearer temporal trends than proportional stream graphs

**What I applied**: Advanced plot types (alluvial diagrams with ggalluvial) • Temporal trend visualization

---

### 3. Housing Price Index Trends

**Dataset**: 61KB housing market data across 4 U.S. regions  
**Visualizations**: Faceted area plots (trend comparison) • Statistical summary tables

**Findings**:

- Midwest, Northeast, and South show similar HPI trends
- West region shows higher volatility
- All regions show HPI increase until ~2005, decline, then recovery after 2010

**What I applied**: Faceted visualizations with small multiples • Area plots for trend analysis • Regional comparisons

---

## Technical Implementation

### Reproducible Research Workflow

- **RMarkdown to PDF**: Created complete code documentation with rendered output
- **Custom Functions**: Developed `data_dict()` function for automated data exploration (variable info, descriptive stats, missing values)
- **Data Transformation**: Performed complex categorical grouping, handled missing values, and processed temporal data

---

## Project Files

| File                                                                                             | Size  | Description                                         |
| ------------------------------------------------------------------------------------------------ | ----- | --------------------------------------------------- |
| [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf)                   | 399KB | Complete rendered portfolio with all visualizations |
| [`Final Portfolio Assignment(Finished).Rmd`](<./Final%20Portfolio%20Assignment(Finished).Rmd>)   | 43KB  | Reproducible source code (991 lines)                |
| [`Data Dictionary Function.R`](<./Data Dictionary Function.R>)                                 | 3.7KB | Custom data exploration function                    |
| [`data/Cougar Killsites.xlsx`](<./data/Cougar Killsites.xlsx>)                                   | 168KB | Wildlife ecology dataset                            |
| [`data/Dangerous Jobs.csv`](<./data/Dangerous Jobs.csv>)                                         | 28MB  | Occupational safety dataset (146K+ records)         |
| [`data/Housing Price Index.xlsx - Data.csv`](<./data/Housing Price Index.xlsx - Data.csv>) | 61KB  | Economic indicators dataset                         |

---

## Key Findings Across Domains

**Wildlife Ecology**: Wild ungulates (mule deer, bighorn sheep, pronghorn) are the primary prey for cougars, while domestic animals represent the least common prey category. Temporal analysis revealed data collection gaps between 2012-2015.

**Occupational Safety**: Identified the most dangerous occupations through comprehensive fatality trend analysis. Alluvial diagrams effectively revealed cause-effect relationships between occupations and fatality types that wouldn't be visible in standard charts.

**Housing Economics**: All four U.S. regions (Midwest, Northeast, South, West) showed similar HPI trends with increases until ~2005, decline, then recovery after 2010. The West region demonstrated higher volatility compared to other regions.

---

## Academic Information

**Course**: INFO 526 - Data Visualization  
**Institution**: University of Arizona  
**Project Type**: Final Course Portfolio  
**Academic Year**: 2024-2025

### What I Applied in This Course

- Implemented fundamental plotting techniques (bar, pie, line, area charts)
- Built advanced visualizations (alluvial diagrams, faceted plots)
- Applied data transformation and categorical grouping strategies
- Created statistical communication through visual narratives
- Established RMarkdown workflow for reproducible research

### Improvements I Made

- Switched from stacked to grouped bar charts for better readability
- Refined categorical grouping to avoid overlapping classifications
- Enhanced color palette selection and visual clarity

---

<p align="center">
  <em>University of Arizona — Graduate Student Data Science Portfolio</em>
</p>
