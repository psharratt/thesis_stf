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
trimmed_did_data = pd.read_excel("data/DiD/trimmed_did_dataset.xlsx")

metrics = [
    'running_total_open_issues',
    'release_count',
    'unique_contributors',
    'avg_commits_per_contributor',
    'average_closure_days'
]

# Apply log transformation to each metric and create a new column for each
for metric in metrics:
    trimmed_did_data[f'log_{metric}'] = np.log1p(trimmed_did_data[metric])

# Check the first few rows to confirm the transformations
print(trimmed_did_data[['log_' + metric for metric in metrics]].head())


# Visualize the transformed distributions
plt.figure(figsize=(15, 10))
for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 3, i)
    sns.histplot(trimmed_did_data[f'log_{metric}'], kde=True)
    plt.title(f'Log Transformed Distribution of {metric}')
plt.tight_layout()
plt.show()
