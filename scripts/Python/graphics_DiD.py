#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 19:28:19 2024

@author: paulsharratt
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

# Load the data
trimmed_did_data = pd.read_excel("data/DiD/trimmed_did_dataset.xlsx")

# Assuming 'time_period' and 'group' are correctly set, and data is loaded as 'trimmed_did_data'
trimmed_did_data['time_period'] = pd.to_datetime(trimmed_did_data['time_period'])

# Setting the figure size and layout
plt.figure(figsize=(14, 8))

# List of metrics to plot
metrics = [
    'running_total_open_issues',
    'release_count',
    'unique_contributors',
    'avg_commits_per_contributor',
    'average_closure_days'
]

# Create a time series plot for each metric
for metric in metrics:
    plt.figure()
    sns.lineplot(data=trimmed_did_data, x='time_period', y=metric, hue='treated', style='treated', markers=True, dashes=False)
    plt.title(f'Time Series Trend for {metric}')
    plt.ylabel(metric)
    plt.xlabel('Time Period')
    plt.legend(title='Group', labels=['Control', 'Treatment'])
    plt.xticks(rotation=45)  # Rotate dates for better legibility
    plt.tight_layout()
    plt.show()


# Histograms and Boxplots for each metric
for metric in metrics:
    plt.figure(figsize=(14, 6))

    # Histogram
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
    sns.histplot(data=trimmed_did_data, x=metric, hue='treated', element='step', kde=True)
    plt.title(f'Histogram of {metric}')
    plt.xlabel(metric)
    plt.ylabel('Frequency')

    # Boxplot
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
    sns.boxplot(x='treated', y=metric, data=trimmed_did_data)
    plt.title(f'Box Plot of {metric}')
    plt.xlabel('Group')
    plt.ylabel(metric)

    plt.tight_layout()
    plt.show()

pre_treatment_end_date = '2018-12-31'



# Setting the figure size for the plot
plt.figure(figsize=(12, 7))

# Creating a line plot to visualize the trends of 'running_total_open_issues' over time
# categorized by treatment status
sns.lineplot(data=trimmed_did_data, x='time_period', y='running_total_open_issues', hue='treated', style='treated', markers=True, dashes=False)

# Adding titles and labels
plt.title('Time Series of Running Total Open Issues by Treatment Status')
plt.xlabel('Time Period')
plt.ylabel('Running Total Open Issues')

# Improving layout for better legibility
plt.xticks(rotation=45)  # Rotate x-axis labels for clarity
plt.tight_layout()

# Displaying the plot
plt.show()
