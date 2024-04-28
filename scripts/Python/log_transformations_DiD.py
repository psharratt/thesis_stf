#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:17:46 2024

@author: paulsharratt
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

# Load the data
trimmed_did_data = pd.read_excel("data/DiD/trimmed_did_data_v2.xlsx")

metrics = [
                'active_repositories',
                'contributors',
                'release_count',
                'running_total_open_issues', 
                'unique_contributors',
                'avg_commits_per_contributor',
                'average_closure_days', 
                'unique_pull_requests', 
                'open_pull_requests',
                'closed_pull_requests',
]


# Mapping of metric codes to full names
metric_names = {
    'active_repositories': 'Active Repositories',
    'contributors': 'Contributors',
    'release_count': 'Release Count',
    'running_total_open_issues': 'Running Total Open Issues',
    'unique_contributors': 'Unique Contributors',
    'avg_commits_per_contributor': 'Average Commits per Contributor',
    'average_closure_days': 'Average Closure Days',
    'unique_pull_requests': 'Unique Pull Requests',
    'open_pull_requests': 'Open Pull Requests',
    'closed_pull_requests': 'Closed Pull Requests',
}


# Apply log transformation to each metric and create a new column for each
for metric in metrics:
    trimmed_did_data[f'log_{metric}'] = np.log1p(trimmed_did_data[metric])
    
# Check the first few rows to confirm the transformations
print(trimmed_did_data[['log_' + metric for metric in metrics]].head())


# Visualize the transformed distributions
plt.figure(figsize=(20, 15))
plt.suptitle('Log Transformed Distributions', fontsize=16, y=0.98)  # Adjust 'y' for vertical position

# Iterate over metrics for plotting
for i, metric in enumerate(metrics, 1):
    ax = plt.subplot(3, 4, i)  # Adjust subplot grid as needed
    sns.histplot(trimmed_did_data[f'log_{metric}'], kde=True)
    ax.set_title(metric_names[metric], pad=20)  # Use friendly names for titles
    plt.xlabel('Value')  # Optional: set x-axis label
    plt.ylabel('Frequency')  # Optional: set y-axis label

plt.tight_layout(pad=3.0)
plt.subplots_adjust(top=0.92)  # Adjust the top margin to give space for the suptitle
plt.show()

# Save the final DataFrame 
output_file_path_excel = os.path.join(target_directory, 'data', 'DiD', 'final_did_dataset_log_transformed_v2.xlsx')
trimmed_did_data.to_excel(output_file_path_excel, index=False)
