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

# Setting working directory
os.chdir(target_directory)

# Loading datasets:
    
# Treatment variables
df_open_issues = pd.read_csv('data/DiD/combined_open_issues_data_all.csv')
df_release_frequency = pd.read_csv('data/DiD/combined_release_frequency_data_all.csv')
df_contributors = pd.read_csv('data/DiD/combined_contributor_data_all.csv')
df_contributor_load = pd.read_csv('data/DiD/combined_contributor_load_data_all.csv')
df_issue_closure = pd.read_csv('data/DiD/combined_issue_closure_data_all.csv')

# Control variables
df_PR_metrics = pd.read_csv('data/DiD/combined_pull_request_data_all.csv')
df_unique_contributors = pd.read_csv('data/DiD/combined_unique_contributor_data_all.csv')
df_org_age = pd.read_csv('data/DiD/combined_org_age_data_all.csv')
df_active_repos = pd.read_csv('data/DiD/combined_active_repo_data_all.csv')
        
# Treatment group
df_treatment_info = pd.read_excel('data/processed/treatment_group.xlsx')

# Rename the time columns to 'time_period'
df_open_issues.rename(columns={'issue_month': 'time_period'}, inplace=True)
df_release_frequency.rename(columns={'release_month': 'time_period'}, inplace=True)
df_contributors.rename(columns={'month': 'time_period'}, inplace=True)
df_contributor_load.rename(columns={'commit_month': 'time_period'}, inplace=True)  # Adjust this line as per your actual column names
df_issue_closure.rename(columns={'issue_month': 'time_period'}, inplace=True)
df_PR_metrics.rename(columns={'month': 'time_period'}, inplace=True)
df_unique_contributors.rename(columns={'month': 'time_period'}, inplace=True)
df_org_age.rename(columns={'month': 'time_period'}, inplace=True)
df_active_repos.rename(columns={'month': 'time_period'}, inplace=True)

# Contributors & Metrics: Converting 'time_period' to string to safely use string methods
df_contributors['time_period'] = df_contributors['time_period'].astype(str)
df_PR_metrics['time_period'] = df_PR_metrics['time_period'].astype(str)
df_unique_contributors['time_period'] = df_PR_metrics['time_period'].astype(str)
df_org_age['time_period'] = df_PR_metrics['time_period'].astype(str)
df_active_repos['time_period'] = df_PR_metrics['time_period'].astype(str)

df_contributors.rename(columns={'unique_contributors': 'contributors'}, inplace=True)


def standardize_date(df, date_column='time_period'):
    """
    Standardizes the date column to a datetime format, assuming YYYY-MM if needed.

    Parameters:
    df (DataFrame): DataFrame containing the date column to standardize.
    date_column (str): Name of the column containing date information.
    """
    if df[date_column].dtype == 'object':
        # Check if 'time_period' is in 'YYYY-MM' format and convert to 'YYYY-MM-DD'
        if df[date_column].str.len().eq(7).any():
            df[date_column] = pd.to_datetime(df[date_column] + '-01', format='%Y-%m-%d')
        else:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df


# Apply date standardization
dataframes = [df_open_issues, df_release_frequency, df_contributors, df_contributor_load,
              df_issue_closure, df_PR_metrics, df_unique_contributors, df_org_age, df_active_repos]

for df in dataframes:
    df = standardize_date(df, 'time_period')

# Merge dataframes on 'org_name' and 'time_period'
df_final = df_open_issues
for df in [df_release_frequency, df_contributors, df_contributor_load, df_issue_closure, 
           df_PR_metrics, df_unique_contributors, df_org_age, df_active_repos]:
    df_final = pd.merge(df_final, df, on=['org_name', 'time_period'], how='outer')



# Create the treatment indicator
def treatment_assignment(row):
    conditions = (df_treatment_info['org_name'] == row['org_name']) & \
                 (df_treatment_info['start_date'] <= row['time_period']) & \
                 (df_treatment_info['end_date'] >= row['time_period'])
    return 1 if not df_treatment_info[conditions].empty else 0

df_final['treated'] = df_final.apply(treatment_assignment, axis=1)


column_names = df_final.columns
print(column_names)



# Reorder columns
column_order = ['time_period', 
                'org_name', 
                'age',
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
                'treated'
]

df_final = df_final[column_order]

# Saving the final DF in both CSV and Excel formats
output_file_path_csv = os.path.join(target_directory, 'data', 'DiD', 'final_did_dataset_v2.csv')
output_file_path_excel = os.path.join(target_directory, 'data', 'DiD', 'final_did_dataset_v2.xlsx')

df_final.to_csv(output_file_path_csv, index=False)
print("CSV DataFrame is ready and saved for DiD analysis at {}".format(output_file_path_csv))

df_final.to_excel(output_file_path_excel, index=False)
print("Excel DataFrame is ready and saved for DiD analysis at {}".format(output_file_path_excel))