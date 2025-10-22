# Data Visualization Portfolio

[![Course Project](https://img.shields.io/badge/Course-Final%20Portfolio-blue?style=for-the-badge)](https://github.com)
[![INFO 526](https://img.shields.io/badge/INFO%20526-Data%20Visualization-red?style=for-the-badge)](https://github.com)
[![R](https://img.shields.io/badge/R-4.x-276DC3?style=for-the-badge&logo=r)](https://r-project.org)
[![RMarkdown](https://img.shields.io/badge/RMarkdown-Portfolio-FF6B35?style=for-the-badge&logo=r)](https://rmarkdown.rstudio.com)

> **Data visualization portfolio demonstrating R programming, ggplot2, and statistical graphics across ecological, safety, and economic datasets** • University of Arizona, INFO 526 (2024-2025)

**[View Complete Portfolio (PDF)](./MatthewThompson_Final_Portfolio.pdf)** | **[Source Code (.Rmd)](<./Final%20Portfolio%20Assignment(Finished).Rmd>)**

---

## Project Overview

Created comprehensive visualizations analyzing wildlife predation patterns, workplace safety trends, and housing market dynamics using R, ggplot2, and tidyverse. Demonstrates technical proficiency in data transformation, categorical grouping, and multi-plot layouts for comparative analysis.

---

## Hard Skills & Visualization Tools

**Languages & Libraries**: R 4.x • RMarkdown • ggplot2 • tidyverse (dplyr, tidyr) • lubridate  
**Specialized Packages**: ggalluvial (alluvial diagrams) • viridis (color palettes) • patchwork (multi-plot layouts)  
**Visualization Types**: Pie charts • Grouped bar charts • Line plots • Alluvial diagrams • Faceted area plots • Statistical tables  
**Technical Skills**: Data transformation • Categorical grouping • Custom color palettes • Temporal analysis • Custom function development

## Visualizations & Findings

### 1. Cougar Predation Ecology

**Dataset**: 168KB cougar killsite data with prey species and temporal information  
**Visualizations**: Pie chart (prey distribution) • Grouped bar chart (temporal trends)  
**Analysis**: Grouped prey species into 4 ecological categories (Wild Ungulates, Small Animals, Domestic Animals, Carnivores)

**Key Findings**:

- Wild ungulates (mule deer, bighorn sheep, pronghorn) are primary prey
- Domestic animals represent least common prey category
- Temporal patterns show data gaps between 2012-2015
- Year 2016: No domestic animal kills recorded

**Technical Skills**: Custom grouping strategies to avoid overlapping classifications • Categorical data transformation with dplyr • Color palette design for ecological categories

---

### 2. Occupational Safety Analysis

**Dataset**: 28MB comprehensive workplace fatality data by occupation and cause  
**Visualizations**: Line graph (temporal trends) • Alluvial diagram (cause-effect relationships)  
**Analysis**: Top 5 most dangerous occupations with temporal trends and cause-effect relationships

**Key Findings**:

- Identified most dangerous occupations with fatality trends over time
- Alluvial diagram reveals common causes of fatalities for each occupation
- Line plots show clearer temporal trends than proportional stream graphs

**Technical Skills**: Advanced plot types (alluvial diagrams with ggalluvial) • Temporal trend visualization • Cause-effect relationship mapping

---

### 3. Housing Price Index Trends

**Dataset**: 61KB housing market data across 4 U.S. regions  
**Visualizations**: Faceted area plots (trend comparison) • Statistical summary tables  
**Analysis**: Seasonally-adjusted vs non-adjusted HPI comparisons across Northeast, Midwest, South, West

**Key Findings**:

- Midwest, Northeast, and South show similar HPI trends
- West region shows higher volatility with seasonally-adjusted HPI occasionally exceeding non-adjusted
- All regions show HPI increase until ~2005, decline, then recovery after 2010
- Regional variations in price volatility documented

**Technical Skills**: Faceted visualizations with small multiples • Area plots for trend analysis • Statistical summary tables • Regional comparisons

---

## Technical Implementation

### Reproducible Research Workflow

- **RMarkdown to PDF**: Complete code documentation with rendered output
- **Custom Functions**: `data_dict()` function for automated data exploration (variable info, descriptive stats, missing values)
- **Data Transformation**: Complex categorical grouping, handling missing values, temporal data processing

## Project Files

| File                                                                                             | Size  | Description                                                                 |
| ------------------------------------------------------------------------------------------------ | ----- | --------------------------------------------------------------------------- |
| [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf)                   | 399KB | **Complete rendered portfolio** with all visualizations, code, and analysis |
| [`Final Portfolio Assignment(Finished).Rmd`](<./Final%20Portfolio%20Assignment(Finished).Rmd>)   | 43KB  | Reproducible source code (992 lines)                                        |
| [`Data Dictionary Function.R`](./Data%20Dictionary%20Function.R)                                 | 3.7KB | Custom data exploration function                                            |
| [`data/Cougar Killsites.xlsx`](./data/Cougar%20Killsites.xlsx)                                   | 168KB | Wildlife ecology dataset                                                    |
| [`data/Dangerous Jobs.csv`](./data/Dangerous%20Jobs.csv)                                         | 28MB  | Occupational safety dataset                                                 |
| [`data/Housing Price Index.xlsx - Data.csv`](./data/Housing%20Price%20Index.xlsx%20-%20Data.csv) | 61KB  | Economic indicators dataset                                                 |

## Quick Start

### Prerequisites

```r
# Required R packages
install.packages(c("ggplot2", "dplyr", "tidyverse", "lubridate",
                   "reshape2", "readxl", "viridis", "ggstream",
                   "ggalluvial", "knitr", "rmarkdown"))
```

### Running the Portfolio

1. **View Complete Work**: Open [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf) for professionally formatted visualizations and analysis
2. **Explore Source Code**: Open [`Final Portfolio Assignment(Finished).Rmd`](<./Final%20Portfolio%20Assignment(Finished).Rmd>) in RStudio
3. **Regenerate Output**: Run `rmarkdown::render("Final Portfolio Assignment(Finished).Rmd")` to rebuild the PDF

### Data Dictionary Function

Custom function for automated data exploration:

```r
source("Data Dictionary Function.R")

# Basic usage
data_summary <- data_dict(your_dataset, print_table = "No")  # Returns data frame
data_table <- data_dict(your_dataset, print_table = "Yes")   # Returns formatted table
```

**Function Features**: Variable types, missing values, descriptive statistics (mean, SD, median, min, max, range)

## Academic Information

**Course**: INFO 526 - Data Visualization  
**Institution**: University of Arizona  
**Project Type**: Final Course Portfolio  
**Academic Year**: 2024-2025  
**Grade Self-Assessment**: B (solid grasp of fundamentals with ongoing progress toward mastery)

### Key Learning Outcomes

- Fundamental plotting techniques (bar, pie, line, area charts)
- Advanced visualization methods (alluvial diagrams, faceted plots)
- Data transformation and categorical grouping strategies
- Statistical communication through visual narratives
- RMarkdown workflow for reproducible research

### Areas of Growth

**Improvements Made**:

- Moved from stacked to grouped bar charts for better readability
- Refined categorical grouping to avoid overlapping classifications
- Improved color palette selection and visual clarity

**Challenges Encountered**: Label positioning in complex plots, initial difficulties with alluvial diagram implementation

---

<div align="center">

**University of Arizona Master's Data Science Portfolio**  
_Demonstrating R programming and statistical visualization capabilities_

</div>
