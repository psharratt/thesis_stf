#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 17:16:06 2024

@author: paulsharratt
"""

def number_of_forks_per_month(org_name, start_date, end_date, engine):
    """
    Calculate the total number of forks for all repositories in a GitHub organization,
    cumulated monthly from the start_date to the end_date.

    Parameters
    ----------
    org_name : str
        Name of the GitHub organization.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy engine object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing each month and the cumulative number of forks by that month.
    """
    import pandas as pd
    import logging

    logging.basicConfig(filename='forks_count_error_log.log', level=logging.ERROR, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

    query = f"""
        WITH ForksByMonth AS (
            SELECT
                DATE_TRUNC('month', repo.repo_added) AS month,
                SUM(repo.forks_count) AS total_forks
            FROM
                augur_data.repo
            JOIN
                augur_data.repo_groups ON repo.repo_group_id = repo_groups.repo_group_id
            WHERE
                LOWER(repo_groups.rg_name) = LOWER('{org_name}')
                AND repo.repo_added BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY
                DATE_TRUNC('month', repo.repo_added)
        ),
        CumulativeForks AS (
            SELECT
                month,
                SUM(total_forks) OVER (ORDER BY month) AS cumulative_forks
            FROM
                ForksByMonth
        )
        SELECT
            month,
            cumulative_forks
        FROM
            CumulativeForks
        ORDER BY
            month;
    """

    try:
        # Execute the query and return results
        forks_df = pd.read_sql_query(query, con=engine)
        
        # Convert 'month' to period (M) for consistent time series
        forks_df['month'] = pd.to_datetime(forks_df['month']).dt.to_period('M')
        
        return forks_df

    except Exception as e:
        logging.error(f"SQL query failed for organization {org_name}: {e}", exc_info=True)
        return pd.DataFrame(columns=['month', 'cumulative_forks'])

