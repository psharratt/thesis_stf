library(dplyr)
library(fixest)
library(ggplot2)

'''
The key concern regarding collinearity would arise if you were to include both the log-transformed and the original (non-transformed) versions of these variables in the same regression model. This would indeed be problematic because the transformed and original variables would be highly correlated with each other, leading to multicollinearity. However, if you are only using the log-transformed variables in your model without their corresponding non-transformed versions, then collinearity should not be an issue simply because of the transformation. Its quite common to use log-transformed variables in regression models, particularly when dealing with skewed data or when you want to interpret the coefficients in terms of percentage changes (elasticities). If your model includes multiple log-transformed variables that are derived from the same underlying data (e.g., total pull requests and unique pull requests), there might still be a concern if the original variables were highly correlated. You would need to check the correlation between your log-transformed variables to ensure that they are not introducing collinearity into the model. If you find that the log-transformed variables are highly correlated, you may need to consider whether including all of them in the same model is necessary, or if it might be better to use a dimensionality reduction technique like Principal Component Analysis (PCA) before modeling. Since youre already considering PCA, this could be a good approach to distill the information from the correlated predictors into a smaller set of uncorrelated components.
'''

# Set the working directory (adjust if necessary)
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

# Load the dataset
data_path <- "data/DiD/final_did_dataset_log_transformed_v3.xlsx"
dataset <- read_excel(data_path)

# Directory for saving the output
output_dir <- "output/DiD_v2_PCA_function_Summaries"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Selecting only numeric columns for PCA, excluding the 'treated' variable and non-numeric variables
numeric_data <- dataset %>%
  select(where(is.numeric)) %>%
  mutate(across(everything(), ~ifelse(is.na(.), mean(., na.rm = TRUE), .)))

# Scaling the numeric data
numeric_data_scaled <- scale(numeric_data)

# Performing PCA on the scaled numeric data
pca_result <- prcomp(numeric_data_scaled, center = TRUE, scale. = TRUE)

# Extracting the first few principal components based on your decision
pc_data <- pca_result$x[, 1:5]  # Adjust the number of components as needed

# Merging principal components with necessary categorical variables and outcome variables from the original dataset
diagnosis_data <- dataset %>%
  select(treated, time_period, org_name, log_contributors, log_release_count, log_running_total_open_issues, log_avg_commits_per_contributor, log_average_closure_days) %>%
  mutate(treated = as.factor(treated),
         time_period = as.factor(time_period),
         org_name = as.factor(org_name)) %>%
  bind_cols(as.data.frame(pc_data))

# Creating the interaction term for treatment and time for the DiD model
diagnosis_data$treatment_time <- interaction(diagnosis_data$treated, diagnosis_data$time_period)

# Function to run DiD, summarize the model, plot coefficients, and save the plot
run_did_and_plot <- function(outcome_var, data, output_dir) {
  # Build the formula for the model dynamically
  formula <- as.formula(paste(outcome_var, "~ treatment_time + PC1 + PC2 + PC3 + PC4 + PC5 | org_name + time_period"))
  
  # Run the DiD analysis
  model <- feols(formula, data = data)
  
  # Generate the summary
  model_summary <- summary(model)
  
  # Extract coefficients for plotting
  coefs <- model_summary$coef.est
  cis <- model_summary$coef.ci
  terms <- rownames(coefs)
  
  # Create a dataframe for plotting
  plot_data <- data.frame(
    Term = terms,
    Estimate = coefs[, 1],
    CI_low = cis[, 1],
    CI_high = cis[, 2]
  )
  
  # Create the coefficient plot
  plot <- ggplot(plot_data, aes(x = Term, y = Estimate, ymin = CI_low, ymax = CI_high)) +
    geom_pointrange() +
    geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
    labs(title = paste("Estimated Coefficients for", outcome_var),
         y = "Coefficient Estimate",
         x = "")
  
  # Save the plot
  plot_file_path <- file.path(output_dir, paste("Coefficients_", outcome_var, ".pdf", sep = ""))
  ggsave(plot_file_path, plot, width = 10, height = 6)
  
  return(list(model_summary = model_summary, plot = plot))
}

# Apply the function to each outcome variable
outcome_vars <- c("log_contributors", "log_running_total_open_issues", "log_release_count", 
                  "log_avg_commits_per_contributor", "log_average_closure_days")

# Assuming diagnosis_data is your dataset and output_dir is your output directory
results <- lapply(outcome_vars, run_did_and_plot, data = diagnosis_data, output_dir = output_dir)

# Now results is a list of lists, each containing a model summary and a plot for each outcome variable
