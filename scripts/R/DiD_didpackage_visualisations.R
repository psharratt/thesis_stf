if (!requireNamespace("did", quietly = TRUE)) install.packages("did")
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
if (!requireNamespace("dplyr", quietly = TRUE)) install.packages("dplyr")

library(did)
library(ggplot2)
library(dplyr)
library(lubridate)


# Set the working directory and data path
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")
data_path <- "data/DiD/FINAL_TRIMMED_DATASET_SAVED.xlsx"
did_data <- read_xlsx(data_path)


# https://tilburgsciencehub.com/topics/analyze/causal-inference/did/staggered-did/

# Convert 'time_period' to Date type if it represents specific dates
data <- did_data %>%
  mutate(
    time_period = ymd(time_period),  # Convert to Date if format is 'YYYY-MM-DD'
    treatment_start = year(month_treated) * 100 + month(month_treated)  # Create a numeric representation of treatment start
  )

data <- data %>%
  mutate(
    time_period = as.Date(time_period, format = "%Y-%m-%d"),  # Ensure correct date format
    numeric_time = as.numeric(format(time_period, "%Y%m"))    # Convert to a numeric format like YYYYMM
  )

# Ensure the 'treatment_start' variable is also numeric and appropriately calculated
data <- data %>%
  mutate(
    treatment_start = if_else(is.na(month_treated),  as.numeric(format(month_treated, "%Y%m")))  # Using '0' for never treated
  )

data <- data %>%
  mutate(
    org_id = as.numeric(as.factor(org_name))  # Convert org_name to a numeric factor
  )


# Assuming 'contributors' as the outcome variable and other settings from before
results <- att_gt(
  yname = "contributors",                 # Outcome variable
  tname = "numeric_time",                 # Numeric time variable
  idname = "org_id",                      # Updated ID variable, now numeric
  gname = "treatment_start",              # First treatment period variable, already numeric
  data = data,                            # Updated data
  xformla = ~ age + active_repositories,  # Including covariates
  control_group = "notyettreated",        # Control group specification
  allow_unbalanced_panel = TRUE           # If unbalanced panel data is allowed
)

# Check the results
summary(results)

# Optional: Plot the results if needed
library(ggplot2)
ggdid_plot <- ggplot(results) +
  labs(x = "Time Relative to Treatment", y = "Estimated ATT")
print(ggdid_plot)


