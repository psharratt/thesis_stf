# Load necessary packages
if (!requireNamespace("fixest", quietly = TRUE)) install.packages("fixest")
if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")
if (!requireNamespace("writexl", quietly = TRUE)) install.packages("writexl")
if (!requireNamespace("lmtest", quietly = TRUE)) install.packages("lmtest")
if (!requireNamespace("broom", quietly = TRUE)) install.packages("broom")
if (!requireNamespace("knitr", quietly = TRUE)) install.packages("knitr")
if (!requireNamespace("kableExtra", quietly = TRUE)) install.packages("kableExtra")
if (!requireNamespace("texreg", quietly = TRUE)) install.packages("texreg")


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
library(lubridate)

# Set the working directory and data path
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")
data_path <- "FINAL_TRIMMED_DATASET.xlsx"
did_data <- read_xlsx(data_path)

# Data cleaning and preparation
did_data <- did_data %>%
  filter(!duplicated(did_data[c("time_period", "org_name")])) %>%
  mutate(
    time_period = as.Date(time_period),
    month_treated = as.Date(as.character(month_treated)),
    post = as.integer(time_period >= month_treated),
    time_period = as.factor(time_period),
    org_name = as.factor(org_name)
  ) 

# Brute forcing NAs into 'post'
did_data$post[is.na(did_data$post)] <- 0

# Dependent variables to analyze
dependent_vars <- c("log_contributors", "log_release_count", "log_running_total_open_issues",
                    "log_avg_commits_per_contributor", "log_average_closure_days")

titles_dict <- c(log_contributors = "Effects on Log Contributors",
                 log_release_count = "Effects on Log Release Count",
                 log_running_total_open_issues = "Effects on Log Running Total Open Issues",
                 log_avg_commits_per_contributor = "Effects on Log Average Commits Per Contributor",
                 log_average_closure_days = "Effects on Log Average Closure Days")


# Control variables 
control_vars <- c("age", "active_repositories")
control_vars_str <- paste(control_vars, collapse = " + ")

# NAs check in the control and dependent variables
na_check <- sapply(did_data[c(dependent_vars, control_vars, "treated", "post")], function(x) sum(is.na(x)))


did_data$rel_month <- round(interval(did_data$month_treated, did_data$time_period) / months(1))

# DiD setup
results <- list()
for (dep_var in dependent_vars) {
  formula_str <- paste(dep_var, "~ treated * post +", control_vars_str, "| org_name + time_period")
  model <- feols(as.formula(formula_str), data = did_data)
  results[[dep_var]] <- summary(model)
  predictions <- predict(model, newdata = did_data, type = "response")
  did_data[[paste("pred", dep_var, sep = "_")]] <- predictions
}

# Output and save results
results_names <- names(results)
output_dir <- "output/DiD_main_summaries/"


for (i in seq_along(results)) {
  cat("Results for", results_names[i], ":\n")
  print(results[[i]])
  cat("\n\n")
  writeLines(capture.output(results[[i]]), paste0(output_dir, "Summary_FINAL_", results_names[i], ".txt"))
}


model_list <- results # If 'results' already contains the model objects, no need for lapply

# Iterate through the list and plot using coefplot
for (i in seq_along(model_list)) {
    # Extract the name of the dependent variable
    dep_var_name <- names(model_list)[i]
    
    # Lookup the title using the dictionary
    plot_title <- titles_dict[dep_var_name]
    
    # Create the coefficient plot with the lookup title
    p <- coefplot(model_list[[i]],
                  ci_level = 0.95, # Confidence interval level
                  main = plot_title, # Use the title from the dictionary
                  xlab = "Terms",
                  ylab = "Estimates",
                  cex = 0.7,
                  lab.cex = 0.7,
                  grid = TRUE,
                  zero = TRUE)
  
  # Define the output filename for the plot
  plot_filename <- paste0(output_dir, "/Coefplot_", dep_var_name, ".png")
  
  # Save the plot to a PNG file
  ggsave(plot_filename, plot = p, width = 10, height = 8)
}


# Create LaTeX or HTML formatted tables for each model and combine them into one table
screenreg_list <- lapply(model_list, screenreg)
htmlreg_list <- lapply(model_list, htmlreg)

