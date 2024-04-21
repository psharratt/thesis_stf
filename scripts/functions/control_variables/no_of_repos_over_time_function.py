#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:04:45 2024

@author: paulsharratt

THIS DOESN'T WORK BECAUSE YOU DON'T HAVE VALUES IN THE REPO_ADDED COLUMN
"""
import pandas as pd
import logging
    
def number_of_repos_per_month(org_name, start_date, end_date, engine):
    """
    Get monthly repository count for a GitHub organization from the Augur database.
    This function computes the count of repositories under the specified GitHub organization
    that were created up to the end of each month within the specified date range, identified by the GitHub URL.

    Parameters
    ----------
    org_name : str
        GitHub organization name part of the repo URL.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object used to execute queries.

    Returns
    -------
    pandas.DataFrame
        DataFrame with each row representing a month and the cumulative number of repositories up to that month.
    """

    # Set up logging
    logging.basicConfig(filename='repo_count_error_log.log', level=logging.ERROR, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

    # Prepare SQL query
    query = f"""
        WITH RepoCreation AS (
            SELECT
                DATE_TRUNC('month', CAST(repo.repo_added AS TIMESTAMP)) AS creation_month,
                COUNT(repo.repo_id) AS repo_count
            FROM
                repo
            WHERE
                repo.repo_git LIKE '%%github.com/{org_name}/%%'
                AND repo.repo_added <= '{end_date}'
            GROUP BY
                DATE_TRUNC('month', CAST(repo.repo_added AS TIMESTAMP))
        ),
        MonthlyCount AS (
            SELECT
                series.month,
                COALESCE(SUM(rc.repo_count) OVER (ORDER BY series.month), 0) AS cumulative_repos
            FROM
                (SELECT generate_series(DATE_TRUNC('month', '{start_date}'::date), 
                                        DATE_TRUNC('month', '{end_date}'::date), 
                                        '1 month'::interval) AS month) series
            LEFT JOIN RepoCreation rc
            ON series.month >= rc.creation_month
        )
        SELECT
            month,
            cumulative_repos
        FROM
            MonthlyCount
        ORDER BY
            month;
    """

    try:
        # Execute SQL query
        repo_count_df = pd.read_sql_query(query, con=engine)
        
        # Convert 'month' to period (M) to ensure consistency for time series analysis
        repo_count_df['month'] = pd.to_datetime(repo_count_df['month']).dt.to_period('M')
        
        return repo_count_df

    except Exception as e:
        logging.error(f"Failed to fetch repository count data using org name {org_name}: {e}", exc_info=True)
        return pd.DataFrame(columns=['month', 'cumulative_repos'])
