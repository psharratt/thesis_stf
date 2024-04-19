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



def get_open_issues_per_month(repo_id, start_date, end_date, engine):
    """
    Calculate the number of open issues at the end of each month for a specific GitHub repository.

    Parameters:
    - repo_id: int, the repository ID.
    - start_date: str, start date in 'YYYY-MM-DD' format.
    - end_date: str, end date in 'YYYY-MM-DD' format.
    - engine: sqlalchemy engine object, database connection object.

    Returns:
    - pandas.DataFrame containing the count of open issues at the end of each month.
    """
    query = f"""
        WITH monthly_events AS (
            SELECT
                DATE_TRUNC('month', created_at) AS month,
                COUNT(*) AS issues_opened,
                0 AS issues_closed
            FROM
                augur_data.issues
            WHERE
                repo_id = {repo_id}
                AND created_at BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY DATE_TRUNC('month', created_at)

            UNION ALL

            SELECT
                DATE_TRUNC('month', closed_at) AS month,
                0 AS issues_opened,
                COUNT(*) AS issues_closed
            FROM
                augur_data.issues
            WHERE
                repo_id = {repo_id}
                AND issue_state = 'closed'
                AND closed_at IS NOT NULL
                AND closed_at BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY DATE_TRUNC('month', closed_at)
        ),
        cumulative_totals AS (
            SELECT
                month,
                SUM(issues_opened - issues_closed) OVER (ORDER BY month) AS running_open_issues
            FROM
                monthly_events
        )
        SELECT
            month AS issue_month,
            MAX(running_open_issues) AS open_issues_count  -- Ensures no negative counts
        FROM
            cumulative_totals
        GROUP BY month
        ORDER BY month;
    """
    import pandas as pd
    return pd.read_sql_query(query, con=engine)


# 8Knot version - try this!

def get_open_issues_per_month_v2(repo_id, start_date, end_date, engine):
    """Returns a time series of the count of open issues per month for a specific repository.

    Parameters
    ----------
    repo_id : int
        The repository's repo_id.
    start_date : str
        Start date in 'YYYY-MM-DD' format.
    end_date : str
        End date in 'YYYY-MM-DD' format.
    engine : sqlalchemy engine object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the count of open issues per month.
    """
    from sqlalchemy import text
    query = text("""
        WITH monthly_issues AS (
            SELECT
                DATE_TRUNC('month', created_at) AS month,
                COUNT(issue_id) AS issues_opened,
                0 AS issues_closed
            FROM
                augur_data.issues
            WHERE
                repo_id = :repo_id
                AND created_at >= :start_date
                AND created_at <= :end_date
            GROUP BY 1

            UNION ALL

            SELECT
                DATE_TRUNC('month', closed_at) AS month,
                0 AS issues_opened,
                COUNT(issue_id) AS issues_closed
            FROM
                augur_data.issues
            WHERE
                repo_id = :repo_id
                AND issue_state = 'closed'
                AND closed_at IS NOT NULL
                AND closed_at >= :start_date
                AND closed_at <= :end_date
            GROUP BY 1
        ),
        aggregated_data AS (
            SELECT
                month,
                SUM(issues_opened) AS opened,
                SUM(issues_closed) AS closed
            FROM
                monthly_issues
            GROUP BY month
        ),
        cumulative_issues AS (
            SELECT
                month AS issue_month,
                SUM(opened - closed) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_open_issues
            FROM
                aggregated_data
        )
        SELECT
            issue_month,
            running_open_issues
        FROM
            cumulative_issues
        ORDER BY issue_month;
    """)
    import pandas as pd
    result = pd.read_sql_query(query, engine, params={
        'repo_id': repo_id,
        'start_date': start_date,
        'end_date': end_date
    })

    return result
