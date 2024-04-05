# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load necessary libraries
library(tidyverse)
library(lubridate)
library(readxl)

# Data import
treatment_group <- read_excel(paste0(base_path, "data/raw/investment/investment dataset_dataset_v3.xlsx"))

# need to get descriptive stats on the different orgs, i.e. number of repos, number of contributors, average commits etc all before the treatment happened