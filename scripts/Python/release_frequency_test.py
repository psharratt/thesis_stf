#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:34:07 2024

@author: paulsharratt
"""
import os

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.release_frequency_functions import get_release_data, activity_release_data, get_aggregated_release_data, get_org_release_data, get_org_release_frequency,  get_org_release_frequency_over_time

# If your script is in thesis_stf and you run it from there:
engine = augur_db_connect("scripts/config.json")

org_name  = 'curl'
repo_name = 'fpm'
repo_id =  '191494' # fortran-lang	fpm
start_date = '2019-01-01'
end_date =  '2024-04-01'


# TESTING RELEASE DATA

# get_release_data Function & call
# arguments: repo_id, start_date, end_date, engine
fortran_release_data = get_release_data(repo_id, start_date, end_date, engine)

# works
print(fortran_release_data)


# TESTING ACTIVITIY RELEASE DATA

# activity_release_data Function & call
# arguments: repo_id, repo_name, org_name, start_date, end_date, engine
fortran_activity_release_data = activity_release_data(repo_id, repo_name, org_name, start_date, end_date, engine)


print(fortran_activity_release_data)

# TESTING AGGREGATED ACTIVITIY RELEASE DATA

# Example repository IDs for Fortran
repo_ids = [
    150834, 191494, 191615, 191616, 191619, 191621, 191632, 191631,
    191637, 191628, 191626, 191623, 191620, 191640, 191617, 191624,
    191636, 191625, 191629, 191638, 191627, 191614, 191634, 191641,
    191635, 191622, 191633, 191630
]  

# Fetch release data for Fortran
fortran_releases_df = get_aggregated_release_data(repo_ids, start_date, end_date, engine)

# Output the results
print(fortran_releases_df)

# need to come up with a function that gives the release frequency of an org across all repos over time...

# TESTING ORG RELEASE DATA

# Fetch release data
fortran_org_df = get_org_release_data(org_name, start_date, end_date, engine)

# Output the results
print(fortran_org_df)


# TESTING ORG RELEASE FREQUENCY
fortran_org_release_frequency = get_org_release_frequency(org_name, start_date, end_date, engine)

# Output the results
print(fortran_org_release_frequency)

# TESTING ORG RELEASE FREQUENCY OVER TIME

org_name  = 'apache'
repo_name = 'fpm'
repo_id =  '191494' # fortran-lang	fpm
start_date = '2019-01-01'
end_date =  '2024-04-01'

fortran_org_release_frequency_over_time = get_org_release_frequency_over_time(org_name, start_date, end_date, engine)

# Output the results
print(fortran_org_release_frequency_over_time)

import matplotlib.pyplot as plt

# Fetch release frequency data over time
release_freq_df = get_org_release_frequency_over_time("fortran-lang", "2019-01-01", "2023-01-01", engine)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(release_freq_df['release_month'], release_freq_df['release_count'], marker='o')
plt.title(f'Monthly Release Frequency for {org_name}')
plt.xlabel('Month')
plt.ylabel('Number of Releases')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
