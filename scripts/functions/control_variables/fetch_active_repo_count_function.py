#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:00:33 2024

@author: paulsharratt
"""


def fetch_monthly_active_repo_count(org_name, start_date, end_date, engine):
    """
    Fetches the count of unique active repositories per month for a specified organization.
    
    Parameters:
    org_name (str): Organization name on GitHub.
    start_date (str): Start date for the data retrieval in YYYY-MM-DD format.
    end_date (str): End date for the data retrieval in YYYY-MM-DD format.
    engine: SQLalchemy engine object connected to the database.
    
    Returns:
    pandas.DataFrame: DataFrame with months and active repository counts.
    """
    query = f"""
    WITH MonthlyCommits AS (
        SELECT
            DATE_TRUNC('month', CAST(cmt_committer_date AS TIMESTAMP)) AS month,
            repo_id
        FROM
            augur_data.commits
        WHERE
            cmt_committer_date IS NOT NULL
            AND repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
            AND cmt_committer_date BETWEEN '{start_date}' AND '{end_date}'
    )
    SELECT
        month,
        COUNT(DISTINCT repo_id) AS active_repositories
    FROM
        MonthlyCommits
    GROUP BY
        month
    ORDER BY
        month;
    """
    import pandas as pd
    df = pd.read_sql_query(query, con=engine)
    df['month'] = pd.to_datetime(df['month']).dt.to_period('M')  # Convert timestamps to period (month)
    return df