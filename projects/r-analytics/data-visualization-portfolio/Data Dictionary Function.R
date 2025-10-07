
### Data Dictionary Function ###

data_dict <- function(data, print_table = "No"){
  
  # List of required packages
  required_packages <- c("tidyverse", "psych", "ggpubr", "gridExtra", "Lahman")
  
  # Install any missing packages
  for (pkg in required_packages) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      install.packages(pkg)
    }
  }
  
  # Load the required packages
  lapply(required_packages, library, character.only = TRUE)
  
  # packages
  suppressPackageStartupMessages(suppressWarnings(require(tidyverse)))
  suppressPackageStartupMessages(suppressWarnings(require(psych)))
  suppressPackageStartupMessages(suppressWarnings(require(ggpubr)))
  suppressPackageStartupMessages(suppressWarnings(require(gridExtra)))
  
  # Load required libraries at the start of your script or RMarkdown
  library(tidyverse)
  library(psych)
  library(ggpubr)
  library(gridExtra)
  
  # get rid of scientific notation
  options(scipen = 999)
  
  #get variable info(type and missing values)
  var_info <- data.frame(
    Variable = names(data),
    VariableType = sapply(data, class),
    MissingValues = sapply(data, function(y) sum(is.na(y))),
    row.names = NULL
  )
  
  # Handle numeric columns for descriptive stats
  numeric_cols <- data[, sapply(data, is.numeric), drop = FALSE]
  if (ncol(numeric_cols) > 0) {
    desc_stats <- data.frame(
      Variable = names(numeric_cols),
      describe(numeric_cols)[, c("mean", "sd", "median", "se", "min", "max", "range")],
      row.names = NULL
    )
  } else {
    desc_stats <- data.frame()  # Empty if no numeric columns
  }
  
  # Merge variable info and descriptive stats
  d_dict <- merge(var_info, desc_stats, by = "Variable", all.x = TRUE)
  
  # Round numeric columns and replace NA for non-numeric variables
  d_dict <- d_dict %>%
    mutate(across(c(mean, sd, median, se, min, max, range), ~ ifelse(is.na(.), "", round(., 2))))
  
  # Return data dictionary
  if (print_table == "No") {
    return(d_dict)
  } else {
    return(ggtexttable(d_dict, rows = NULL))
  }
}

  # NA's for summary stats of variables not of class numeric or integer
   d_dict <- d_dict %>%
    mutate(mean = ifelse(VariableType == "numeric" | VariableType == "integer", mean, ""),
           sd = ifelse(VariableType == "numeric" | VariableType == "integer", sd, ""),
           median = ifelse(VariableType == "numeric" | VariableType == "integer", median, ""),
           se = ifelse(VariableType == "numeric" | VariableType == "integer", se, ""),
           min = ifelse(VariableType == "numeric" | VariableType == "integer", min, ""),
           max = ifelse(VariableType == "numeric" | VariableType == "integer", max, ""),
           range = ifelse(VariableType == "numeric" | VariableType == "integer", range, ""))
   # return the result
   if(print_table == "No"){
     
     return(d_dict)
     
   } else {
     #create table if table = TRUE
     d_dict <- ggtexttable(d_dict,
                           rows = NULL)
     
     return(d_dict)
     
   }
}

## create fake data

Names <- c("Sal", "John", "Jeff", "Karl", "Ben")
HomeTown <- c("CLE", "NYC", "CHI", "DEN", "SEA")
var1 <- rnorm(n = length(Names), mean = 10, sd = 2)
var2 <- rnorm(n = length(Names), mean = 300, sd = 150)
var3 <- rnorm(n = length(Names), mean = 1000, sd = 350)
var4 <- c(6, 7, NA, 3, NA)

df <- data.frame(Names, HomeTown, var1, var2, var3, var4)
df

# Data dictionary without table
data_dict(df, print_table = "No")

# Data dictionary with table
data_dict(df, print_table = "Yes")

### Try the data dictionary on a larger data set

library(Lahman)

# without table
data_dict(Batting, print_table = "No")

# with table
data_dict(Batting, print_table = "Yes")
