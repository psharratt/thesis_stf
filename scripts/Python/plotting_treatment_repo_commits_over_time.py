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

# Load the Excel file into a pandas DataFrame
file_path = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/processed/commits_data_2.xlsx"
commits_data_2_df = pd.read_excel(file_path)

# Create a directory for the plots if it doesn't already exist
plots_dir = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/output/plots/repo commits over time/"
os.makedirs(plots_dir, exist_ok=True)

# Set the style of the seaborn plots
sns.set_style("whitegrid")

# Loop through each unique repo_id to create a plot
for repo_id in commits_data_2_df['repo_id'].unique():
    # Filter the data for the current repo_id
    repo_data = commits_data_2_df[commits_data_2_df['repo_id'] == repo_id]
    
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
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot with repo name in the filename
    plot_filename = f"{plots_dir}commits_over_time_{sanitized_repo_name}_{repo_id}.png"
    plt.savefig(plot_filename)
    plt.close()
