# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load necessary libraries
library(tidyverse)
library(lubridate)

# Data import
investment_all <- read.csv(paste0(base_path, "data/raw/augur/repo_commits_all.csv"))

repo_group_check <- read.csv(paste0(base_path, "data/raw/augur/repo_group.csv"))