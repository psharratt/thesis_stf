#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:45:15 2024

@author: paulsharratt
"""

def get_core_contributor_count(org_name, start_date, end_date, engine):
    """Get monthly count of core contributors for a GitHub organization."""
    import pandas as pd

    core_contributors_query = f"""
        SELECT
            DATE_TRUNC('month', contributors.created_at) AS month,
            COUNT(DISTINCT cntrb_id) AS core_contributors
        FROM
            augur_data.contributors
        WHERE
            repo_id IN (
                SELECT repo_id
                FROM augur_data.repo
                WHERE repo_group_id IN (
                    SELECT repo_group_id
                    FROM augur_data.repo_groups
                    WHERE rg_name = '{org_name}'
                )
            )
            AND created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY DATE_TRUNC('month', contributors.created_at)
        ORDER BY month;
    """
    try:
        core_contributors_df = pd.read_sql_query(core_contributors_query, con=engine)
        return core_contributors_df
    except Exception as e:
        print(f"Failed to fetch core contributor data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
