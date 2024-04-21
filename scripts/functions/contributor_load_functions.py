#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:49:05 2024

@author: paulsharratt
"""

"""
Functions for identifying the contributor load per organisation on GitHub:
    no. of commits per major contributor
"""


def get_org_contributor_load_over_time(org_name, start_date, end_date, engine):
    """Get average contributor load per month for a GitHub organization."""
    import pandas as pd

    contributor_query = f"""
                        SELECT
                            DATE_TRUNC('month', CAST(cmt_author_date AS TIMESTAMP)) AS commit_month,
                            COUNT(DISTINCT cmt_author_name) AS num_contributors,
                            COUNT(*) AS total_commits
                        FROM
                            augur_data.commits
                        WHERE 
                            repo_id IN (
                                SELECT repo_id
                                FROM augur_data.repo
                                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                            )
                            AND cmt_author_date <> ''  -- Exclude empty strings
                            AND cmt_author_date IS NOT NULL  -- Ensure no NULL values are present
                            AND CAST(cmt_author_date AS DATE) >= '{start_date}'
                            AND CAST(cmt_author_date AS DATE) <= '{end_date}'
                        GROUP BY DATE_TRUNC('month', CAST(cmt_author_date AS TIMESTAMP))
                        ORDER BY commit_month
                        """
    try:
        contributor_load_df = pd.read_sql_query(contributor_query, con=engine)
        contributor_load_df['avg_commits_per_contributor'] = contributor_load_df['total_commits'] / contributor_load_df['num_contributors']
        return contributor_load_df[['commit_month', 'avg_commits_per_contributor']]
    except Exception as e:
        print(f"Failed to fetch contributor load data for {org_name}: {e}")
        return pd.DataFrame()

