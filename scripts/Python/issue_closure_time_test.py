#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:52:27 2024

@author: paulsharratt
"""
import os

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"


# Change the current working directory
os.chdir(target_directory)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.issue_closure_time_functions import plot_issue_closure_data, plot_issue_closure_investment, average_issue_closure_time_per_month

engine = augur_db_connect("scripts/config.json")

org_name = 'curl'
start_date = "2019-01-01"
end_date = "2024-04-01"
save_directory = 'output/plots/org issue closure time'

curl_issue_data = plot_issue_closure_data(org_name, start_date, end_date, engine, save_directory)
curl_issue_data_investment = plot_issue_closure_investment(org_name, start_date, end_date, engine, save_directory)


# Load treatment group 
file_path = 'data/processed/treatment_group_final.xlsx'
treatment_df = pd.read_excel(file_path)
treatment_df['start_date'] = pd.to_datetime(treatment_df['start_date'])
treatment_df['end_date'] = pd.to_datetime(treatment_df['end_date'])


# Define the directory for saving plots
plots_dir = 'output/plots/org issue closure time'
os.makedirs(save_directory, exist_ok=True)


# Define data collection start and end dates
data_start_date = "2019-01-01"
data_end_date = "2024-04-01"


# Iterate over each row in the DataFrame
for index, row in treatment_df.iterrows():
    org_name = row['org']
    investment_start_date = row['start_date']
    investment_end_date = row['end_date']

    closure_time_df = average_issue_closure_time_per_month(org_name, data_start_date, data_end_date, engine)

    if closure_time_df.empty:
        print(f"No closure data found for {org_name}")
        continue

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=closure_time_df, x='issue_month', y='average_closure_days', marker='o', linestyle='-', color='b', label='Monthly Closure Time')
    plt.title(f"Average Issue Closure Time for {org_name}")
    plt.xlabel("Month")
    plt.ylabel("Average Closure Time (days)")
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Highlight the investment period
    plt.axvspan(investment_start_date, investment_end_date, color='grey', alpha=0.3, label='Investment Period')

    plt.legend()
    plt.tight_layout()

    # Save the plot
    sanitized_org_name = org_name.replace('/', '_').replace(' ', '_')
    plot_filename = f"{plots_dir}/{sanitized_org_name}_issue_closure_time.png"
    plt.savefig(plot_filename)
    plt.close()

    print(f'Plot saved for {org_name}: {plot_filename}')

