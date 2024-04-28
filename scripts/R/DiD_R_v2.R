library(fixest)
library(readxl)
library(dplyr)
library(ggplot2)


# Assuming your data frame is named df
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

data <- read_xlsx("data/DiD/final_did_dataset_log_transformed_v3.xlsx")

data = unique(data)

data$active_repositories[is.na(data$active_repositories)] <- 0
data$contributors[is.na(data$contributors)] <- 0
data$release_count[is.na(data$release_count)] <- 0
data$running_total_open_issues[is.na(data$running_total_open_issues)] <- 0

# Ensure 'time_period' is treated as a factor if not already
data$time_period <- as.factor(data$time_period)
data$org_name <- as.factor(data$org_name)

data_cleaned <- data %>% 
  group_by(time_period, org_name) %>%
  summarise(across(everything(), ~mean(.x, na.rm = TRUE)), .groups = 'drop')


# Assuming 'treated' is already in the correct format
results <- list()

for (dep_var in c("log_contributors", "log_release_count", "log_running_total_open_issues",
                  "log_avg_commits_per_contributor", "log_average_closure_days")) {
  # Dynamically build formula with interaction and fixed effects
  formula <- as.formula(paste(dep_var, "~ treated * time_period | org_name + time_period", sep = ""))
  
  # Fit the model
  model <- feols(formula, data = data_cleaned)
  # Store the summary
  results[[dep_var]] <- summary(model)
}

# Display the results
print(results)


# Aggregating data by treatment status and time period for each metric
aggregated_data <- data_cleaned %>%
  group_by(treated, time_period) %>%
  summarise(
    mean_log_release_count = mean(log_release_count, na.rm = TRUE),
    mean_log_running_total_open_issues = mean(log_running_total_open_issues, na.rm = TRUE),
    mean_log_avg_commits_per_contributor = mean(log_avg_commits_per_contributor, na.rm = TRUE),
    mean_log_average_closure_days = mean(log_average_closure_days, na.rm = TRUE),
    .groups = 'drop'
  )

# Plotting time-series for log_release_count
ggplot(aggregated_data, aes(x = time_period, y = mean_log_release_count, color = as.factor(treated), group = as.factor(treated))) +
  geom_line() +
  labs(title = "Trend in Log of Release Count Over Time", x = "Time Period", y = "Log of Release Count") +
  theme_minimal() +
  geom_vline(xintercept = as.numeric(as.Date("2023-01-01")), linetype = "dashed", color = "red")

# Repeat similar plots for other metrics by changing 'y' and titles appropriately.


# Calculate differences for log_release_count
diff_log_release_count <- aggregated_data %>%
  filter(treated == 1) %>%
  mutate(difference_release_count = mean_log_release_count - lead(mean_log_release_count))

# Plotting difference plot for log_release_count
ggplot(diff_log_release_count, aes(x = time_period, y = difference_release_count, group = 1)) +
  geom_line() +
  labs(title = "Difference-in-Differences for Log of Release Count", x = "Time Period", y = "Difference (Treated - Control)") +
  theme_minimal()

# Repeat similar calculations and plots for other metrics.
