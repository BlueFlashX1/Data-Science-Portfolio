# Data Visualization Portfolio

[![Course Project](https://img.shields.io/badge/Course-Final%20Portfolio-blue?style=for-the-badge)](https://github.com)
[![INFO 526](https://img.shields.io/badge/INFO%20526-Data%20Visualization-red?style=for-the-badge)](https://github.com)
[![R](https://img.shields.io/badge/R-4.x-276DC3?style=for-the-badge&logo=r)](https://r-project.org)
[![RMarkdown](https://img.shields.io/badge/RMarkdown-Portfolio-FF6B35?style=for-the-badge&logo=r)](https://rmarkdown.rstudio.com)

> **COURSE FINAL PORTFOLIO**: Comprehensive data visualization projects demonstrating advanced R programming and ggplot2 mastery

**Academic Context**: This is a final portfolio for INFO 526 (Data Visualization) showcasing mastery of R programming, ggplot2, and advanced visualization techniques through multiple assignments and projects.

## Portfolio Overview

This portfolio contains a comprehensive collection of data visualization projects demonstrating proficiency in R programming, statistical graphics, and visual storytelling. The work spans multiple domains including wildlife ecology, occupational safety, and economic indicators.

### Key Visualization Types Demonstrated
- **Basic Plots**: Pie charts and bar charts for categorical data
- **Paneled Visualizations**: Multi-panel layouts for comparative analysis
- **Faceted Plots**: Small multiples for detailed breakdowns
- **Unusual Plots**: Advanced techniques including alluvial diagrams and stream plots
- **Statistical Summaries**: Tables with descriptive statistics

## Project Structure

### Core Portfolio Files

| File | Size | Description |
|------|------|-------------|
| [`Final Portfolio Assignment(Finished).Rmd`](./Final%20Portfolio%20Assignment(Finished).Rmd) | 43KB | Main portfolio with all visualizations and analysis |
| [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf) | 399KB | **Complete rendered portfolio (PDF)** |
| [`Final-Portfolio-Assignment.pdf`](./Final-Portfolio-Assignment.pdf) | 399KB | Alternative PDF version |
| [`Final_MinMaxHPI_Output.pdf`](./Final_MinMaxHPI_Output.pdf) | 75KB | Housing Price Index analysis supplement |

### Individual Assignment Files

| Assignment | File | Size | Focus Area |
|------------|------|------|------------|
| Assignment 1 | [`Weekly_1_Assignment_MatthewT.Rmd`](./Weekly_1_Assignment_MatthewT.Rmd) | 18KB | Basic plotting fundamentals |
| Assignment 2 | [`Weekly3_Assignment2_MatthewThompson.Rmd`](./Weekly3_Assignment2_MatthewThompson.Rmd) | 15KB | Intermediate visualization techniques |
| Assignment 4 | [`Weekly 3_Assignment4.Rmd`](./Weekly%203_Assignment4.Rmd) | 23KB | Advanced plot types |
| Assignment 4 (Alt) | [`Weekly5_Assignment4_MatthewThompson.Rmd`](./Weekly5_Assignment4_MatthewThompson.Rmd) | 15KB | Refined visualization approaches |
| Assignment 5 | [`Assignment 5 Unusual Plots.Rmd`](./Assignment%205%20Unusual%20Plots.Rmd) | 16KB | Innovative visualization techniques |

### Supporting Files

| File | Size | Description |
|------|------|-------------|
| [`Final Portfolio.Rproj`](./Final%20Portfolio.Rproj) | 253B | R project configuration for RStudio |
| [`Data Dictionary Function.R`](./Data%20Dictionary%20Function.R) | 3.7KB | Custom R function for automated data documentation |

## Datasets

### Wildlife Ecology
| Dataset | Size | Description |
|---------|------|-------------|
| [`Cougar Killsites.xlsx`](./Cougar%20Killsites.xlsx) | 168KB | Cougar predation data with prey species and temporal information |

### Occupational Safety
| Dataset | Size | Description |
|---------|------|-------------|
| [`Dangerous Jobs.csv`](./Dangerous%20Jobs.csv) | 28MB | Comprehensive workplace fatality data by occupation and cause |

### Economic Indicators
| Dataset | Size | Description |
|---------|------|-------------|
| [`Housing Price Index.xlsx - Data.csv`](./Housing%20Price%20Index.xlsx%20-%20Data.csv) | 61KB | Housing market trends and price index data |

## Key Visualizations

### 1. Wildlife Predation Analysis
**Data**: Cougar killsite data
**Techniques**: 
- Pie charts for prey species distribution
- Grouped bar charts for temporal analysis
- Custom color palettes for ecological categories

**Key Findings**: Wild ungulates represent the majority of cougar prey, with domestic animals being least common.

### 2. Occupational Safety Trends
**Data**: Workplace fatality statistics
**Techniques**:
- Line plots for temporal trends
- Alluvial diagrams for cause-effect relationships
- Faceted visualizations for comparative analysis

**Key Findings**: Analysis of most dangerous occupations and primary causes of workplace fatalities.

### 3. Housing Market Analysis
**Data**: Housing Price Index data
**Techniques**:
- Area plots for trend visualization
- Statistical summary tables
- Faceted comparisons across regions

**Key Findings**: Regional variations in housing market trends and price volatility.

## Technical Specifications

### R Environment
- **R Version**: 4.x
- **Primary Packages**: ggplot2, dplyr, tidyverse, lubridate
- **Specialized Libraries**: ggalluvial, ggstream, viridis, plotly
- **Document Generation**: RMarkdown to PDF

### Advanced Techniques Demonstrated
- **Custom data transformations** with dplyr and tidyverse
- **Complex grouping strategies** for categorical data
- **Advanced ggplot2 aesthetics** including custom themes and scales
- **Innovative plot types** including alluvial diagrams and stream plots
- **Professional document formatting** with RMarkdown
- **Custom function development** for automated data exploration

## Recommended Viewing

### For Quick Overview
**View the complete portfolio**: [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf)

This 399KB PDF contains all visualizations, analysis, and reflections in a professionally formatted document. It includes:
- Detailed methodology explanations
- Complete code documentation
- Professional figure captions
- Comprehensive reflection on visualization choices

### For Interactive Exploration
**Examine the source code**: [`Final Portfolio Assignment(Finished).Rmd`](./Final%20Portfolio%20Assignment(Finished).Rmd)

This RMarkdown file contains all the reproducible code and can be executed to:
- Regenerate all visualizations
- Modify parameters and styling
- Explore alternative approaches
- Understand data transformation processes

## Installation & Usage

### Prerequisites
```r
# Required R packages
install.packages(c(
  "ggplot2", "dplyr", "tidyverse", "lubridate", 
  "reshape2", "readxl", "viridis", "ggstream", 
  "ggalluvial", "knitr", "rmarkdown"
))
```

### Running the Portfolio
```r
# Open RStudio and load the main file
rmarkdown::render("Final Portfolio Assignment(Finished).Rmd")

# Or open the R project file for best experience
# Double-click "Final Portfolio.Rproj" to open in RStudio
```

### Using the Data Dictionary Function

The portfolio includes a custom `data_dict()` function for automated data exploration and documentation.

#### Loading the Function
```r
# Source the function
source("Data Dictionary Function.R")

# The function will automatically install required packages:
# tidyverse, psych, ggpubr, gridExtra, Lahman
```

#### Function Usage
```r
# Basic usage - returns data frame
data_dict(your_dataset, print_table = "No")

# Table output - returns formatted table
data_dict(your_dataset, print_table = "Yes")
```

#### Function Features
- **Variable Information**: Names, types, missing value counts
- **Descriptive Statistics**: Mean, SD, median, min, max, range (for numeric variables)
- **Smart Handling**: Only calculates numeric stats for appropriate variable types
- **Flexible Output**: Data frame or formatted table
- **Self-contained**: Includes built-in examples and handles package installation

#### Example Usage
```r
# Try with built-in demo data (included in function)
source("Data Dictionary Function.R")

# Example with your own data
my_data <- read.csv("your_data.csv")
data_summary <- data_dict(my_data, print_table = "No")
print(data_summary)

# Create a formatted table
data_table <- data_dict(my_data, print_table = "Yes")
```

## Project Structure

```
data-visualization-portfolio/
├── Final Portfolio.Rproj                         # R project configuration
├── README.md                                     # This documentation file
├── Final Portfolio Assignment(Finished).Rmd      # Main portfolio source code
├── MatthewThompson_Final_Portfolio.pdf           # Complete rendered portfolio (399KB)
├── Data Dictionary Function.R                    # Custom data exploration function
├── Cougar Killsites.xlsx                         # Wildlife ecology dataset (168KB)
├── Dangerous Jobs.csv                            # Occupational safety dataset (28MB)
└── Housing Price Index.xlsx - Data.csv           # Economic indicators dataset (61KB)
```

### Professional Structure Notes
- **R Project File**: Ensures consistent working directory and RStudio settings
- **Single Main File**: All analysis consolidated in one comprehensive RMarkdown document  
- **Complete PDF Output**: Professionally formatted final portfolio with all visualizations
- **Custom Function**: Demonstrates advanced R programming capabilities
- **Essential Data Only**: Three key datasets supporting all visualizations
- **Clean Organization**: No unnecessary intermediate files or assignments

## Academic Information

**Course**: INFO 526 - Data Visualization  
**Institution**: University of Arizona  
**Project Type**: Final Course Portfolio  
**Grade Self-Assessment**: B (demonstrating solid grasp of fundamentals with ongoing progress toward mastery)

### Learning Objectives Demonstrated
- **Fundamental Plotting**: Mastery of basic chart types (bar, pie, line, area)
- **Advanced Techniques**: Implementation of complex visualizations (alluvial, stream)
- **Design Principles**: Application of color theory, typography, and layout
- **Data Storytelling**: Effective communication of insights through visual narrative
- **Technical Proficiency**: Advanced R programming and package utilization

## Reflection & Growth

This portfolio represents significant growth in data visualization capabilities, with particular improvements in:

- **Category Management**: Better grouping decisions to avoid overlapping classifications
- **Visual Clarity**: Moving from overly complex stacked plots to clearer grouped visualizations
- **Aesthetic Refinement**: Improved color choices, labeling, and overall design quality
- **Technical Challenges**: Successful implementation of advanced plot types despite initial difficulties

Areas for continued development include:
- **Label Positioning**: Further refinement of text placement in complex plots
- **Interactive Elements**: Exploration of dynamic visualization capabilities
- **Advanced Statistical Graphics**: Integration of more sophisticated analytical visualizations

## File Recommendations

**For Portfolio Review**: Use [`MatthewThompson_Final_Portfolio.pdf`](./MatthewThompson_Final_Portfolio.pdf) - it provides the most complete and professionally formatted view of all work with proper context and explanations.

**For Code Review**: Examine [`Final Portfolio Assignment(Finished).Rmd`](./Final%20Portfolio%20Assignment(Finished).Rmd) - it contains all the reproducible code and detailed comments.

**For Assignment History**: Individual assignment files show the progression of skills throughout the course.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

---

<div align="center">

**A course portfolio demonstrating the art and science of data visualization**

*Transforming complex data into compelling visual narratives through R and ggplot2*

</div>