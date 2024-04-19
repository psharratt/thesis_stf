#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:29:45 2024

@author: paulsharratt
"""


import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Define the target directory and file path
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
file_path = target_directory + 'data/processed/treatment_group_final.xlsx'

# Load the Excel file containing the organization names
treatment_df = pd.read_excel(file_path)
treatment_df['start_date'] = pd.to_datetime(treatment_df['start_date'])
treatment_df['end_date'] = pd.to_datetime(treatment_df['end_date'])


# If using a global start date based on the earliest project data available
global_start_date = pd.to_datetime('2019-01-01')  # You might choose '2019-01-01' or another relevant date

# Calculate the time period as the number of months from the global start date to each project's start date
treatment_df['time_period'] = (treatment_df['start_date'] - global_start_date).dt.days // 30

# Define the current date for ongoing analysis; adjust as necessary to align with your data's latest date
current_date = pd.to_datetime('today')  # or replace 'today' with the specific cut-off date you're analyzing

# Create the treated indicator based on whether the date falls within the treatment window
treatment_df['treated'] = treatment_df.apply(lambda x: 1 if x['start_date'] <= current_date <= x['end_date'] else 0, axis=1)


# Save the updated DataFrame to a new Excel file
updated_file_path = 'thesis_stf/data/processed/updated_treatment_group_final.xlsx'
treatment_df.to_excel(updated_file_path, index=False)








# Assume 'treatment_df' is your DataFrame with projects ending by 2023
# 'treated' is a binary indicator where 1 indicates post-treatment period and 0 pre-treatment.
# 'time' should be a continuous or categorical variable indicating time periods or specific dates.
# Note: Ensure that 'treated' and 'time' columns are correctly defined in your DataFrame

# Calculating the duration in days as a control variable
treatment_df['duration_days'] = (treatment_df['end_date'] - treatment_df['start_date']).dt.days

# Example of a fixed effects model
model = smf.ols('outcome_metric ~ treated * time + duration_days + C(org)', data=treatment_df)
results = model.fit(cov_type='cluster', cov_kwds={'groups': treatment_df['org']})
print(results.summary())






