
merged_data_new <- read.csv("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/merged_data_new.csv")

library(dplyr)
library(lubridate)



# Assuming 'releases_raw' and 'repo_org_mapping' are your dataframes
# And both have a 'repo_id' column
# Ensure that 'repo_id' columns in both dataframes are of the same type
releases_raw <- left_join(releases_raw, repo_group_data, by = "repo_id")

releases_master <- releases_raw %>%
  mutate(org_name = str_extract(repo_git.x, "(?<=github\\.com\\/)[^\\/]+"))

# THIS DOESN'T QUITE WORK!!!

# Convert release_created_at to Date if it's not already
releases_master$release_created_at <- as.Date(merged_data$release_created_at)

# Calculate monthly release frequency for each org
release_frequency <- releases_master %>%
  mutate(year_month = floor_date(release_created_at, "month")) %>%
  group_by(org_name, year_month) %>%
  summarise(releases = n(), .groups = 'drop')

# View the results
head(release_frequency)