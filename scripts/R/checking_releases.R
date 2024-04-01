# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Load necessary libraries
library(tidyverse)
library(lubridate)

# Data import
releases_raw <- read.csv(paste0(base_path, "data/raw/augur/releases-all.csv")) %>%
  mutate(
    # Convert date formats and extract components
    release_created_at = ymd_hms(release_created_at),
    date = as.Date(release_created_at),
  )



# ChatGPT:

# Assuming releases_grouped and repo_group_data are already defined and available
# Merge dataframes on 'repo_id'
merged_data <- left_join(releases_grouped, repo_group_data, by = "repo_id") %>%
  # Additional manipulation can go here if necessary
  # Extract organization name from repo_git (assuming this column exists in releases_raw)
  mutate(org_name = str_extract(repo_git, "(?<=github\\.com\\/)[^\\/]+"))

# Writing the processed data to a CSV file
write.csv(merged_data, paste0(base_path, "data/processed/merged_data.csv"), row.names = FALSE)

# Aggregate data: Count releases by org_name and date
releases_over_time <- merged_data %>%
  group_by(org_name, date) %>%
  summarise(releases_count = n(), .groups = 'drop')  # Adjusted to count by org_name

# Plot the aggregated data
ggplot(releases_over_time, aes(x = date, y = releases_count, color = as.factor(org_name))) +
  geom_line() +
  geom_point(size = 1, alpha = 0.6) +
  theme_minimal() +
  labs(title = "Number of Releases by Organization Over Time",
       x = "Date", y = "Number of Releases", color = "Organization") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Note: The 'repo_group_id' references changed to 'org_name' 
