# Install R packages required to knit Final-Portfolio-Assignment.Rmd.
# Run once in a fresh R or RStudio session before knitting.

required_packages <- c(
  "tidyverse",   # ggplot2, dplyr, tidyr, lubridate, readr
  "readxl",      # .xlsx reader (cougar data)
  "ggalluvial",  # alluvial diagrams
  "viridis",     # color palettes
  "patchwork",   # multi-plot composition
  "gt",          # publication-quality tables
  "reshape2",    # legacy wide/long reshape
  "rmarkdown",   # render the Rmd to PDF
  "tinytex",     # bundled LaTeX distribution for PDF rendering
  "webshot2"     # used by gt::gtsave() to export the HPI table as a PDF (needs Chrome)
)

missing <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]
if (length(missing) > 0) {
  cat("Installing missing packages:", paste(missing, collapse = ", "), "\n")
  install.packages(missing)
} else {
  cat("All required packages already installed.\n")
}

# Ensure LaTeX is available for PDF rendering.
# tinytex::install_tinytex() downloads ~150MB and installs a minimal TeX
# distribution into ~/Library/TinyTeX (or platform equivalent). Idempotent.
if (!tinytex::is_tinytex() && !nzchar(Sys.which("pdflatex"))) {
  cat("No system LaTeX detected. Installing TinyTeX (~150MB, one-time)...\n")
  tinytex::install_tinytex()
} else {
  cat("LaTeX detected. PDF rendering ready.\n")
}
