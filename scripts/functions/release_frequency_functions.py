#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:26:37 2024

@author: paulsharratt
"""

def get_release_data(repo_id, start_date, end_date, engine):
    """Get release data from the Augur database.

    Parameters
    ----------
    repo_id : int
        Repository ID.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy.engine.base.Engine
        SQL Alchemy database engine object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing release dates within the specified range.
    """
    import pandas as pd

    release_query = f"""
                    SELECT
                        release_published_at AS date
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id = {repo_id} AND
                        release_published_at > '{start_date}' AND
                        release_published_at <= '{end_date}'
                    """
    try:
        releases_df = pd.read_sql_query(release_query, con=engine)
        return releases_df
    except Exception as e:
        print(f"Failed to fetch release data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure


def activity_release_data(repo_id, repo_name, org_name, start_date, end_date, engine):
    """Processes release data for the specified repository and time frame.

    Parameters
    ----------
    repo_id : int
        Repository ID.
    repo_name : str
        Repository name.
    org_name : str
        Organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy.engine.base.Engine
        SQL Alchemy database engine object.

    Returns
    -------
    tuple
        Contains error code, error text, DataFrame of releases, start date, end date, title, interpretation, and number of releases.
    """
    from datetime import datetime, timedelta
    import pandas as pd

    try:
        releases_df = get_release_data(repo_id, start_date, end_date, engine)
        if releases_df.empty:
            raise ValueError("No data returned for the specified repository and date range.")

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        six_mos_dt = end_dt - timedelta(days=180)

        release_num = releases_df.loc[(releases_df['date'] >= six_mos_dt) & (releases_df['date'] <= end_dt)].shape[0]

        if release_num == 0:
            raise ValueError("No releases in the past 6 months.")

        title = f"{org_name}/{repo_name} Release Frequency: {release_num} releases in the past 6 months."
        interpretation = "Interpretation: Healthy projects will have frequent releases with security updates, bug fixes, and features."

        return 0, None, releases_df, start_dt, end_dt, title, interpretation, release_num
    except Exception as e:
        return -1, str(e), None, None, None, None, None, None

def get_aggregated_release_data(repo_ids, start_date, end_date, engine):
    """Get aggregated release data for multiple repositories per org from the Augur database.

    Parameters
    ----------
    repo_ids : list of int
        List of repository IDs.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing aggregated release dates across specified repositories.
    """
    import pandas as pd

    repo_ids_tuple = tuple(repo_ids)  # Ensure it's a tuple to use in SQL query

    release_query = f"""
                    SELECT
                        repo_id, COUNT(*) AS release_count
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id IN {repo_ids_tuple}
                        AND release_published_at > '{start_date}'
                        AND release_published_at <= '{end_date}'
                    GROUP BY repo_id
                    """
    try:
        releases_df = pd.read_sql_query(release_query, con=engine)
        return releases_df
    except Exception as e:
        print(f"Failed to fetch release data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    
def get_org_release_data(org_name, start_date, end_date, engine):
    """Get aggregated release data for all repositories under a specific GitHub organization from the Augur database.

    Parameters
    ----------
    organization_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing aggregated release dates across specified repositories.
    """
    import pandas as pd

    release_query = f"""
                    SELECT
                        repo_id, COUNT(*) AS release_count
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id IN (
                            SELECT repo_id
                            FROM augur_data.repo
                            WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                        )
                        AND release_published_at > '{start_date}'
                        AND release_published_at <= '{end_date}'
                    GROUP BY repo_id
                    """
    try:
        releases_df = pd.read_sql_query(release_query, con=engine)
        return releases_df
    except Exception as e:
        print(f"Failed to fetch release data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure


def get_org_release_frequency(org_name, start_date, end_date, engine):
    """Get total release count for a GitHub organization from the Augur database.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object.

    Returns
    -------
    int
        Total count of releases across all repositories of the organization within the specified time range.
    """
    import pandas as pd

    release_query = f"""
                    SELECT
                        COUNT(*) AS total_releases
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id IN (
                            SELECT repo_id
                            FROM augur_data.repo
                            WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                        )
                        AND release_published_at > '{start_date}'
                        AND release_published_at <= '{end_date}'
                    """
    try:
        result = pd.read_sql_query(release_query, con=engine)
        return result.iloc[0]['total_releases']
    except Exception as e:
        print(f"Failed to fetch release data: {e}")
        return 0  # Return 0 releases on failure


def get_org_release_frequency_over_time(org_name, start_date, end_date, engine):
    """Get monthly release frequency for a GitHub organization from the Augur database.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    engine : sqlalchemy object
        Database connection object.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the count of releases per month.
    """
    import pandas as pd

    release_query = f"""
                    SELECT
                        DATE_TRUNC('month', release_published_at) AS release_month,
                        COUNT(*) AS release_count
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id IN (
                            SELECT repo_id
                            FROM augur_data.repo
                            WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                        )
                        AND release_published_at > '{start_date}'
                        AND release_published_at <= '{end_date}'
                    GROUP BY DATE_TRUNC('month', release_published_at)
                    ORDER BY release_month
                    """
    try:
        release_freq_df = pd.read_sql_query(release_query, con=engine)
        return release_freq_df
    except Exception as e:
        print(f"Failed to fetch release frequency data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure


def plot_org_release_frequency(org_name, start_date, end_date, engine, save_dir):
    """Fetch release data and plot the release frequency for a specified organization."""
    release_query = f"""
                    SELECT
                        DATE_TRUNC('month', release_published_at) AS release_month,
                        COUNT(*) AS release_count
                    FROM
                        augur_data.releases
                    WHERE 
                        repo_id IN (
                            SELECT repo_id
                            FROM augur_data.repo
                            WHERE repo_git LIKE '%%github.com/{org_name}/%%'
                        )
                        AND release_published_at >= '{start_date}'
                        AND release_published_at <= '{end_date}'
                    GROUP BY 1
                    ORDER BY 1
                    """
    import os
    import pandas as pd
    try:
        release_freq_df = pd.read_sql_query(release_query, con=engine)
        if release_freq_df.empty:
            print(f"No data found for {org_name}")
            return
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 6))
        plt.plot(release_freq_df['release_month'], release_freq_df['release_count'], marker='o', linestyle='-')
        plt.title(f'Monthly Release Frequency for {org_name}')
        plt.xlabel('Month')
        plt.ylabel('Number of Releases')
        plt.grid(True)
        plt.xticks(rotation=45)
        
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(f'{save_dir}/{org_name}_release_frequency.png')
        plt.close()
        print(f'Plot saved for {org_name}')
    except Exception as e:
        print(f"Error processing {org_name}: {e}")

def calculate_release_frequencies(org_name, investment_start_date, investment_end_date, engine):
    """Calculate average monthly release frequency before, during, and after the investment period.

    Parameters
    ----------
    org_name : str
        Name of the GitHub organization.
    investment_start_date : datetime
        Start date of the investment period.
    investment_end_date : datetime
        End date of the investment period.
    engine : sqlalchemy engine object
        Database connection object.

    Returns
    -------
    dict
        Dictionary containing formatted average release frequencies for 'before', 'during', and 'after' investment periods.
    """
    import pandas as pd
    import numpy as np

    query = f"""
        SELECT
            DATE_TRUNC('month', release_published_at) AS release_month,
            COUNT(*) AS release_count
        FROM
            augur_data.releases
        WHERE
            repo_id IN (
                SELECT repo_id
                FROM augur_data.repo
                WHERE repo_git LIKE '%%github.com/{org_name}/%%'
            )
        GROUP BY 1
        ORDER BY 1
    """
    try:
        releases_df = pd.read_sql_query(query, con=engine)
        if releases_df.empty:
            return {'before': 'NA', 'during': 'NA', 'after': 'NA'}
        
        # Convert release_month to datetime
        releases_df['release_month'] = pd.to_datetime(releases_df['release_month'])
        
        # Define periods
        before_period = releases_df[releases_df['release_month'] < investment_start_date]
        during_period = releases_df[(releases_df['release_month'] >= investment_start_date) & (releases_df['release_month'] <= investment_end_date)]
        after_period = releases_df[releases_df['release_month'] > investment_end_date]
        
        # Calculate average releases per month and round to 2 decimal places
        averages = {
            'before': np.round(before_period['release_count'].mean() if not before_period.empty else 0, 2),
            'during': np.round(during_period['release_count'].mean() if not during_period.empty else 0, 2),
            'after': np.round(after_period['release_count'].mean() if not after_period.empty else 0, 2)
        }
        
        return averages
    except Exception as e:
        print(f"Error processing {org_name}: {e}")
        return {'before': 'Error', 'during': 'Error', 'after': 'Error'}