# Combine the tables into one
combined_screenreg <- do.call("rbind", screenreg_list)
combined_htmlreg <- do.call("rbind", htmlreg_list)

# Display the combined table in the R console
print(combined_screenreg)


# Assuming your models are stored in a list called model_list

# Create LaTeX formatted table for all models
combined_texreg <- texreg(model_list, caption = "Combined Summary Statistics for All Models")

# Save the LaTeX table to a file
writeLines(as.character(combined_texreg), "output/DiD_main_summaries/Combined_Summary_Statistics.tex")




#####



# Save the final cleaned and analyzed dataset
if (!requireNamespace("writexl", quietly = TRUE)) {
  install.packages("writexl")
}
library(writexl)
write_xlsx(did_data, path = "data/DiD/FINAL_TRIMMED_DATASET_SAVED.xlsx")






# Create tidy summaries for each model
tidy_results <- lapply(results, broom::tidy)

# Create a list to store formatted tables
formatted_tables <- list()

for (i in seq_along(tidy_results)) {
  # Format each summary into a nice table
  formatted_tables[[i]] <- kable(tidy_results[[i]], format = "html", caption = paste("Results for", results_names[i]))
  
  # Output tables to HTML files (can also be output to other formats like PDF)
  table_file <- paste0(output_dir, "Formatted_Summary_", results_names[i], ".html")
  writeLines(capture.output(formatted_tables[[i]]), table_file)
}

# Example of enhanced table formatting
enhanced_table <- kable(tidy_results[[1]], format = "html") %>%
  kable_styling(bootstrap_options = c("striped", "hover"))

# Create a LaTeX-formatted table
enhanced_latex_table <- kable(tidy_results[[1]], format = "latex", booktabs = TRUE, caption = "Summary Statistics Outcome Variables") %>%
  kable_styling(latex_options = c("striped", "scale_down"))

# View the LaTeX code (useful for copying into a LaTeX document)
print(enhanced_latex_table)

# Optionally, save the LaTeX code to a .tex file
writeLines(as.character(enhanced_latex_table), "output/DiD_main_summaries/Summary_Statistics_Log.tex")

# Tidying and combining results
combined_results <- lapply(results, broom::tidy) %>% 
  bind_rows(.id = "Model") %>%  # Combine all results into one data frame with an identifier
  mutate(Model = sub("pred_", "", Model))  # Optional: Clean up model names for presentation

# Adding a more descriptive identifier
combined_results$Model <- factor(combined_results$Model, levels = results_names)

# Create a LaTeX-formatted table with combined results
enhanced_latex_table <- kable(combined_results, format = "latex", booktabs = TRUE, 
                              caption = "Combined Summary Statistics for All Models") %>%
  kable_styling(latex_options = "scale_down", full_width = FALSE) %>%
  column_spec(1, bold = TRUE)  # Make model identifier bold

# View the LaTeX code
print(enhanced_latex_table)


# Saving the LaTeX table as a PDF
enhanced_latex_table <- kable(combined_results, "latex", booktabs = TRUE, 
                              caption = "Combined Summary Statistics for All Models") %>%
  kable_styling(latex_options = "scale_down", full_width = F) %>%
  column_spec(1, bold = TRUE)

# Save as PDF - ensure you have a LaTeX engine installed
kableExtra::save_kable(enhanced_latex_table, file = "output/DiD_main_summaries/Summary_Model_Statistics.pdf")





##### 



library(ggplot2)

# Filter for the outcome variable of interest
outcome_variable <- "log_average_closure_days"
filtered_data <- did_data %>%
  filter(!is.na({{outcome_variable}}))  # Filter out missing values for the outcome variable

# Calculate mean effect and standard error by relative month
mean_effect <- filtered_data %>%
  group_by(rel_month) %>%
  summarise(mean_effect = mean({{outcome_variable}}, na.rm = TRUE),
            se_effect = sd({{outcome_variable}}, na.rm = TRUE) / sqrt(n()))

