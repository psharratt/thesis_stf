# Install and load necessary packages
if (!requireNamespace("fixest", quietly = TRUE)) {
  install.packages("fixest")
}
library(fixest)

if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl")
}
library(readxl)

# Install and load dplyr for data manipulation
if (!requireNamespace("tidyr", quietly = TRUE)) {
  install.packages("tidyr")
}
library(tidyr)
library(dplyr)

# Set the working directory and data path
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

# Load the data
data_path <- "data/DiD/final_did_dataset_log_transformed_v2.xlsx"
did_data <- read_xlsx(data_path)

# Convert 'time_period' to Date (if it's not already in that format) and ensure it's a factor
did_data$time_period <- as.Date(did_data$time_period, format = "%Y-%m-%d")
did_data$time_period <- as.factor(did_data$time_period)
did_data$org_name <- as.factor(did_data$org_name)

# Generate lead and lag variables for treatment
did_data <- did_data %>%
  group_by(org_name) %>%
  arrange(time_period) %>%
  mutate(
    lag_treated1 = lag(treated, 1),
    lag_treated2 = lag(treated, 2),
    lead_treated1 = lead(treated, 1),
    lead_treated2 = lead(treated, 2)
  ) %>%
  fill(lag_treated1, lag_treated2, lead_treated1, lead_treated2, .direction = "updown") %>%
  ungroup()

# Dependent variables to analyze
dependent_vars <- c("log_contributors", "log_release_count", "log_running_total_open_issues",
                    "log_avg_commits_per_contributor", "log_average_closure_days")

# Loop through each dependent variable to apply the staggered DiD model with dynamic specifications
results <- list()
for (dep_var in dependent_vars) {
  formula <- as.formula(paste(dep_var, "~ treated + lag_treated1 + lag_treated2 + lead_treated1 + lead_treated2 + treated:time_period | org_name + time_period", sep = ""))
  model <- feols(formula, data = did_data)
  results[[dep_var]] <- summary(model)
}

# Output the results
results_names <- names(results)
for (i in seq_along(results)) {
  cat("Results for", results_names[i], ":\n")
  print(results[[i]])
  cat("\n\n")
}

# Optional: Save the model summaries to files
output_dir <- "output/DiD_Lag_Lead_R_Summaries/"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}
for (i in seq_along(results)) {
  writeLines(capture.output(results[[i]]), paste0(output_dir, "Summary_V2_", results_names[i], ".txt"))
}
