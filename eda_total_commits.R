# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

library(tidyverse)
library(readr)
library(dplyr)
library(ggplot2)

# Load dataset
commits_data <- read_csv("data/raw/augur/total_commits_org_desc.csv") # Adjust path as necessary

# Basic Descriptive Statistics
summary_stats <- commits_data %>%
  summarise(
    Mean = mean(total_commits, na.rm = TRUE),
    Median = median(total_commits, na.rm = TRUE),
    SD = sd(total_commits, na.rm = TRUE),
    Min = min(total_commits, na.rm = TRUE),
    Max = max(total_commits, na.rm = TRUE)
  )

# Print summary statistics to console
print(summary_stats)

# Creating a bar plot
bar_plot <- ggplot(commits_data, aes(x = reorder(org_name, total_commits), y = total_commits)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  theme_minimal() +
  labs(title = "Total Commits per Organization", x = "Organization", y = "Total Commits") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) # Rotate x-axis labels for better readability

# Display the plot
print(bar_plot)

# Define the file path for the output graph
output_file_path <- "output/graphs/histogram_of_total_commits.png"

# Save the histogram plot
ggsave(output_file_path, plot = bar_plot, width = 10, height = 8, dpi = 300)
