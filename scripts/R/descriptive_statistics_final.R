library(dplyr)
library(tidyr)
library(gtsummary)
library(gt)
library(readxl)
library(writexl)

# https://epirhandbook.com/en/descriptive-tables.html

setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

data <- read_xlsx("data/DiD/FINAL_TRIMMED_DATASET.xlsx")

# Convert time_period to datetime if it's not already
data$time_period <- as.Date(data$time_period)

# Define start and end dates
start_date <- as.Date("2019-01-01")
end_date <- as.Date("2024-04-01")

# Filter data for the specified time period
trimmed_data <- data %>%
  filter(time_period >= start_date & time_period <= end_date)

selected_cols <- c(
  'treated', 'active_repositories', 'contributors', 'release_count',
  'running_total_open_issues', 'unique_contributors',
  'avg_commits_per_contributor', 'average_closure_days',
  'unique_pull_requests', 'open_pull_requests', 'closed_pull_requests'
)

# Define columns where you want to impute zeros for NA values
columns_to_impute_zeros <- c("active_repositories", "contributors", "release_count",
                             "running_total_open_issues", "unique_contributors",
                             "avg_commits_per_contributor", "average_closure_days",
                             "unique_pull_requests", "open_pull_requests", "closed_pull_requests",
                             "log_active_repositories", "log_contributors", "log_release_count",
                             "log_running_total_open_issues", "log_unique_contributors",
                             "log_avg_commits_per_contributor", "log_average_closure_days",
                             "log_unique_pull_requests", "log_open_pull_requests", "log_closed_pull_requests"
                             )

# Impute zeros for NA values in selected columns
trimmed_data <- trimmed_data %>%
  mutate(across(all_of(columns_to_impute_zeros), ~replace_na(., 0)))


# Define the file path and name where you want to save the document
output_file <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/output/tables/Summary_Statistics_FINAL.docx"

trimmed_data %>% 
  select(all_of(selected_cols)) %>% 
  tbl_summary(     
    by = treated,                  
    statistic = list(
      all_continuous() ~ c("{mean} ({sd})", "{median} ({p25}, {p75})", "{min}, {max}"),
      all_categorical() ~ "{n} / {N} ({p}%)"
    ),   
    digits = all_continuous() ~ 1,                              
    type = list(all_continuous() ~ "continuous2", all_categorical() ~ "categorical"),                 
    label = list(    
      active_repositories ~ "Active Repositories",  
      contributors ~ "Contributors",  
      release_count ~ "Releases Per Month",  
      running_total_open_issues ~ "Open Issues",  
      unique_contributors ~ "Unique Contributors",  
      avg_commits_per_contributor ~ "Average Commits per Contributor",  
      average_closure_days ~ "Average Closure Days",  
      unique_pull_requests ~ "Unique Pull Requests",  
      open_pull_requests ~ "Open Pull Requests",  
      closed_pull_requests ~ "Closed Pull Requests"
    ),
    missing_text = "Missing"                                    
  ) %>%
  as_gt() %>%
  gt::gtsave(filename = output_file)

write_xlsx(trimmed_data, "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/DiD/FINAL_TRIMMED_DATASET.xlsx")

