# Load necessary packages
if (!requireNamespace("fixest", quietly = TRUE)) install.packages("fixest")
if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")
if (!requireNamespace("writexl", quietly = TRUE)) install.packages("writexl")
if (!requireNamespace("lmtest", quietly = TRUE)) install.packages("lmtest")
if (!requireNamespace("broom", quietly = TRUE)) install.packages("broom")
if (!requireNamespace("knitr", quietly = TRUE)) install.packages("knitr")
if (!requireNamespace("kableExtra", quietly = TRUE)) install.packages("kableExtra")
if (!requireNamespace("did2s", quietly = TRUE)) install.packages("did2s")

library(dplyr)
library(readxl)
library(lubridate)
library(fixest)
library(writexl)
library(lmtest)
library(ggplot2)
library(broom)
library(knitr)
library(kableExtra)
library(did2s)

# Set the working directory and data path
setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")
data_path <- "data/DiD/FINAL_TRIMMED_DATASET.xlsx"
did_data <- read_xlsx(data_path)

# Data cleaning and preparation
did_data <- did_data %>%
  mutate(
    time_period = as.Date(time_period),
    month_treated = as.Date(month_treated),
    year = as.factor(format(time_period, "%Y")),
    org_name = as.factor(org_name)
  ) %>%
  select(-`Unnamed: 0`)

# Brute forcing NAs into 'post' 
did_data$post <- ifelse(did_data$time_period >= did_data$month_treated, 1, 0)

# Calculate 'relative month to treatment' as the difference in months
did_data$month_treated <- as.Date(did_data$month_treated, format = "%Y-%m-%d")
did_data$time_period <- as.Date(did_data$time_period, format = "%Y-%m-%d")

did_data$rel_month <- round(interval(did_data$month_treated, did_data$time_period) / months(1))

# Saving dataset - THIS WILL NEED REVISION
output_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/FINAL_TRIMMED_DATASET.xlsx"

# Save the dataframe to Excel
write_xlsx(did_data, path = output_path)

# Confirm message
cat("Dataframe saved to:", output_path, "\n")

# Sort dataframe by 'month_treated'
did_data <- did_data %>% arrange(month_treated)

# Initialize a new column for batch IDs and assign the first batch ID
did_data$batch_id <- NA
did_data$batch_id[1] <- 1


# Creating a new dataframe without NAs in 'month_treated'
did_data_no_na <- did_data %>%
  filter(!is.na(month_treated))

# Or, if you prefer to overwrite the existing dataframe
did_data <- filter(did_data, !is.na(month_treated))
# Loop through the dataframe to assign batch numbers
current_batch_id <- 1
for (i in 2:nrow(did_data_no_na)) {
  if (!is.na(did_data_no_na$month_treated[i]) && difftime(did_data_no_na$month_treated[i], did_data_no_na$month_treated[i - 1], units = "weeks") <= 4) {
    did_data_no_na$batch_id[i] <- current_batch_id
  } else {
    current_batch_id <- current_batch_id + 1
    did_data_no_na$batch_id[i] <- current_batch_id
  }
}

# Review the distribution of batch IDs
table(did_data$batch_id)



selected_data <- did_data %>%
  select(org_name, month_treated, batch_id)

# View the first few rows to confirm the selection
head(selected_data)

did_data_no_na$org_id <- as.numeric(as.factor(did_data_no_na$org_name))
max_rel_month <- max(did_data_no_na$rel_month, na.rm = TRUE)
did_data_no_na$rel_month[is.na(did_data_no_na$rel_month)] <- max_rel_month + 1


library(did)

example_attgt <- att_gt(yname = "log_contributors",
                        tname = "rel_month",
                        idname = "org_id",
                        gname = "batch_id",
                        xformla = ~ age,
                        data = did_data_no_na,
                        control_group="notyettreated",
                        panel = FALSE
)

example_attgt <- att_gt(yname = "log_contributors",
                        tname = "rel_month",
                        idname = "org_id",
                        gname = "batch_id",
                        xformla = ~ 1,  # This uses only an intercept, testing if the issue lies with the predictors
                        data = did_data_no_na,
                        control_group="notyettreated",
                        panel = FALSE
)

summary(example_attgt)






# USEFUL GRAPHICS:


library(ggplot2)

# Aggregate the data as you've done
agg <- aggregate(did_data$log_active_repositories, by=list(g = did_data$batch_id, month = as.Date(did_data$time_period)), FUN = mean)

# Renaming the columns for clarity
names(agg) <- c("batch_id", "month", "mean_log_repositories")

# Split the data by batch_id for plotting
g1 <- agg[agg$batch_id == "1", ]
g2 <- agg[agg$batch_id == "2", ]
g3 <- agg[agg$batch_id == "3", ]
g4 <- agg[agg$batch_id == "4", ]
g5 <- agg[agg$batch_id == "5", ]

# Plotting the data using base R plotting functions
plot(g1$month, g1$mean_log_repositories, type = "n", xlim = range(agg$month), ylim = range(agg$mean_log_repositories, na.rm = TRUE),
     main = "Data-generating Process", xlab = "Month", ylab = "Mean Active Repositories", xaxt='n')
abline(v = as.Date(c("2023-06-15", "2023-08-28")), lty = 2)  # Adjusted dates for mid-2023 and late August 2023
axis(1, at = g1$month, labels = format(g1$month, "%Y-%m"), cex.axis = 0.7, las=2)  # Rotate axis labels for clarity

# More distinctive colors
colors <- c("#FF6347", "#4682B4", "#32CD32", "#FFD700", "#6A5ACD")

# Draw lines for each group
lines(g1$month, g1$mean_log_repositories, col = colors[1], type = "b", pch = 17)
lines(g2$month, g2$mean_log_repositories, col = colors[2], type = "b", pch = 16)
lines(g3$month, g3$mean_log_repositories, col = colors[3], type = "b", pch = 18)
lines(g4$month, g4$mean_log_repositories, col = colors[4], type = "b", pch = 19)
lines(g5$month, g5$mean_log_repositories, col = colors[5], type = "b", pch = 20)

# Adding a legend with more distinctive colors
legend("topright", col = colors, 
       pch = c(17, 16, 18, 19, 20), legend = c("Batch 1", "Batch 2", "Batch 3", "Batch 4", "Batch 5"))


# Filter data for Batch 4
batch_4_data <- did_data %>%
  filter(batch_id == 4) %>%
  arrange(month_treated)  # Ensure data is sorted by treatment date

# Find the first treatment date in Batch 4
first_treatment_date_batch_4 <- batch_4_data$month_treated[1]

# Print the first treatment date for Batch 4
print(first_treatment_date_batch_4)

