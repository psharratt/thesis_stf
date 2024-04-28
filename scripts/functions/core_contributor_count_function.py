#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:45:15 2024

@author: paulsharratt
"""

def fetch_monthly_unique_contributors(org_name, start_date, end_date, engine):
    """
    Fetches the count of unique contributors per month for a specified GitHub organization within a given timeframe.

    Parameters
    ----------
    org_name : str
        The name of the GitHub organization.
    start_date : str
        The start date for the query (inclusive), formatted as 'YYYY-MM-DD'.
    end_date : str
        The end date for the query (inclusive), formatted as 'YYYY-MM-DD'.
    engine : sqlalchemy.engine.base.Engine
        An SQLAlchemy engine instance connected to the database.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns: 'month' and 'unique_contributors', listing the number of unique contributors for each month.
    """

    query = f"""
        SELECT
            DATE_TRUNC('month', commits.cmt_committer_timestamp) AS month,
            COUNT(DISTINCT commits.cmt_author_name) AS unique_contributors
        FROM
            augur_data.commits
        WHERE
            commits.repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
            AND commits.cmt_committer_timestamp BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE_TRUNC('month', commits.cmt_committer_timestamp)
        ORDER BY
            month;
    """
    import pandas as pd
    try:
        contributors_df = pd.read_sql_query(query, con=engine)
        contributors_df['month'] = pd.to_datetime(contributors_df['month']).dt.to_period('M')
        return contributors_df
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()



