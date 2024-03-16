
library(tidyverse)
library(lubridate)
library(dplyr)

merged_data_new <- read.csv("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/merged_data_new.csv")

# Assuming your merged dataframe is named 'merged_data'
# And assuming 'release_count' is already the count of releases per repo_id per date
# Now, summing up the release counts per org_name per date
releases_per_org_date <- merged_data_new %>%
  group_by(org_name, date) %>%
  summarise(total_releases = sum(release_count), .groups = 'drop')

# View the resulting dataframe
head(releases_per_org_date)

# Assuming your dataframe is named 'merged_data' and has a column 'org_name'
number_of_orgs <- merged_data_new %>%
  summarise(total_orgs = n_distinct(org_name)) %>%
  pull(total_orgs)

# Print the number of unique organizations
print(number_of_orgs)