# Plot the event study
ggplot(mean_effect, aes(x = rel_month, y = mean_effect)) +
  geom_point() +
  geom_errorbar(aes(ymin = mean_effect - 1.96 * se_effect, 
                    ymax = mean_effect + 1.96 * se_effect), 
                width = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(title = "Event Study: Impact of Treatment on Log Average Closure Days",
       x = "Relative Time to Treatment (Months)",
       y = "Mean Effect Size") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))  # Rotate x-axis labels if necessary


agg_outcome_variable <- aggregate(did_data$log_active_repositories, by=list(rel_month = did_data$rel_month), FUN = mean)
# might be useful for aggregate treatment effect...?

# Assuming agg_outcome_variable is your dataframe and that 'x' represents the mean effect

ggplot(agg_outcome_variable, aes(x = rel_month, y = x)) +
  geom_point() +
  geom_hline(yintercept = 0.2, linetype = "dashed") +
  labs(title = "Event Study: Impact of Treatment on Log Average Closure Days",
       x = "Relative Time to Treatment (Months)",
       y = "Mean Effect Size") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))  # Rotate x-axis labels if necessary


# Calculate the mean and standard error for each relative month
agg_outcome_variable <- did_data %>%
  group_by(rel_month) %>%
  summarise(
    mean_effect = mean(log_active_repositories, na.rm = TRUE),
    se_effect = sd(log_active_repositories, na.rm = TRUE) / sqrt(n())
  ) %>%
  ungroup()  # remove the grouping

# Now plot the means with error bars
ggplot(agg_outcome_variable, aes(x = rel_month, y = mean_effect)) +
  geom_point() +
  geom_line() +  # If you wish to connect the points
  geom_errorbar(aes(ymin = mean_effect - 1.96 * se_effect, 
                    ymax = mean_effect + 1.96 * se_effect), 
                width = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(title = "Event Study: Impact of Treatment on Log Active Repositories",
       x = "Relative Time to Treatment (Months)",
       y = "Mean Effect Size") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))  # Rotate x-axis labels if necessary








#####

"The empirical strategy employs an event study Difference-in-Differences approach with two-way fixed effects. This model allows for the estimation of dynamic treatment effects that may vary before and after the event of interest, accounting for time-varying treatments across entities. Each coefficient captures the treatment's impact at a specific point in time relative to the initiation of the treatment, while controlling for unobserved, time-invariant entity characteristics and common temporal shocks. The estimation results are presented in a tabular form showing the point estimates, standard errors, and corresponding levels of statistical significance for each time period. Additionally, a graphical illustration provides a clear visual representation of how the treatment effects evolve over time."

"In a standard two-way fixed effects Difference-in-Differences (DiD) setup, you typically don't get a separate coefficient for each period relative to the treatment if you use only a binary indicator for treatment and post-treatment period. Instead, you get a single coefficient for the interaction between the treatment indicator and the post-treatment period, which measures the average treatment effect after the treatment has been implemented.

However, in an event study framework within a DiD setup, especially with staggered adoption of the treatment (which can be estimated with a two-way fixed effects model), you can include separate dummy variables for each time period relative to the treatment event for each entity. These dummy variables interact with the treatment indicator to get separate coefficients for the effect of treatment at each point in time relative to the treatment.

To get these period-specific effects, your regression model needs to be set up to estimate coefficients for these period dummies. For instance:

# Assuming `rel_month` is a factor with levels indicating each period relative to treatment
# and `treated` is a binary treatment indicator.
model <- feols(outcome_variable ~ treated * as.factor(rel_month) | entity + time, data = did_data)


# Assuming `rel_month` is a factor with levels indicating each period relative to treatment
# and `treated` is a binary treatment indicator.
model <- feols(outcome_variable ~ treated * as.factor(rel_month) | entity + time, data = did_data)
This model would include interaction terms between treated and each level of rel_month (which should be converted from numeric to factor), allowing you to estimate the treatment effect for each period relative to the start of treatment.

Then, you can plot these estimated period-specific treatment effects and their confidence intervals over time to visually assess how the effect of the treatment evolves before and after the treatment event. This type of event study analysis is valuable for understanding the dynamic effects of policies or interventions when treatment timing varies across entities."
