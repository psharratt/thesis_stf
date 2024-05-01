# Packages
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

# Set WD
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

# Iterate list and plot using coefplot
for (i in seq_along(model_list)) {
    # Extracting the name of the dependent variable
    dep_var_name <- names(model_list)[i]
    
    # Title dictionary
    plot_title <- titles_dict[dep_var_name]
    
    #  coefficient plot with the lookup title
    p <- coefplot(model_list[[i]],
                  ci_level = 0.95, # Confidence interval level
                  main = plot_title, # Use the title from the dictionary
                  xlab = "Terms",
                  ylab = "Estimates",
                  cex = 0.7,
                  lab.cex = 0.7,
                  grid = TRUE,
                  zero = TRUE)
  
  # output file name for  plot
  plot_filename <- paste0(output_dir, "/Coefplot_", dep_var_name, ".png")
  
  # Save to a PNG file
  ggsave(plot_filename, plot = p, width = 10, height = 8)
}


# LaTeX table
screenreg_list <- lapply(model_list, screenreg)
htmlreg_list <- lapply(model_list, htmlreg)

# combingin the tables into one
combined_screenreg <- do.call("rbind", screenreg_list)
combined_htmlreg <- do.call("rbind", htmlreg_list)

# Display the combined table in the R console
print(combined_screenreg)

combined_texreg <- texreg(model_list, caption = "Combined Summary Statistics for All Models")

# Saving LaTeX table to a file
writeLines(as.character(combined_texreg), "output/DiD_main_summaries/Combined_Summary_Statistics.tex")


# Saving the final cleaned and analyzed dataset
if (!requireNamespace("writexl", quietly = TRUE)) {
  install.packages("writexl")
}
library(writexl)
write_xlsx(did_data, path = "data/DiD/FINAL_TRIMMED_DATASET_SAVED.xlsx")










