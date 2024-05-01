#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:29:30 2024

@author: paulsharratt
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Setting the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Changing the current working directory
os.chdir(target_directory)

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.release_frequency_functions import plot_org_release_frequency, get_org_release_frequency_over_time, calculate_release_frequencies

# Output directory
save_directory = 'output/plots/org release frequency over time'

# Importing Augur connect function
engine = augur_db_connect("scripts/config.json")

# Loading xlsx file containing the organization names
file_path = 'data/processed/treatment_group_final.xlsx'
treatment_df = pd.read_excel(file_path)
treatment_df['start_date'] = pd.to_datetime(treatment_df['start_date'])
treatment_df['end_date'] = pd.to_datetime(treatment_df['end_date'])

# Assuming the relevant column is named 'org_name' or similar
org_names = treatment_df['org'].unique()  

# Define the date range
start_date = '2019-01-01'
end_date = '2024-04-01'

# Process each organization
for org_name in org_names:
    plot_org_release_frequency(org_name, start_date, end_date, engine, save_directory)


# - testing curl
# will compare this output with the official release data from Daniel Stenberg
org_name = 'curl'
curl_test = get_org_release_frequency_over_time(org_name, start_date, end_date, engine)
print(curl_test)
file_path = 'data/raw/test_curl/test_curl_releases.csv'
curl_test.to_csv(file_path, index=False)


# Define the directory for saving plots
plots_dir = "output/plots/org release frequency over time and investment"
os.makedirs(plots_dir, exist_ok=True)

# Set the style of the plots
sns.set_style("whitegrid")

# Iterate over each organization in the treatment group
for index, row in treatment_df.iterrows():
    org_name = row['org']
    investment_start_date = row['start_date']  # Using the correct column name
    investment_end_date = row['end_date']      # Using the correct column name

    # Convert dates for axvspan, which needs exact positions
    investment_start_date = pd.to_datetime(investment_start_date)
    investment_end_date = pd.to_datetime(investment_end_date)

    # Fetch release frequency data over time using the function
    release_freq_df = get_org_release_frequency_over_time(org_name, '2019-01-01', '2024-04-01', engine)

    if release_freq_df.empty:
        print(f"No release data found for {org_name}")
        continue

    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(release_freq_df['release_month'], release_freq_df['release_count'], marker='o', linestyle='-', color='b', label='Monthly Releases')
    plt.title(f"Monthly Release Frequency for {org_name}")
    plt.xlabel("Month")
    plt.ylabel("Release Count")
    plt.grid(True)
    plt.xticks(rotation=45)

    # Highlight the investment period
    plt.axvspan(investment_start_date, investment_end_date, color='grey', alpha=0.3, label='Investment Period')

    plt.legend()
    plt.tight_layout()

    # Save the plot
    sanitized_org_name = org_name.replace('/', '_').replace(' ', '_')
    plot_filename = f"{plots_dir}/{sanitized_org_name}_release_frequency.png"
    plt.savefig(plot_filename)
    plt.close()

    print(f'Plot saved for {org_name}')
    


# Calculate release frequencies for each org wiith investment periods
release_frequencies = {}
for index, row in treatment_df.iterrows():
    org_name = row['org']
    investment_start_date = row['start_date']
    investment_end_date = row['end_date']

    frequencies = calculate_release_frequencies(org_name, investment_start_date, investment_end_date, engine)
    
    # Store frequencies along with investment periods
    release_frequencies[org_name] = {
        'Before Investment': frequencies['before'],
        'During Investment': frequencies['during'],
        'After Investment': frequencies['after'],
        'Investment Start Date': investment_start_date,
        'Investment End Date': investment_end_date
    }
    print(f"Calculated frequencies for {org_name}: {frequencies}")

# Convert the dictionary to a DataFrame
freq_df = pd.DataFrame.from_dict(release_frequencies, orient='index')
freq_df.index.name = 'Organization'
freq_df.columns = ['Average Releases Before Investment', 'Average Releases During Investment', 'Average Releases After Investment', 'Investment Start Date', 'Investment End Date']

print(freq_df)

output_path = "output/metrics/average_release_frequencies_per_month.csv"
freq_df.to_csv(output_path)
