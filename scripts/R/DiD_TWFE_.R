library(data.table)
library(readxl)
library(fixest)
library(lubridate)


setwd("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf")

# Load your data
dat <- read_xlsx("data/DiD/FINAL_TRIMMED_DATASET.xlsx")


# Convert data.frame to data.table
setDT(dat)

# dat[, treated := ifelse(is.na(month_treated), 0, 1)]

# Create the time_to_treatment variable
dat[, time_to_treat := ifelse(treated == 1, month(time_period) - month(month_treated), 0)]

# Add control variables properly to the regression
control_vars <- c("age", "active_repositories", "unique_pull_requests")

# Define the model with fixed effects and clustering
mod_twfe <- feols(log_contributors ~ i(time_to_treat, treated, ref = -1) + 
                    age + active_repositories + unique_pull_requests | 
                    org_name + year(time_period),  # Ensure to extract year from the date if time_period is a date
                  cluster = ~ org_name, 
                  data = dat)

# Print the summary of the model
summary(mod_twfe)


iplot(mod_twfe, 
      xlab = 'Time to treatment',
      main = 'Event study: Staggered treatment (TWFE)')


# As earlier mentioned, the standard TWFE approach to event studies is subject to various problems in the presence of staggered treatment rollout. Fortunately, fixest provides the sunab() convenience function for estimating the aggregated “cohort” method proposed by Sun and Abraham (2020). In the below example, the only material change is to swap out the i() interaction with the sunab() equivalent.


dat[, treated_month := ifelse(treated==0, 5, month_treated)]

dat$month_treated <- floor_date(dat$month_treated, "month")


# Now, use the 'treatment_time' variable directly with sunab() 
# Note that we'll use the 'month_time_period' you've created as the second argument for sunab() 
# which should be the time of the observation in months
mod_sa <- feols(contributors ~ sunab(month_treated, time_period) + 
                  age + active_repositories + unique_pull_requests | 
                  org_name + month(time_period),  # Fixed effects by year, consider adding month if necessary
                cluster = ~ org_name,          # Clustered SEs
                data = dat)

# Plotting the Sun and Abraham model results alongside the TWFE model results
library(ggplot2)
iplot(list(mod_twfe, mod_sa), sep = 0.5, ref.line = -1,
      xlab = 'Months to treatment',
      main = 'Event study: Staggered treatment')
legend("bottomleft", col = c(1, 2), pch = c(20, 17), 
       legend = c("TWFE", "Sun & Abraham (2020)"))
