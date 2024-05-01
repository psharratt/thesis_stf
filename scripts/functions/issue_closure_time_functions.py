#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:51:23 2024

@author: paulsharratt
"""

def number_of_open_issues_per_month(org_name, start_date, end_date, engine):
    """Calculate the number of open issues per month for a GitHub organization within a specified date range.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy engine object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the count of open issues per month.
    """
    query = f"""
        SELECT
            DATE_TRUNC('month', created_at) AS issue_month,
            COUNT(issue_id) AS open_issues_count
        FROM
            augur_data.issues
        WHERE
            repo_id IN (
                SELECT repo_id
                FROM augur_data.repo
                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
            )
            AND created_at >= '{start_date}'
            AND created_at <= '{end_date}'
            AND issue_state = 'open'
        GROUP BY DATE_TRUNC('month', created_at)
        ORDER BY issue_month
    """
    import pandas as pd
    open_issues_df = pd.read_sql_query(query, con=engine)
    return open_issues_df




def average_issue_closure_time_per_month(org_name, start_date, end_date, engine):
    """Calculate the average time taken to close issues per month for a GitHub organization within a specified date range.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format for data collection.
    end_date : str
        End date in YYYY-MM-DD format for data collection.
    engine : sqlalchemy engine object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the average closure time (in days) per month.
    """
    query = f"""
        SELECT
            DATE_TRUNC('month', created_at) AS issue_month,
            AVG(EXTRACT(epoch FROM (closed_at - created_at))/86400) AS average_closure_days
        FROM
            augur_data.issues
        WHERE
            repo_id IN (
                SELECT repo_id
                FROM augur_data.repo
                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
            )
            AND created_at >= '{start_date}'
            AND created_at <= '{end_date}'
            AND issue_state = 'closed'
        GROUP BY DATE_TRUNC('month', created_at)
        ORDER BY issue_month
    """
    import pandas as pd
    return pd.read_sql_query(query, con=engine)

def plot_issue_closure_data(org_name, start_date, end_date, engine, save_directory):
    """Plot the average issue closure time per month for a GitHub organization within specified date range.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy engine object
        Database connection object.
    save_directory : str
        Directory path to save the plot.
    """
    closure_time_df = average_issue_closure_time_per_month(org_name, start_date, end_date, engine)
    
    if closure_time_df.empty:
        print(f"No closure data found for {org_name}")
        return
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=closure_time_df, x='issue_month', y='average_closure_days', marker='o', linestyle='-')
    plt.title(f'Average Issue Closure Time for {org_name} ({start_date} to {end_date})')
    plt.xlabel('Month')
    plt.ylabel('Average Closure Time (days)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Ensure the directory exists
    import os
    os.makedirs(save_directory, exist_ok=True)
    plot_filename = f"{save_directory}/{org_name}_issue_closure_time.png"
    plt.savefig(plot_filename)
    plt.close()
    print(f'Plot saved for {org_name}: {plot_filename}')
    
def plot_issue_closure_investment(row, start_date, end_date, engine, save_directory):
    """Plot the average issue closure time per month for a GitHub organization and highlight the investment period.

    Parameters
    ----------
    row : pd.Series
        A row from the DataFrame containing organization name, and investment start and end dates.
    start_date : str
        Start date in YYYY-MM-DD format for data collection.
    end_date : str
        End date in YYYY-MM-DD format for data collection.
    engine : sqlalchemy engine object
        Database connection object.
    save_directory : str
        Directory path to save the plot.
    """
    import pandas as pd
    org_name = row['org']
    investment_start_date = pd.to_datetime(row['start_date']).strftime('%Y-%m-%d')
    investment_end_date = pd.to_datetime(row['end_date']).strftime('%Y-%m-%d')

    closure_time_df = average_issue_closure_time_per_month(org_name, start_date, end_date, engine)
    
    if closure_time_df.empty:
        print(f"No closure data found for {org_name}")
        return
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=closure_time_df, x='issue_month', y='average_closure_days', marker='o', linestyle='-')
    plt.title(f'Average Issue Closure Time for {org_name} ({start_date} to {end_date})')
    plt.xlabel('Month')
    plt.ylabel('Average Closure Time (days)')
    plt.grid(True)
    plt.xticks(rotation=45)

    # Highlight the investment period
    plt.axvspan(pd.to_datetime(investment_start_date), pd.to_datetime(investment_end_date), color='yellow', alpha=0.3, label='Investment Period')
    plt.legend()

    plt.tight_layout()
    
    import os
    
    # Ensure directory exists
    os.makedirs(save_directory, exist_ok=True)
    plot_filename = f"{save_directory}/{org_name.replace('/', '_').replace(' ', '_').replace(':', '_')}_issue_closure_time.png"
    plt.savefig(plot_filename)
    plt.close()
    print(f'Plot saved for {org_name}: {plot_filename}')

