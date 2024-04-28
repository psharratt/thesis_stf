# Load necessary libraries
library(fixest)
library(readxl)
library(dplyr)
library(writexl)
library(lmtest)
library(ggplot2)
library(broom)
library(knitr)
library(kableExtra)
library(texreg)

# Read and prepare data
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")
data_path <- "FINAL_TRIMMED_DATASET.xlsx"

did_data <- read_xlsx(data_path) %>%
  mutate(
    time_period = as.factor(as.Date(time_period)),
    month_treated = as.Date(as.character(month_treated)),
    post = as.integer(time_period >= month_treated),
    org_name = as.factor(org_name),
    post = ifelse(is.na(post), 0, post) # Replace NAs with 0
  )

# Define variables
dependent_vars <- c("log_contributors", "log_release_count", "log_running_total_open_issues",
                    "log_avg_commits_per_contributor", "log_average_closure_days")

control_vars <- c("age", "active_repositories")

control_vars_str <- paste(control_vars, collapse = " + ")

# Check for NAs
na_check <- sapply(did_data[c(dependent_vars, control_vars, "treated", "post")], function(x) sum(is.na(x)))
print(na_check)

# Run models
output_dir <- "output/DiD_Summaries"
dir.create(output_dir, recursive = TRUE)
results <- list()

for (dep_var in dependent_vars) {
  formula <- as.formula(paste(dep_var, "~ treated * post +", control_vars_str, "| org_name + time_period"))
  model <- feols(formula, data = did_data)
  results[[dep_var]] <- model
  cat("Results for", dep_var, ":\n")
  screenreg(model)
  cat("\n\n")
}

# Save model summaries
for (dep_var in dependent_vars) {
  summary_file <- paste0(output_dir, "Summary_DONE_", dep_var, ".txt")
  writeLines(capture.output(summary(results[[dep_var]])), summary_file)
}

# Extract model objects for texreg
model_list <- lapply(results, function(x) x)
texreg_table <- screenreg(model_list)
writeLines(texreg_table, paste0(output_dir, "regression_table_DONE.tex"))

# Plot coefficients with 95% CI
plot_coefficients <- function(model, dep_var) {
  coef_data <- tidy(model, conf.int = TRUE) # Ensure confidence intervals are calculated
  ggplot(coef_data, aes(x = term, y = estimate, ymin = conf.low, ymax = conf.high)) +
    geom_pointrange() +
    geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
    labs(title = paste("Treatment Effects for", dep_var),
         x = "Terms", y = "Point Estimate (with 95% CI)") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# Apply the plotting function to each model and save plots
for (dep_var in dependent_vars) {
  plot_file <- paste0(output_dir, "Coefficients_Plot_DONE", dep_var, ".png")
  g <- plot_coefficients(results[[dep_var]], dep_var)
  ggsave(plot_file, plot = g, width = 10, height = 8)
}



model_list <- results # If 'results' already contains the model objects, no need for lapply

# Ensure the directory exists
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Iterate through the list and plot using coefplot
for (i in seq_along(model_list)) {
  # Extract the name of the dependent variable for the title
  dep_var_name <- names(model_list)[i]
  
  # Create the coefficient plot
  p <- coefplot(model_list[[i]],
                ci_level = 0.95, # Confidence interval level
                main = paste("Effects on", dep_var_name),
                xlab = "Terms",
                ylab = "Estimates",
                cex = 0.7,
                lab.cex = 0.7,
                grid = TRUE,
                zero = TRUE)
  
  # Define the output filename for the plot
  plot_filename <- paste0(output_dir, "Coefplot_", dep_var_name, ".pdf")
  
  # Save the plot to a PDF file
  pdf(plot_filename)
  print(p)
  dev.off() # Remember to close the pdf device
}


# Save final dataset
write_xlsx(did_data, path = "FINAL_TRIMMED_DATASET_SAVED.xlsx")




