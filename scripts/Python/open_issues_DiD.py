#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:53:48 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)


from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.no_of_open_issues_functions import number_of_open_issues_per_month

engine = augur_db_connect("scripts/config.json")

# Load organization data
data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
org_data = pd.read_excel(data_file_path)

repo_id = 193661
org_name = 'curl'
start_date = "2012-01-01"
end_date = "2024-05-01"
# save_directory = 'output/plots/org issue closure time'

curl_open_issues_per_month = number_of_open_issues_per_month(org_name, start_date, end_date, engine)


def collect_open_issues_data(org_data, start_date, end_date, engine):
    all_org_issues = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org_name']  # Assuming the column name for organization name is 'org'
        print(f"Processing data for organization: {org_name}")
        
        # Fetch data
        org_issues_df = number_of_open_issues_per_month(org_name, start_date, end_date, engine)
        
        # Append additional organization info if needed for DiD analysis
        org_issues_df['org_name'] = org_name
        all_org_issues = pd.concat([all_org_issues, org_issues_df], ignore_index=True)
    
    return all_org_issues

# Define the overall date range for analysis
start_date = "2012-01-01"
end_date = "2024-05-01"

# Collect data
combined_issues_data = collect_open_issues_data(org_data, start_date, end_date, engine)

# Define the path for saving the output
output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_open_issues_data_all.csv')

# Save the combined data
combined_issues_data.to_csv(output_file_path, index=False)
print(f"Data saved to {output_file_path}")




"""
This doesn't quite work yet?, there's something about the cumulative totals, although the current version is much better

Or does it?

It might be down to curl being in several org names...

curl_issue_data_investment = plot_issue_closure_investment(org_name, start_date, end_date, engine, save_directory)
def number_of_open_issues_per_month(org_name, engine):

"""
