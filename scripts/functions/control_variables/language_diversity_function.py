#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:42:07 2024

@author: paulsharratt
"""

def get_language_diversity(org_name, engine):
    """Get the count of unique programming languages used by a GitHub organization."""
    import pandas as pd

    language_diversity_query = f"""
        SELECT
            repo_id,
            COUNT(DISTINCT programming_language) AS language_count
        FROM
            augur_data.repo_labor
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
        GROUP BY repo_id;
    """
    try:
        language_diversity_df = pd.read_sql_query(language_diversity_query, con=engine)
        return language_diversity_df
    except Exception as e:
        print(f"Failed to fetch language diversity data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
