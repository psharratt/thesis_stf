#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 17:25:00 2024

@author: paulsharratt
"""

def fetch_org_languages_over_time(engine, org_name, start_date, end_date):
    """
    Fetches the programming languages used by the repositories of a specified organization
    over a given time period, aggregated monthly.

    Parameters:
    ----------
    engine : sqlalchemy.engine.Engine
        Database connection object used to execute queries.
    org_name : str
        The GitHub organization name part of the repository URL.
    start_date : str
        The start date for the query filter (YYYY-MM-DD).
    end_date : str
        The end date for the query filter (YYYY-MM-DD).

    Returns:
    -------
    pd.DataFrame
        DataFrame containing the monthly count of different programming languages used,
        along with total lines of code for each language.
    """
    import pandas as pd
    import logging

    logging.basicConfig(level=logging.INFO, filename='language_query_log.log',
                        format='%(asctime)s:%(levelname)s:%(message)s')

    logging.info("Starting the collection of programming language data.")

    query = f"""
        SELECT
            DATE_TRUNC('month', rl_analysis_date) AS month,
            programming_language,
            SUM(code_lines) AS total_code_lines,
            COUNT(DISTINCT repo_id) AS repo_count
        FROM
            augur_data.repo_labor
        WHERE
            repo_id IN (
                SELECT repo_id FROM augur_data.repo 
                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
            )
            AND rl_analysis_date >= '{start_date}'
            AND rl_analysis_date <= '{end_date}'
            AND programming_language IS NOT NULL
        GROUP BY
            DATE_TRUNC('month', rl_analysis_date), programming_language
        ORDER BY
            month, programming_language;
    """

    try:
        # Execute the query and return results
        language_data = pd.read_sql(query, con=engine)
        
        # Convert 'month' column to datetime type to ensure consistency
        language_data['month'] = pd.to_datetime(language_data['month']).dt.to_period('M')
        
        logging.info("Successfully collected programming language data.")
        return language_data
    except Exception as e:
        logging.error(f"SQL query failed for organization {org_name}: {e}")
        print(f"SQL Error: {e}")
        return pd.DataFrame(columns=['month', 'programming_language', 'total_code_lines', 'repo_count'])


def fetch_distinct_languages_per_month(engine, org_name, start_date, end_date):
    """
    Fetches the count of distinct programming languages used by the repositories of a specified organization
    over a given time period, aggregated monthly.

    Parameters:
    ----------
    engine : sqlalchemy.engine.Engine
        Database connection object used to execute queries.
    org_name : str
        The GitHub organization name part of the repository URL.
    start_date : str
        The start date for the query filter (YYYY-MM-DD).
    end_date : str
        The end date for the query filter (YYYY-MM-DD).

    Returns:
    -------
    pd.DataFrame
        DataFrame containing the monthly count of distinct programming languages used.
    """
    import pandas as pd
    import logging

    logging.basicConfig(level=logging.INFO, filename='distinct_languages_query_log.log',
                        format='%(asctime)s:%(levelname)s:%(message)s')

    logging.info("Starting the collection of distinct programming language data.")

    query = f"""
        SELECT
            DATE_TRUNC('month', rl_analysis_date) AS month,
            COUNT(DISTINCT programming_language) AS distinct_languages
        FROM
            augur_data.repo_labor
        WHERE
            repo_id IN (
                SELECT repo_id FROM augur_data.repo 
                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
            )
            AND rl_analysis_date >= '{start_date}'
            AND rl_analysis_date <= '{end_date}'
            AND programming_language IS NOT NULL
        GROUP BY
            DATE_TRUNC('month', rl_analysis_date)
        ORDER BY
            month;
    """

    try:
        # Execute the query and return results
        language_data = pd.read_sql(query, con=engine)
        
        # Convert 'month' column to datetime type to ensure consistency
        language_data['month'] = pd.to_datetime(language_data['month']).dt.to_period('M')
        
        logging.info("Successfully collected distinct programming language data.")
        return language_data
    except Exception as e:
        logging.error(f"SQL query failed for organization {org_name}: {e}")
        print(f"SQL Error: {e}")
        return pd.DataFrame(columns=['month', 'distinct_languages'])



