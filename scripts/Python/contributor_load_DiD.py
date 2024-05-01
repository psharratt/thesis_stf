#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:23:56 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.contributor_load_functions import get_org_contributor_load_over_time

engine = augur_db_connect("scripts/config.json")

def collect_contributor_load_data(org_data, start_date, end_date, engine):
    all_org_contributor_load = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org_name']
        print(f"Processing contributor load data for organization: {org_name}")
        
        # Fetch data
        org_contributor_load_df = get_org_contributor_load_over_time(org_name, start_date, end_date, engine)
        
        # Append organization name for merging later
        org_contributor_load_df['org_name'] = org_name
        all_org_contributor_load = pd.concat([all_org_contributor_load, org_contributor_load_df], ignore_index=True)
    
    return all_org_contributor_load

def main():
    engine = augur_db_connect("scripts/config.json")

    # Load organization data
    data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
    org_data = pd.read_excel(data_file_path)

    # Collect data
    start_date = "2012-01-01"
    end_date = "2024-05-01"
    combined_contributor_load_data = collect_contributor_load_data(org_data, start_date, end_date, engine)

    # Save the data
    output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_contributor_load_data_all.csv')
    combined_contributor_load_data.to_csv(output_file_path, index=False)
    print(f"Contributor load data saved to {output_file_path}")

if __name__ == "__main__":
    main()
