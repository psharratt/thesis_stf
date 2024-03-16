
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/")

# Load necessary libraries
library(tidyverse)
library(lubridate)

# Data import
releases_raw <- read.csv("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/raw/releases-all.csv")

### doesn't quite work - need to cross reference in the org id otherwise it's not manageable

# Assuming your releases_raw dataframe's release_created_at column is already in datetime format.
# If not, convert it:
releases_raw$release_created_at <- ymd_hms(releases_raw$release_created_at)

# First, let's create a new column that just contains the date part of release_created_at
releases_raw$date <- as.Date(releases_raw$release_created_at)

# Now, group by repo_id and date, and count the number of releases
releases_grouped <- releases_raw %>%
  group_by(repo_id, date) %>%
  summarise(release_count = n(), .groups = 'drop')  # Drop groups for easier plotting

# Plot the data with ggplot2
releases_grouped %>%
  ggplot(aes(x = date, y = release_count, group = repo_id)) +
  geom_line(aes(color = as.factor(repo_id)), alpha = 0.75) +  # Connects counts over time by repo_id
  geom_point(aes(color = as.factor(repo_id))) +  # Visualize each count
  theme_minimal() +
  labs(x = "Date", y = "Number of Releases", title = "Time Series of Release Counts by Repo", color = "Repo ID") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Improve date labels readability


