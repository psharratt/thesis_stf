# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load necessary libraries
library(tidyverse)
library(lubridate)
library(readxl)
library(readr)

# Import treatment group data
treatment_group <- read_excel(paste0(base_path, "data/raw/investment/target_group.xlsx"))

# Import augur repo groups all data
repo_groups_all <- read_csv("data/raw/augur/repo_groups_all.csv")

# Load the repo_group.csv file
repo_group <- read_csv("data/raw/augur/repo_group.csv")


# View the structure and first few rows of the dataframe
str(repo_group)
head(repo_group)


