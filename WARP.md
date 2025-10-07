# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a comprehensive data science and development portfolio showcasing projects in R, Python, Quarto, and web development. The portfolio demonstrates end-to-end data science workflows, interactive dashboards, statistical analysis, and development environment automation.

## Repository Structure

```
portfolio/
├── projects/                    # Main project directories
│   ├── automation/             # DevOps and automation scripts
│   ├── data-science/           # Data science projects and analyses
│   │   └── data-mining-final-project/  # Quarto website with data mining analysis
│   ├── r-analytics/            # R-specific analytics projects
│   │   ├── data-visualization-portfolio/  # RMarkdown portfolio work
│   │   └── sales-dashboard/    # Shiny dashboard application
│   └── web-dev/               # Web development projects
├── assets/docs/               # Documentation and guides
├── skills/                    # Technical skills documentation
├── templates/                 # Project templates and boilerplates
└── workflows/                 # Development workflows and automation
```

## Common Development Commands

### R Development
```bash
# Run R Shiny applications
R -e "shiny::runApp('projects/r-analytics/sales-dashboard')"

# Render RMarkdown documents
R -e "rmarkdown::render('path/to/file.Rmd')"

# Install R dependencies for a project
R -e "renv::restore()"  # If using renv
```

### Python/Jupyter Development
```bash
# Install Python dependencies for data science projects
pip install -r projects/data-science/data-mining-final-project/requirements.txt

# Launch Jupyter for the data mining project
cd projects/data-science/data-mining-final-project && jupyter lab index.ipynb
```

### Quarto Development
```bash
# Render Quarto website (for data mining project)
cd projects/data-science/data-mining-final-project && quarto render

# Preview Quarto website during development
cd projects/data-science/data-mining-final-project && quarto preview

# Publish to GitHub Pages
cd projects/data-science/data-mining-final-project && quarto publish gh-pages
```

## Project-Specific Architecture

### Data Science Projects (`projects/data-science/`)
- **Primary Language**: Python with R integration
- **Key Technologies**: Jupyter, Quarto, scikit-learn, pandas, SHAP
- **Structure**: End-to-end data science pipeline from data ingestion to model deployment
- **Output**: Interactive websites, presentations, and analysis reports

### R Analytics Projects (`projects/r-analytics/`)
- **Primary Language**: R
- **Key Technologies**: Shiny, RMarkdown, tidyverse, ggplot2, plotly
- **Structure**: Interactive dashboards and statistical analysis portfolios
- **Data Visualization**: Heavy use of ggplot2, plotly, and custom visualization functions

### Automation Projects (`projects/automation/`)
- **Primary Languages**: Shell scripting, R automation
- **Focus**: Development environment setup, configuration management, CI/CD workflows
- **Integration**: Git workflows, GitHub Actions, cross-platform compatibility

## Key Technology Stack

### Data Analysis & Statistics
- **R Ecosystem**: tidyverse, ggplot2, shiny, RMarkdown, tidymodels
- **Python Ecosystem**: pandas, numpy, scikit-learn, matplotlib, seaborn, SHAP
- **Statistical Methods**: Machine learning, predictive modeling, data mining, visualization

### Publishing & Documentation
- **Quarto**: Website generation, presentations, reports
- **RMarkdown**: Statistical reports, analysis documentation
- **Jupyter**: Interactive analysis notebooks

### Development Environment
- **IDE Preferences**: Positron (for R), VS Code (general development)
- **Terminal**: Advanced zsh configuration with performance optimizations
- **Version Control**: Git with GitHub integration

## Development Workflow Notes

### For R Development
- Projects may use RMarkdown or Quarto for documentation
- Shiny applications are self-contained in individual directories
- Data visualization follows ggplot2 conventions with plotly integration
- Statistical analysis emphasizes reproducible research principles

### For Python/Data Science Projects
- Jupyter notebooks are primary analysis format
- Requirements.txt files specify Python dependencies
- SHAP library used for model interpretability
- Integration with R when needed for specific statistical functions

### For Quarto Projects
- Multi-format output (HTML, presentations, PDFs)
- Integrated with both R and Python code chunks
- Automated rendering and publishing workflows
- GitHub Pages deployment for web content

## Portfolio Context

This repository serves as a comprehensive portfolio demonstrating:
- **Data Science Expertise**: End-to-end analytical workflows
- **R Programming**: Advanced statistical analysis and visualization
- **Python Integration**: Machine learning and data processing
- **Web Development**: Interactive dashboards and applications  
- **Development Operations**: Automation and environment management
- **Technical Communication**: Documentation, presentations, and tutorials

The structure supports both individual project development and portfolio presentation, with emphasis on reproducible research and professional development practices.