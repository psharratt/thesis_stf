
### WARNING THIS DOES NOT WORK - Use Python function instead:
# /Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/scripts/Python/plotting_treatment_repo_commits_over_time.py

# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

library(readxl)
library(ggplot2)
library(dplyr)
library(lubridate)

# Load the Excel file into a data frame
file_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/commits_data_2.xlsx" # Adjust the path for this environment
commits_data_2_df <- read_excel(file_path)

# Ensure 'date' is a Date type
commits_data_2_df$date <- as.Date(commits_data_2_df$date)

# Define the directory for plots
plots_dir <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/output/graphs/repo commits over time/R file test" # Adjust the path for this environment
dir.create(plots_dir, recursive = TRUE, showWarnings = FALSE)

# Loop through each unique repo_id to create and save plots
for (repo_id in unique(commits_data_2_df$repo_id)) {
  # Filter data for the current repo_id
  repo_data <- filter(commits_data_2_df, repo_id == repo_id)
  
  # Generate the plot
  p <- ggplot(repo_data, aes(x = date, y = total_commits)) +
    geom_line() + geom_point() +
    labs(title = paste("Total Commits Over Time for", repo_data$repo[1], "(ID:", repo_id, ")"),
         x = "Date", y = "Total Commits") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Save the plot
  ggsave(paste0(plots_dir, "repo_", repo_id, ".png"), plot = p, width = 10, height = 6)
}



