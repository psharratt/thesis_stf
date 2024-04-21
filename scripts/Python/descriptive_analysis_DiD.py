#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:24:07 2024

@author: paulsharratt
"""
import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

# Load the data
did_data = pd.read_excel("data/DiD/final_did_dataset.xlsx")

# Convert 'time_period' to datetime format if not already
did_data['time_period'] = pd.to_datetime(did_data['time_period'])

# Define the common period
start_date = pd.to_datetime('2019-01-01')
end_date = pd.to_datetime('2024-04-01')

# Filter the data to include only the common period
trimmed_did_data = did_data[(did_data['time_period'] >= start_date) & (did_data['time_period'] <= end_date)]

trimmed_did_data.to_excel("data/DiD/trimmed_did_dataset.xlsx")


# Assuming the DataFrame has 'group' column to differentiate between control (0) and treatment (1) groups
# Divide the dataset based on treatment status
control_group = trimmed_did_data[trimmed_did_data['treated'] == 0]
treatment_group = trimmed_did_data[trimmed_did_data['treated'] == 1]

# Metrics to analyze
metrics = [
    'running_total_open_issues',
    'release_count',
    'unique_contributors',
    'avg_commits_per_contributor',
    'average_closure_days'
]

# Initialize a dictionary to store stats
stats = {}

# Calculate Descriptive Statistics for Each Metric
for metric in metrics:
    stats[metric] = {
        "Control": {
            "Count": control_group[metric].count(),
            "Mean": control_group[metric].mean(),
            "Median": control_group[metric].median(),
            "Standard Deviation": control_group[metric].std(),
            "25% Quantile": control_group[metric].quantile(0.25),
            "75% Quantile": control_group[metric].quantile(0.75),
            "Variance": control_group[metric].var()
        },
        "Treatment": {
            "Count": treatment_group[metric].count(),
            "Mean": treatment_group[metric].mean(),
            "Median": treatment_group[metric].median(),
            "Standard Deviation": treatment_group[metric].std(),
            "25% Quantile": treatment_group[metric].quantile(0.25),
            "75% Quantile": treatment_group[metric].quantile(0.75),
            "Variance": treatment_group[metric].var()
        }
    }

# Convert the dictionary to DataFrame for better display
stats_did_df = pd.DataFrame(stats).swapaxes("index", "columns")  # Swap rows and columns for better readability

print(stats_did_df)

stats_did_df.to_excel("data/DiD/descriptive_statistics_all.xlsx")


# Excel writer for saving dataframes
with pd.ExcelWriter("data/DiD/descriptive_statistics.xlsx") as writer:
    for metric in metrics:
        stats = {
            "Control": {
                "Count": control_group[metric].count(),
                "Mean": control_group[metric].mean(),
                "Median": control_group[metric].median(),
                "Standard Deviation": control_group[metric].std(),
                "25% Quantile": control_group[metric].quantile(0.25),
                "75% Quantile": control_group[metric].quantile(0.75),
                "Variance": control_group[metric].var()
            },
            "Treatment": {
                "Count": treatment_group[metric].count(),
                "Mean": treatment_group[metric].mean(),
                "Median": treatment_group[metric].median(),
                "Standard Deviation": treatment_group[metric].std(),
                "25% Quantile": treatment_group[metric].quantile(0.25),
                "75% Quantile": treatment_group[metric].quantile(0.75),
                "Variance": treatment_group[metric].var()
            }
        }

        # Convert the dictionary to DataFrame
        stats_df = pd.DataFrame(stats)
        
        # Print metric name and its DataFrame
        print(f"Stats for {metric}:")
        print(stats_df)
        print("\n")  # Print a newline for better separation in output

        # Save the DataFrame to an Excel sheet named by the metric
        stats_df.to_excel(writer, sheet_name=metric)

print("All metrics have been processed and saved.")

