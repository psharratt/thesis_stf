

def fetch_pull_request_data(org_name, start_date, end_date, engine):
    """
    Fetch monthly pull request data for a GitHub organization from the Augur database.
    This function computes both the open and closed pull requests, as well as the count of unique pull requests per month.

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
        DataFrame with each row representing a month, including counts of open and closed, and unique pull requests.
    """
    import pandas as pd
    import logging
    # Set up logging
    logging.basicConfig(filename='pull_request_data_log.log', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

    logging.info("Starting the pull request data retrieval process.")

    # SQL query for open and closed pull requests
    query_open_closed = f"""
        SELECT
            DATE_TRUNC('month', pr_created_at) AS month,
            SUM(CASE WHEN pr_closed_at IS NULL THEN 1 ELSE 0 END) AS open_pull_requests,
            SUM(CASE WHEN pr_closed_at IS NOT NULL THEN 1 ELSE 0 END) AS closed_pull_requests
        FROM
            augur_data.pull_requests
        WHERE
            repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%github.com/{org_name}/%')
            AND pr_created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE_TRUNC('month', pr_created_at)
        ORDER BY
            month;
    """

    # SQL query for unique pull requests
    query_unique_prs = f"""
        SELECT
            DATE_TRUNC('month', pr_created_at) AS month,
            COUNT(DISTINCT pr_html_url) AS unique_pull_requests
        FROM
            augur_data.pull_requests
        WHERE
            pr_html_url LIKE '%github.com/{org_name}/%'
            AND pr_created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE_TRUNC('month', pr_created_at)
        ORDER BY
            month;
    """

    try:
        # Execute SQL queries
        data_open_closed = pd.read_sql_query(query_open_closed, con=engine)
        data_unique_prs = pd.read_sql_query(query_unique_prs, con=engine)
        
        # Merge the two dataframes on 'month'
        result = pd.merge(data_open_closed, data_unique_prs, on='month', how='outer')

        # Convert 'month' to period (M) to ensure consistency for time series analysis
        result['month'] = pd.to_datetime(result['month']).dt.to_period('M')

        logging.info("Successfully retrieved pull request data.")
        return result

    except Exception as e:
        logging.error(f"Failed to fetch pull request data for {org_name}: {e}", exc_info=True)
        # Return an empty DataFrame on failure
        return pd.DataFrame(columns=['month', 'open_pull_requests', 'closed_pull_requests', 'unique_pull_requests'])




def fetch_pull_request_metrics(org_name, start_date, end_date, engine):
    """
    Fetches monthly pull request metrics for a GitHub organization from the Augur database.
    Computes the number of unique pull requests, and categorizes them into open and closed.

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
        DataFrame with each row representing a month, the count of unique pull requests, 
        and the counts of open and closed pull requests in that month.
    """
    import pandas as pd
    import logging
    # Set up logging
    logging.basicConfig(filename='pull_request_metrics_log.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    # Prepare SQL query for unique pull requests
    unique_pr_query = f"""
        SELECT
            DATE_TRUNC('month', pr_created_at) AS month,
            COUNT(DISTINCT pr_html_url) AS unique_pull_requests
        FROM
            augur_data.pull_requests
        WHERE
            pr_html_url LIKE '%%github.com/{org_name}/%%'
            AND pr_created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            month
        ORDER BY
            month;
    """

    # Prepare SQL query for open and closed pull requests
    open_closed_pr_query = f"""
        SELECT
            DATE_TRUNC('month', pr_created_at) AS month,
            SUM(CASE WHEN pr_closed_at IS NULL THEN 1 ELSE 0 END) AS open_pull_requests,
            SUM(CASE WHEN pr_closed_at IS NOT NULL THEN 1 ELSE 0 END) AS closed_pull_requests
        FROM
            augur_data.pull_requests
        WHERE
            repo_id IN (SELECT repo_id FROM augur_data.repo WHERE repo_git LIKE '%%github.com/{org_name}/%%')
            AND pr_created_at BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            month
        ORDER BY
            month;
    """

    try:
        # Execute SQL queries
        unique_pr_df = pd.read_sql_query(unique_pr_query, con=engine)
        open_closed_pr_df = pd.read_sql_query(open_closed_pr_query, con=engine)

        # Merge the dataframes on the 'month' column
        merged_df = pd.merge(unique_pr_df, open_closed_pr_df, on='month', how='outer')

        # Convert 'month' to period (M) to ensure consistency for time series analysis
        merged_df['month'] = pd.to_datetime(merged_df['month']).dt.to_period('M')

        logging.info("Successfully retrieved pull request metrics.")
        return merged_df

    except Exception as e:
        logging.error(f"Failed to fetch pull request metrics for {org_name}: {e}", exc_info=True)
        # Return an empty DataFrame on failure
        return pd.DataFrame(columns=['month', 'unique_pull_requests', 'open_pull_requests', 'closed_pull_requests'])

