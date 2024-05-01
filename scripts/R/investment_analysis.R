# Seting working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load libraries
library(tidyverse)
library(lubridate)
library(readxl)
library(readr)
library(dplyr)
library(stringr)
library(openxlsx)


# Import treatment group data
treatment_group <- read_excel(paste0(base_path, "data/raw/investment/target_group.xlsx"))

# Import augur repo groups all data
repo_groups_all <- read_csv("data/raw/augur/repo_groups_all.csv")

repo_ids <- read_csv("data/processed/target_group_repo_ids.csv")

treatment_group <- treatment_group %>%
  rename(org_url = org, repo_url = repo)

# Adjusted step for extracting org and repo names without str_remove_suffix
treatment_group <- treatment_group %>%
  mutate(
    org = str_extract(org_url, "(?<=github.com/)[^/]+") %>% str_replace("/$", ""),
  )

# Double-check the extraction results
head(treatment_group)

# Perform the join
treatment_group_final <- left_join(treatment_group, repo_ids, by = c("org"))

treatment_group_final <- treatment_group_final %>%
  mutate(start_date = as.Date(start_date, format = "%B %d, %Y"), # Adjust format based on original format
         end_date = as.Date(end_date, format = "%B %d, %Y")) %>% # Adjust format based on original format
  select(org, repo, org_url, repo_url, repo_id, everything())

# Verify the merged data
head(treatment_group_final)

# Specifying the path and filename from Excel file
file_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/treatment_group_final.xlsx"

# Exporting the data frame to  Excel 
write.xlsx(treatment_group_final, file = file_path)



