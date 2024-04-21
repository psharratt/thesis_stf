#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:38:10 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

# Load your datasets:
    
# Treatment variables
df_open_issues = pd.read_csv('data/DiD/combined_open_issues_data_all.csv')
df_release_frequency = pd.read_csv('data/DiD/combined_release_frequency_data_all.csv')
df_contributors = pd.read_csv('data/DiD/combined_contributor_data_all.csv')
df_contributor_load = pd.read_csv('data/DiD/combined_contributor_load_data_all.csv')
df_issue_closure = pd.read_csv('data/DiD/combined_issue_closure_data_all.csv')

# Control variables
df_PR_metrics = pd.read_csv('data/DiD/combined_pull_request_data_all.csv')

df_treatment_info = pd.read_excel('data/processed/treatment_group.xlsx')

# Rename the time columns to 'time_period'
df_open_issues.rename(columns={'issue_month': 'time_period'}, inplace=True)
df_release_frequency.rename(columns={'release_month': 'time_period'}, inplace=True)
df_contributors.rename(columns={'month': 'time_period'}, inplace=True)
df_contributor_load.rename(columns={'commit_month': 'time_period'}, inplace=True)  # Adjust this line as per your actual column names
df_issue_closure.rename(columns={'issue_month': 'time_period'}, inplace=True)
df_PR_metrics.rename(columns={'month': 'time_period'}, inplace=True)

# Contributors & Metrics: Converting 'time_period' to string to safely use string methods
df_contributors['time_period'] = df_contributors['time_period'].astype(str)
df_PR_metrics['time_period'] = df_PR_metrics['time_period'].astype(str)

# Check if 'time_period' needs day appended (if it's in 'YYYY-MM' format)
if df_contributors['time_period'].str.len().eq(7).any():
    # Append '-01' to assume the first day of the month for datetime conversion
    df_contributors['time_period'] = pd.to_datetime(df_contributors['time_period'] + '-01', format='%Y-%m-%d')
else:
    # Already in 'YYYY-MM-DD' format or similar
    df_contributors['time_period'] = pd.to_datetime(df_contributors['time_period'], format='%Y-%m-%d')

# Check if 'time_period' needs day appended (if it's in 'YYYY-MM' format)
if df_PR_metrics['time_period'].str.len().eq(7).any():
    # Append '-01' to assume the first day of the month for datetime conversion
    df_PR_metrics['time_period'] = pd.to_datetime(df_PR_metrics['time_period'] + '-01', format='%Y-%m-%d')
else:
    # Already in 'YYYY-MM-DD' format or similar
    df_PR_metrics['time_period'] = pd.to_datetime(df_PR_metrics['time_period'], format='%Y-%m-%d')




# Standardize 'time_period' across all DataFrames to datetime
for df in [df_open_issues, df_release_frequency, df_contributors, df_contributor_load, df_issue_closure, df_PR_metrics]:
    df['time_period'] = pd.to_datetime(df['time_period'], errors='coerce', format='%Y-%m-%d')

# Merge all dataframes on 'org_name' and 'time_period'
df_final = df_open_issues
for df in [df_release_frequency, df_contributors, df_contributor_load, df_issue_closure, df_PR_metrics]:
    df_final = pd.merge(df_final, df, on=['org_name', 'time_period'], how='outer')

# Convert 'time_period' to datetime for comparison
df_final['time_period'] = pd.to_datetime(df_final['time_period'], format='%Y-%m-%d')
df_treatment_info['start_date'] = pd.to_datetime(df_treatment_info['start_date'])
df_treatment_info['end_date'] = pd.to_datetime(df_treatment_info['end_date'])

# Create the treatment indicator
def treatment_assignment(row):
    treatment_period = df_treatment_info[(df_treatment_info['org_name'] == row['org_name']) &
                                         (df_treatment_info['start_date'] <= row['time_period']) &
                                         (df_treatment_info['end_date'] >= row['time_period'])]
    if not treatment_period.empty:
        return 1
    return 0

df_final['treated'] = df_final.apply(treatment_assignment, axis=1)

# Reorder columns
column_order = ['time_period', 
                'org_name', 
                'running_total_open_issues', 
                'release_count', 
                'unique_contributors', 
                'avg_commits_per_contributor', 
                'average_closure_days', 
                'unique_pull_requests',
                'open_pull_requests',
                'closed_pull_requests',
                'treated']

df_final = df_final[column_order]

# Save the final DataFrame in both CSV and Excel formats
output_file_path_csv = os.path.join(target_directory, 'data', 'DiD', 'final_did_dataset.csv')
output_file_path_excel = os.path.join(target_directory, 'data', 'DiD', 'final_did_dataset.xlsx')

df_final.to_csv(output_file_path_csv, index=False)
print("CSV DataFrame is ready and saved for DiD analysis at {}".format(output_file_path_csv))

df_final.to_excel(output_file_path_excel, index=False)
print("Excel DataFrame is ready and saved for DiD analysis at {}".format(output_file_path_excel))