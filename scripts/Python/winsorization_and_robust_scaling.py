#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:20:43 2024

@author: paulsharratt
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler

#https://www.publichealth.columbia.edu/research/population-health-methods/difference-difference-estimation

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

os.chdir(target_directory)






# Load the data
trimmed_did_data = pd.read_excel("data/DiD/FINAL_TRIMMED_DATASET.xlsx")

metrics = [
                'log_active_repositories',
                'log_contributors',
                'log_release_count',
                'log_running_total_open_issues', 
                'log_unique_contributors',
                'log_avg_commits_per_contributor',
                'log_average_closure_days', 
                'log_unique_pull_requests', 
                'log_open_pull_requests',
                'log_closed_pull_requests',
]


# Mapping of metric codes to full names
metric_names = {
    'log_active_repositories': 'Log Active Repositories',
    'log_contributors': 'Log Contributors',
    'log_release_count': 'Log Release Count',
    'log_running_total_open_issues': 'Log Running Total Open Issues',
    'log_unique_contributors': 'Log Unique Contributors',
    'log_avg_commits_per_contributor': 'Log Average Commits per Contributor',
    'log_average_closure_days': 'Log Average Closure Days',
    'log_unique_pull_requests': 'Log Unique Pull Requests',
    'log_open_pull_requests': 'Log Open Pull Requests',
    'log_closed_pull_requests': 'Log Closed Pull Requests',
}



# Visualize the transformed distributions
plt.figure(figsize=(20, 15))
plt.suptitle('Log Transformed Distributions', fontsize=16, y=0.98)  # Adjust 'y' for vertical position

# Iterate over metrics for plotting
for i, metric in enumerate(metrics, 1):
    ax = plt.subplot(3, 4, i)  # Adjust subplot grid as needed
    sns.histplot(trimmed_did_data[f'{metric}'], kde=True)
    ax.set_title(metric_names[metric], pad=20)  # Use friendly names for titles
    plt.xlabel(metric_names[metric])  # Set x-axis label to the full metric name
    plt.ylabel('Frequency')  # Optional: set y-axis label

plt.tight_layout(pad=3.0)
plt.subplots_adjust(top=0.92)  # Adjust the top margin to give space for the suptitle
plt.show()

plt.savefig('output/plots/log_transformed_distributions_FINAL.jpeg', dpi=600)  # Adjust the filename and dpi as needed
plt.show()



# Winsoring certain variables 

# List of variables to Winsorize
variables_to_winsorize = ['log_active_repositories', 'log_contributors', 'log_release_count', 'log_open_pull_requests', 'log_running_total_open_issues']

# Winsorize selected variables
for var in variables_to_winsorize:
    threshold = 0.95  # Set the threshold (percentile) for Winsorization (adjust as needed)
    upper_percentile = trimmed_did_data[var].quantile(threshold)
    lower_percentile = trimmed_did_data[var].quantile(0.05)
    trimmed_did_data[f'{var}_winsorized'] = trimmed_did_data[var].clip(lower=lower_percentile, upper=upper_percentile)


# Check the new DataFrame with log-transformed and Winsorized variables
print(trimmed_did_data.head())

metrics_win = [
                'log_active_repositories_winsorized',
                'log_contributors_winsorized',
                'log_release_count_winsorized',
                'log_running_total_open_issues_winsorized', 
                'log_unique_contributors',
                'log_avg_commits_per_contributor',
                'log_average_closure_days', 
                'log_unique_pull_requests', 
                'log_open_pull_requests_winsorized',
                'log_closed_pull_requests',
]


metric_names_win = {
    'log_active_repositories_winsorized': 'Log Active Repositories Winsorized',
    'log_contributors_winsorized': 'Log Contributors Winsorized',
    'log_release_count_winsorized': 'Log Release Count Winsorized',
    'log_running_total_open_issues_winsorized': 'Log Running Total Open Issues',
    'log_unique_contributors': 'Log Unique Contributors',
    'log_avg_commits_per_contributor': 'Log Average Commits per Contributor',
    'log_average_closure_days': 'Log Average Closure Days',
    'log_unique_pull_requests': 'Log Unique Pull Requests',
    'log_open_pull_requests_winsorized': 'Log Open Pull Requests Winsorized',
    'log_closed_pull_requests': 'Log Closed Pull Requests',
}

# Visualize the transformed and winsorized distributions
plt.figure(figsize=(20, 15))
plt.suptitle('Log Transformed & Winsorized Distributions', fontsize=16, y=0.98)  # Adjust 'y' for vertical position

# Iterate over metrics for plotting
for i, metric in enumerate(metrics_win, 1):
    ax = plt.subplot(3, 4, i)  # Adjust subplot grid as needed
    sns.histplot(trimmed_did_data[f'{metric}'], kde=True)
    ax.set_title(metric_names_win[metric], pad=20)  # Use friendly names for titles
    plt.xlabel(metric_names_win[metric])  # Set x-axis label to the full metric name
    plt.ylabel('Frequency')  # Optional: set y-axis label

plt.tight_layout(pad=3.0)
plt.subplots_adjust(top=0.92)  # Adjust the top margin to give space for the suptitle
plt.show()


# Select columns to be scaled
columns_to_scale = [
                'log_active_repositories_winsorized',
                'log_contributors_winsorized',
                'log_release_count_winsorized',
                'log_running_total_open_issues_winsorized', 
                'log_unique_contributors',
                'log_avg_commits_per_contributor',
                'log_average_closure_days', 
                'log_unique_pull_requests', 
                'log_open_pull_requests_winsorized',
                'log_closed_pull_requests',
]


metric_names_win = {
    'log_active_repositories_winsorized': 'Log Active Repositories Winsorized',
    'log_contributors_winsorized': 'Log Contributors Winsorized',
    'log_release_count_winsorized': 'Log Release Count Winsorized',
    'log_running_total_open_issues_winsorized': 'Log Running Total Open Issues',
    'log_unique_contributors': 'Log Unique Contributors',
    'log_avg_commits_per_contributor': 'Log Average Commits per Contributor',
    'log_average_closure_days': 'Log Average Closure Days',
    'log_unique_pull_requests': 'Log Unique Pull Requests',
    'log_open_pull_requests_winsorized': 'Log Open Pull Requests Winsorized',
    'log_closed_pull_requests': 'Log Closed Pull Requests',
}

# Apply robust scaling
robust_scaler = RobustScaler()
robust_scaled_data = robust_scaler.fit_transform(trimmed_did_data[columns_to_scale])

# Convert the scaled data back to a DataFrame
robust_scaled_df = pd.DataFrame(robust_scaled_data, columns=columns_to_scale)

# Plot the robust scaled distributions
plt.figure(figsize=(20, 15))
plt.suptitle('Robustly Scaled Distributions', fontsize=16, y=0.98)

# Iterate over columns for plotting
for i, column in enumerate(columns_to_scale, 1):
    ax = plt.subplot(3, 4, i)
    sns.histplot(robust_scaled_df[column], kde=True)
    ax.set_title(column, pad=20)
    ax.set_title(metric_names_win[metric], pad=20)  # Use friendly names for titles
    plt.xlabel(metric_names_win[metric])  # Set x-axis label to the full metric name
    plt.ylabel('Frequency')

plt.tight_layout(pad=3.0)
plt.subplots_adjust(top=0.92)
plt.show()



