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
from scripts.functions.release_frequency_functions import get_org_release_frequency_over_time

def collect_release_frequency_data(org_data, start_date, end_date, engine):
    all_org_release_frequency = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org']  # Confirm the column name 'org' matches your DataFrame
        print(f"Processing release frequency data for organization: {org_name}")
        
        # Fetch data
        org_release_freq_df = get_org_release_frequency_over_time(org_name, start_date, end_date, engine)
        
        # Append organization name for merging later
        org_release_freq_df['org_name'] = org_name
        all_org_release_frequency = pd.concat([all_org_release_frequency, org_release_freq_df], ignore_index=True)
    
    return all_org_release_frequency

def main():
    engine = augur_db_connect("scripts/config.json")

    # Load organization data
    data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
    org_data = pd.read_excel(data_file_path)

    # Collect data
    start_date = "2012-01-01"
    end_date = "2024-05-01"
    combined_release_frequency_data = collect_release_frequency_data(org_data, start_date, end_date, engine)

    # Save the data
    output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_release_frequency_data_all.csv')
    combined_release_frequency_data.to_csv(output_file_path, index=False)
    print(f"Release frequency data saved to {output_file_path}")

if __name__ == "__main__":
    main()
