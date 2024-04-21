#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:47:24 2024

@author: paulsharratt
"""
"""
Functions for identifying the number of open issues over time per organisation on GitHub:
   
"""

def number_of_open_issues_per_month(org_name, start_date, end_date, engine):
    query = f"""
        WITH initial_issues AS (
            SELECT
                COUNT(*) AS initially_open
            FROM
                augur_data.issues
            WHERE
                repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
                AND created_at < '{start_date}'
                AND (closed_at IS NULL OR closed_at > '{start_date}')
        ),
        monthly_data AS (
            SELECT
                DATE_TRUNC('month', created_at) AS month,
                COUNT(*) AS opened,
                0 AS closed
            FROM
                augur_data.issues
            WHERE
                repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
                AND created_at BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY DATE_TRUNC('month', created_at)

            UNION ALL

            SELECT
                DATE_TRUNC('month', closed_at) AS month,
                0 AS opened,
                COUNT(*) AS closed
            FROM
                augur_data.issues
            WHERE
                repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
                AND issue_state = 'closed'
                AND closed_at IS NOT NULL
                AND closed_at BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY DATE_TRUNC('month', closed_at)
        ),
        aggregated_data AS (
            SELECT
                month,
                SUM(opened) AS total_opened,
                SUM(closed) AS total_closed
            FROM
                monthly_data
            GROUP BY month
        ),
        running_totals AS (
            SELECT
                month AS issue_month,
                SUM(total_opened - total_closed) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS net_open_issues
            FROM
                aggregated_data
        )
        SELECT
            issue_month,
            (SELECT initially_open FROM initial_issues) + net_open_issues AS running_total_open_issues
        FROM
            running_totals
        ORDER BY issue_month;
    """
    import pandas as pd
    return pd.read_sql_query(query, con=engine)


