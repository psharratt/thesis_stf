#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:47:24 2024

@author: paulsharratt
"""

"""
Functions for identifying the number of contributors per organisation on GitHub:
   
"""
def number_of_contributors_per_month(org_name, start_date, end_date, engine):
    """Get monthly contributor frequency for a GitHub organization from the Augur database by matching full names."""
    query = f"""
        SELECT
            DATE_TRUNC('month', CAST(cntrb_created_at AS TIMESTAMP)) AS month,
            COUNT(DISTINCT cntrb_id) AS unique_contributors
        FROM
            augur_data.contributors
        WHERE
            cntrb_created_at BETWEEN '{start_date}' AND '{end_date}'
            AND cntrb_full_name IN (
                SELECT DISTINCT cmt_author_name
                FROM augur_data.commits
                WHERE repo_id IN (
                    SELECT repo_id
                    FROM augur_data.repo
                    WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                )
            )
        GROUP BY DATE_TRUNC('month', CAST(cntrb_created_at AS TIMESTAMP))
        ORDER BY month;
    """
    import pandas as pd
    try:
        contributors_df = pd.read_sql_query(query, con=engine)
        contributors_df['month'] = pd.to_datetime(contributors_df['month']).dt.to_period('M')
        return contributors_df
    except Exception as e:
        print(f"Failed to fetch contributor data for {org_name}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
