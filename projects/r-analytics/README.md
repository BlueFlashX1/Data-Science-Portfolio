# R Analytics Projects

[![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white)](https://r-project.org)
[![ggplot2](https://img.shields.io/badge/ggplot2-Visualization-orange?style=for-the-badge&logo=r)](https://ggplot2.tidyverse.org)
[![RMarkdown](https://img.shields.io/badge/RMarkdown-Reproducible-FF6B35?style=for-the-badge)](https://rmarkdown.rstudio.com)

> **Course portfolio demonstrating R programming and ggplot2 across wildlife, safety, and economic datasets**

## Featured Project

### [Data Visualization Portfolio](./data-visualization-portfolio/)

**INFO 526 - Data Visualization** | Final Portfolio

![R](https://img.shields.io/badge/R-4.x-276DC3?style=flat-square&logo=r&logoColor=white)
![ggplot2](https://img.shields.io/badge/ggplot2-3.4-E34F26?style=flat-square)
![tidyverse](https://img.shields.io/badge/tidyverse-Data%20Wrangling-1A162D?style=flat-square)
![RMarkdown](https://img.shields.io/badge/RMarkdown-Reporting-FF6B35?style=flat-square)

**Project Scope**

- **3 Domain Analyses**: Wildlife ecology, occupational safety, housing economics
- **Advanced Visualizations**: Alluvial diagrams, faceted plots, temporal trends
- **Custom Function**: Automated data dictionary generator
- **Reproducible Research**: RMarkdown → PDF publication workflow

**What I Applied**

| Domain                  | Analysis                              | Key Insight                                                                                   |
| ----------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Wildlife Ecology**    | Cougar predation patterns (2012-2016) | Identified wild ungulates (mule deer, bighorn) as primary prey; domestic animals least common |
| **Occupational Safety** | Top 5 dangerous occupations           | Used alluvial diagrams to reveal cause-effect relationships for fatalities                    |
| **Housing Economics**   | Regional HPI trends                   | Discovered West shows highest volatility; all regions declined ~2005, recovered post-2010     |

**Technical Highlights**

- Categorical grouping strategies to avoid classification overlap
- Custom `data_dict()` function for automated data exploration
- Publication-ready PDF output (399KB, 991 lines of R code)
- Color palette design for ecological data visualization

---

## Skills Applied

### Data Manipulation

![dplyr](https://img.shields.io/badge/dplyr-Data%20Wrangling-1A162D?style=flat-square)
![tidyr](https://img.shields.io/badge/tidyr-Reshaping-1A162D?style=flat-square)
![lubridate](https://img.shields.io/badge/lubridate-Dates-1A162D?style=flat-square)

- Performed complex data transformations with tidyverse
- Processed and analyzed temporal data
- Implemented missing value handling strategies
- Developed custom functions for reusable analysis

### Visualization

![ggplot2](https://img.shields.io/badge/ggplot2-Grammar%20of%20Graphics-E34F26?style=flat-square)
![ggalluvial](https://img.shields.io/badge/ggalluvial-Flow%20Diagrams-FF6B6B?style=flat-square)
![viridis](https://img.shields.io/badge/viridis-Color%20Palettes-440154?style=flat-square)

| Visualization Type     | Use Case                                    |
| ---------------------- | ------------------------------------------- |
| **Pie Charts**         | Proportional distribution (prey categories) |
| **Grouped Bar Charts** | Temporal comparisons                        |
| **Line Plots**         | Trend analysis over time                    |
| **Alluvial Diagrams**  | Cause-effect relationship mapping           |
| **Faceted Area Plots** | Multi-group comparisons                     |

### Reporting & Reproducibility

- **RMarkdown**: Created literate programming combining code and narrative
- **PDF Generation**: Generated professional document output
- **Code Documentation**: Wrote inline comments and function documentation
- **Version Control**: Managed project with Git

---

## Project Structure

```text
r-analytics/
├── README.md                          # This file
└── data-visualization-portfolio/
    ├── MatthewThompson_Final_Portfolio.pdf   # Complete rendered output
    ├── Final Portfolio Assignment(Finished).Rmd  # Source code (991 lines)
    ├── Data Dictionary Function.R     # Custom exploration function
    ├── Final Portfolio.Rproj          # RStudio project file
    └── data/
        ├── Cougar Killsites.xlsx      # Wildlife ecology (168KB)
        ├── Dangerous Jobs.csv         # Occupational safety (28MB)
        └── Housing Price Index.xlsx   # Economic indicators (61KB)
```

---

## Quick Start

### Prerequisites

```r
# Install required packages
install.packages(c(
  "ggplot2", "dplyr", "tidyverse", "lubridate",
  "reshape2", "readxl", "viridis", "ggstream",
  "ggalluvial", "knitr", "rmarkdown"
))
```

### View the Portfolio

1. **Complete Work**: Open [`MatthewThompson_Final_Portfolio.pdf`](./data-visualization-portfolio/MatthewThompson_Final_Portfolio.pdf)
2. **Source Code**: Open `.Rmd` file in RStudio
3. **Regenerate**: `rmarkdown::render("Final Portfolio Assignment(Finished).Rmd")`

---

## Academic Information

**Course**: INFO 526 - Data Visualization  
**Institution**: University of Arizona  
**Academic Year**: 2024-2025  
**Program**: Graduate Student — M.S. in Data Science

---

<p align="center">
  <em>R programming and statistical visualization for data-driven insights</em><br>
  <em>Part of the Data Science Portfolio | University of Arizona</em>
</p>
