#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:18:54 2024

@author: paulsharratt
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from linearmodels import PanelOLS
import statsmodels.api as sm

# target & outout directories
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
output_directory = os.path.join(target_directory, "output/DiD_PanelOLS_summaries")

# Change the current working directory
os.chdir(target_directory)

# Load the data
trimmed_did_data = pd.read_excel("data/DiD/trimmed_did_dataset.xlsx")

# Set the MultiIndex for the panel data structure
trimmed_did_data.set_index(['org_name', 'time_period'], inplace=True)

# Metrics to be transformed
metrics = [
    'running_total_open_issues',
    'release_count',
    'unique_contributors',
    'avg_commits_per_contributor',
    'average_closure_days'
]

# Applying log transformation to metrics
for metric in metrics:
    trimmed_did_data[f'log_{metric}'] = np.log1p(trimmed_did_data[metric])

# Choose a dependent variable from the transformed metrics
dependent_var = 'log_running_total_open_issues'

# Define independent variables: Include 'treated' and any other relevant controls
exog_vars = ['treated']  # Add more control variables if necessary
exog = sm.add_constant(trimmed_did_data[exog_vars])  # Adds a constant term to the predictors

# Setup the PanelOLS model: including entity effects and time effects
mod = PanelOLS(trimmed_did_data[dependent_var], exog, entity_effects=True, time_effects=True)

# Fit the model with clustered standard errors
res = mod.fit(cov_type='clustered', cluster_entity=True)

# Output the results
print(res)

summary_str = str(res.summary)

# Save to a text file
with open('PanelOLS_Results_Summary.txt', 'w') as file:
    file.write(summary_str)

# Assuming the treatment effect is directly estimated (coefficient of 'treated')
treatment_effect = res.params['treated']
conf_low, conf_high = res.conf_int().loc['treated']

# Plotting
plt.figure(figsize=(8, 4))
sns.barplot(x=['Treatment Effect'], y=[treatment_effect])
plt.errorbar(x=['Treatment Effect'], y=[treatment_effect], yerr=[[treatment_effect - conf_low], [conf_high - treatment_effect]], fmt='o', color='red')
plt.title('Estimated Treatment Effect with 95% Confidence Interval')
plt.ylabel('Log Scale Effect Size')
plt.show()

# Function to run PanelOLS and save summaries
def run_and_save_panel_ols(dependent_var, data, exog_vars):
    exog = sm.add_constant(data[exog_vars])  # Adds a constant term to the predictors
    mod = PanelOLS(data[dependent_var], exog, entity_effects=True, time_effects=True)
    res = mod.fit(cov_type='clustered', cluster_entity=True)

    # Convert summary to string
    summary_str = str(res.summary)

    # Define file path
    summary_file_path = os.path.join(output_directory, f'PanelOLS_Results_Summary_{dependent_var}.txt')

    # Save to a text file
    with open(summary_file_path, 'w') as file:
        file.write(summary_str)
    
    print(f"Results for {dependent_var} saved to {summary_file_path}")

