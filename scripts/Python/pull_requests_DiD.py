#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:18:11 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.control_variables.number_of_PRs_per_month_function import fetch_pull_request_metrics

def collect_pull_request_data(org_data, start_date, end_date, engine):
    all_org_pull_requests = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org_name']  # Ensure the column name 'org_name' matches your DataFrame
        print(f"Processing pull request data for organization: {org_name}")

        # Fetch data
        org_pr_data = fetch_pull_request_metrics(org_name, start_date, end_date, engine)

        # Append organization name for merging later
        org_pr_data['org_name'] = org_name
        all_org_pull_requests = pd.concat([all_org_pull_requests, org_pr_data], ignore_index=True)

    return all_org_pull_requests

def main():
    engine = augur_db_connect("scripts/config.json")

    # Load organization data
    data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
    org_data = pd.read_excel(data_file_path)

    # Collect data
    start_date = "2012-01-01"
    end_date = "2024-05-01"
    combined_pull_request_data = collect_pull_request_data(org_data, start_date, end_date, engine)

    # Save the data
    output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_pull_request_data_all.csv')
    combined_pull_request_data.to_csv(output_file_path, index=False)
    print(f"Pull request data saved to {output_file_path}")

if __name__ == "__main__":
    main()