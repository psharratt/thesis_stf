#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:56:50 2024

@author: paulsharratt
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 15:43:14 2024

@author: paulsharratt
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Loading commits_data_2 as DataFrame
file_path_1 = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/commits_data_2.xlsx"
commits_data_2_df = pd.read_excel(file_path_1)

# Loading treatment_group_final as DataFrame
file_path_2 = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/treatment_group_final.xlsx"
treatment_group_final_df = pd.read_excel(file_path_2)

# Convert start_date and end_date to datetime format if not already
treatment_group_final_df['start_date'] = pd.to_datetime(treatment_group_final_df['start_date'])
treatment_group_final_df['end_date'] = pd.to_datetime(treatment_group_final_df['end_date'])

# Update the directory for the plots
plots_dir = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/output/plots/repo commits over time and investment/"
os.makedirs(plots_dir, exist_ok=True)

# Set the style of the seaborn plots
sns.set_style("whitegrid")

# Loop through each unique repo_id to create a plot
for repo_id in commits_data_2_df['repo_id'].unique():
    # Filter the data for the current repo_id
    repo_data = commits_data_2_df[commits_data_2_df['repo_id'] == repo_id]
    
    # Find corresponding start_date and end_date from treatment_group_final_df
    contract_period = treatment_group_final_df[treatment_group_final_df['repo_id'] == repo_id]
    
    # Check if contract_period is not empty
    if not contract_period.empty:
        start_date = contract_period['start_date'].iloc[0]
        end_date = contract_period['end_date'].iloc[0]
    else:
        start_date, end_date = None, None
    
    # Extract the repository name for the title and filename
    repo_name = repo_data['repo'].iloc[0]
    
    # Sanitize the repo_name for use in the filename (replace spaces and special characters with "_")
    sanitized_repo_name = repo_name.replace(' ', '_').replace('/', '_')
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=repo_data, x='date', y='total_commits', marker="o", label='Total Commits')
    plt.title(f"Total Commits Over Time for {repo_name} (ID: {repo_id})")
    plt.xlabel("Date")
    plt.ylabel("Total Commits")
    
    # Add shaded region for contract period if dates are available
    if start_date and end_date:
        plt.axvspan(start_date, end_date, color='grey', alpha=0.2, label='Contract Period')
    
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot with repo name in the filename
    plot_filename = f"{plots_dir}commits_investment_{sanitized_repo_name}_{repo_id}.png"
    plt.savefig(plot_filename)
    plt.close()