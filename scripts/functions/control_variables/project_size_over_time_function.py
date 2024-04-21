#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:40:50 2024

@author: paulsharratt
"""

def get_project_size_over_time(org_name, start_date, end_date, engine):
    """Get the sum of the lines of code (LOC) per month for a GitHub organization."""
    import pandas as pd
    
    project_size_query = f"""
        SELECT
            DATE_TRUNC('month', commits.cmt_author_date) AS month,
            SUM(commit_changes.lines_added + commit_changes.lines_removed) AS total_changes
        FROM
            augur_data.commits
        JOIN
            augur_data.commit_changes ON commits.cmt_id = commit_changes.cmt_id
        WHERE
            commits.repo_id IN (
                SELECT repo_id
                FROM augur_data.repo
                WHERE repo_group_id IN (
                    SELECT repo_group_id
                    FROM augur_data.repo_groups
                    WHERE rg_name = '{org_name}'
                )
            )
            AND commits.cmt_author_date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE_TRUNC('month', commits.cmt_author_date)
        ORDER BY month;
    """
    try:
        project_size_df = pd.read_sql_query(project_size_query, con=engine)
        return project_size_df
    except Exception as e:
        print(f"Failed to fetch project size data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure


