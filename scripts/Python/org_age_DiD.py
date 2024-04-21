#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:38:15 2024

@author: paulsharratt
"""

import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.control_variables.calculate_org_age_function import calculate_org_age_from_first_release

def collect_org_age_data(org_data, start_date, end_date, engine):
    all_org_ages = pd.DataFrame()
    for idx, row in org_data.iterrows():
        org_name = row['org_name']  # Confirm the column name 'org_name' matches your DataFrame
        print(f"Processing age data for organization: {org_name}")

        # Fetch data
        try:
            org_age_data = calculate_org_age_from_first_release(org_name, start_date, end_date, engine)
            org_age_data['org_name'] = org_name  # Append organization name for merging later
            all_org_ages = pd.concat([all_org_ages, org_age_data], ignore_index=True)
        except ValueError as e:
            print(f"Failed to process data for {org_name}: {e}")

    return all_org_ages

def main():
    engine = augur_db_connect("scripts/config.json")

    # Load organization data
    data_file_path = os.path.join(target_directory, 'data', 'processed', 'treatment_group.xlsx')
    org_data = pd.read_excel(data_file_path)

    # Collect data
    start_date = "2012-01-01"
    end_date = "2024-05-01"
    combined_org_age_data = collect_org_age_data(org_data, start_date, end_date, engine)

    # Save the data
    output_file_path = os.path.join(target_directory, 'data', 'DiD', 'combined_org_age_data_all.csv')
    combined_org_age_data.to_csv(output_file_path, index=False)
    print(f"Organization age data saved to {output_file_path}")

if __name__ == "__main__":
    main()


'''
GNOME is a GitHub mirror, started in Jun 3, 2012
GStreamer is a GitHub mirror, started in 


'''