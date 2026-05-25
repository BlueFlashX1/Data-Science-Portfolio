# Install R packages required to knit Final-Portfolio-Assignment.Rmd.
# Run once in a fresh R or RStudio session before knitting.

required_packages <- c(
  "tidyverse",   # ggplot2, dplyr, tidyr, lubridate, readr
  "readxl",      # .xlsx reader (cougar data)
  "ggalluvial",  # alluvial diagrams
  "ggstream",    # stream plots
  "viridis",     # color palettes
  "patchwork",   # multi-plot composition
  "gt",          # publication-quality tables
  "reshape2",    # legacy wide/long reshape
  "rmarkdown"    # render the Rmd to PDF
)

missing <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]
if (length(missing) > 0) {
  cat("Installing missing packages:", paste(missing, collapse = ", "), "\n")
  install.packages(missing)
} else {
  cat("All required packages already installed.\n")
}

# PDF rendering also requires LaTeX. If you do not have a system TeX install:
#   install.packages("tinytex"); tinytex::install_tinytex()
