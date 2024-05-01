

# Set the working directory and data path
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")
data_path <- "data/DiD/FINAL_TRIMMED_DATASET_SAVED.xlsx"
did_data <- read_xlsx(data_path)

library(ggplot2)
library(ggplot2)
library(dplyr)

did_data$time_period <- as.Date(did_data$time_period, format = "%Y-%m-%d")

# Plot of predicted and actual 
ggplot(did_data, aes(x = time_period)) +
  geom_line(aes(y = .data[[paste("pred", "log_contributors", sep = "_")]], color = "Predicted"), size = 1.2) +
  geom_line(aes(y = log_contributors, color = "Actual"), size = 1.2, linetype = "dashed") +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +  # Adjust date breaks and labels
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),  # Rotate x-axis labels
        plot.title = element_text(hjust = 0.5)) +  # Center the title
  labs(title = "Comparison of Actual vs. Predicted Log Contributors",
       x = "Time Period", y = "Log of Contributors",
       color = "Type") +
  scale_color_manual(values = c("Predicted" = "blue", "Actual" = "red"),
                     labels = c("Predicted", "Actual")) +
  guides(color = guide_legend(title = "Legend"))

