
library(plm)
library(ggplot2)


setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

data <- read_xlsx("data/DiD/FINAL_TRIMMED_DATASET_SAVED.xlsx")

data$time_period <- as.Date(data$time_period)

pdata <- pdata.frame(data, index = c("org_name", "time_period"))

summary(pdata)

# Filtering data for the organization 'curl' as an example
curl_data <- as.data.frame(subset(pdata, org_name == "curl"))

# Plotting histogram and density plot for log_active_repositories
ggplot(curl_data, aes(x = log_active_repositories)) +
  geom_histogram(aes(y = ..density..), bins = 30, fill = "blue", alpha = 0.7) +
  geom_density(alpha = 0.2, fill = "#FF6666") +
  ggtitle("Histogram and Density Plot for 'curl'")

# Generating a Q-Q Plot for log_active_repositories
qqnorm(curl_data$log_active_repositories, main = "Q-Q Plot for 'curl'")
qqline(curl_data$log_active_repositories, col = "steelblue", lwd = 2)



# Melting the dataset to long format
melted_data <- melt(pdata, id.vars = c("org_name", "time_period"))

# Variables of interest
variables <- c("log_contributors", "log_release_count", "log_avg_commits_per_contributor", "log_average_closure_days")

# Filtering melted data to include only variables of interest
filtered_data <- melted_data[melted_data$variable %in% variables, ]

# Plotting histograms and density plots for each variable
ggplot(filtered_data, aes(x = value)) +
  geom_histogram(aes(y = ..density..), bins = 30, fill = "blue", alpha = 0.7) +
  geom_density(alpha = 0.2, fill = "#FF6666") +
  facet_wrap(~ variable, scales = "free") +
  ggtitle("Histogram and Density Plots for Selected Variables")



# Converting pdata to a standard data frame 
data <- as.data.frame(pdata)

# Define the organizations and variables
organizations <- unique(data$org_name)
variables <- c("log_contributors", "log_release_count", "log_avg_commits_per_contributor", "log_average_closure_days")

# Initialize a list to store results
results <- list()

# Loop through each organization
for (org in organizations) {
  # Subset data for the organization
  org_data <- data[data$org_name == org, ]
  
  # Loop through each variable and perform the Shapiro-Wilk test
  for (var in variables) {
    # Check if the variable has only one unique value or if all values are NA
    if (length(unique(org_data[[var]][!is.na(org_data[[var]])])) < 2) {
      results[[paste(org, var, sep = "_")]] <- list(W = NA, p_value = NA)
    } else {
      test_result <- shapiro.test(org_data[[var]][!is.na(org_data[[var]])])
      results[[paste(org, var, sep = "_")]] <- list(
        W = test_result$statistic,
        p_value = test_result$p.value
      )
    }
  }
}

# Convert results to a more accessible format like a data frame
results_df <- data.frame(
  Organization = character(),
  Variable = character(),
  W = numeric(),
  P_Value = numeric(),
  stringsAsFactors = FALSE
)

for (key in names(results)) {
  entry <- results[[key]]
  org_var_split <- unlist(strsplit(key, "_", fixed = TRUE))
  organization <- org_var_split[1]
  variable <- paste(org_var_split[2:length(org_var_split)], collapse = '_') # Reconstructing the variable name
  
  results_df <- rbind(results_df, data.frame(
    Organization = organization,
    Variable = variable,
    W = entry$W,
    P_Value = entry$p_value
  ))
}

# View results
print(results_df)

