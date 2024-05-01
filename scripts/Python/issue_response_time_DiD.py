#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:51:23 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.issue_closure_time_functions import average_issue_closure_time_per_month

def collect_issue_closure_data(org_data, start_date, end_date, engine):
    all_org_issue_closure = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org_name']  
        print(f"Processing issue closure data for organization: {org_name}")
        
        # Fetch data
        org_issue_closure_df = average_issue_closure_time_per_month(org_name, start_date, end_date, engine)
        
        # Append organization name for merging later
        org_issue_closure_df['org_name'] = org_name
        all_org_issue_closure = pd.concat([all_org_issue_closure, org_issue_closure_df], ignore_index=True)
    
    return all_org_issue_closure

def main():
    engine = augur_db_connect("scripts/config.json")

    # Load organization data
    data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
    org_data = pd.read_excel(data_file_path)

    # Collect data
    start_date = "2012-01-01"
    end_date = "2024-05-01"
    combined_issue_closure_data = collect_issue_closure_data(org_data, start_date, end_date, engine)

    # Save the data
    output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_issue_closure_data_all.csv')
    combined_issue_closure_data.to_csv(output_file_path, index=False)
    print(f"Issue closure data saved to {output_file_path}")

if __name__ == "__main__":
    main()
