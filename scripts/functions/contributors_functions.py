#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:47:24 2024

@author: paulsharratt
"""

"""
Functions for identifying the number of contributors per organisation on GitHub:
   
"""
import pandas as pd
import logging

def number_of_contributors_per_month(org_name, start_date, end_date, engine):
    """
    Get monthly contributor frequency for a GitHub organization from the Augur database.
    This function computes the unique count of contributors per month who have active commits
    in repositories under the specified GitHub organization.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object used to execute queries.

    Returns
    -------
    pandas.DataFrame
        DataFrame with each row representing a month and the number of unique contributors in that month.
    """

    # Set up logging
    logging.basicConfig(filename='error_log.log', level=logging.ERROR, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

    # Prepare SQL query
    query = f"""
        SELECT
            DATE_TRUNC('month', CAST(cntrb_created_at AS TIMESTAMP)) AS month,
            COUNT(DISTINCT cntrb_id) AS unique_contributors
        FROM
            augur_data.contributors
        JOIN
            augur_data.commits ON augur_data.contributors.cntrb_full_name = augur_data.commits.cmt_author_name
        JOIN
            augur_data.repo ON augur_data.commits.repo_id = augur_data.repo.repo_id
        WHERE
            augur_data.repo.repo_git LIKE '%%github.com/{org_name}/%%'
            AND cntrb_created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE_TRUNC('month', CAST(cntrb_created_at AS TIMESTAMP))
        ORDER BY
            month;
    """

    try:
        # Execute SQL query
        contributors_df = pd.read_sql_query(query, con=engine)
        
        # Convert 'month' to period (M) to ensure consistency for time series analysis
        contributors_df['month'] = pd.to_datetime(contributors_df['month']).dt.to_period('M')
        
        return contributors_df

    except Exception as e:
        logging.error(f"Failed to fetch contributor data for {org_name}: {e}", exc_info=True)
        # Return an empty DataFrame on failure
        return pd.DataFrame(columns=['month', 'unique_contributors'])

