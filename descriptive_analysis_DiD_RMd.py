import os
import pandas as pd

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
os.chdir(target_directory)

# Load the data
did_data = pd.read_excel("data/DiD/final_did_dataset.xlsx")
did_data['time_period'] = pd.to_datetime(did_data['time_period'])
start_date, end_date = pd.to_datetime('2019-01-01'), pd.to_datetime('2024-04-01')
trimmed_did_data = did_data[(did_data['time_period'] >= start_date) & (did_data['time_period'] <= end_date)]

# Define groups
control_group = trimmed_did_data[trimmed_did_data['treated'] == 0]
treatment_group = trimmed_did_data[trimmed_did_data['treated'] == 1]

metrics = [
    'active_repositories', 'contributors', 'release_count',
    'running_total_open_issues', 'unique_contributors',
    'avg_commits_per_contributor', 'average_closure_days',
    'unique_pull_requests', 'open_pull_requests', 'closed_pull_requests'
]

# Initialize a DataFrame for formatted output
formatted_stats = []

# Calculate Descriptive Statistics for Each Metric
for metric in metrics:
    control_stats = control_group[metric].describe().drop('count')
    treatment_stats = treatment_group[metric].describe().drop('count')
    for stat in control_stats.index:
        formatted_stats.append({
            'Metric': metric,
            'Statistic': stat.capitalize(),
            'Control': f"{control_stats[stat]:.2f}",
            'Treatment': f"{treatment_stats[stat]:.2f}"
        })

# Convert list to DataFrame
formatted_stats_df = pd.DataFrame(formatted_stats)

# Save as markdown table
formatted_stats_df.to_markdown("descriptive_statistics.md", index=False)

print("Formatted statistics have been saved to 'descriptive_statistics.md'.")
