# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load necessary libraries
library(tidyverse)
library(lubridate)

# Data import
repo_group_data <- read.csv("data/raw/augur/repo_group.csv")


# Checking groups
repo_group_filtered <- repo_group_data %>%
  group_by(repo_id) %>%
  filter(n() == 1) %>%
  ungroup()


repo_group_check <- repo_group_data %>%
  group_by(repo_group_id) %>%
  count()

# is it possible that I only have seven organisations in this collection?
# but surely there are more than 7 orgs in the dataset?
# I don't think repo_group_id refers to the org
# nah it's not just 7 orgs, repo_group_id refers to the group they were collected in