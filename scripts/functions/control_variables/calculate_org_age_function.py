#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:36:58 2024

@author: paulsharratt
"""

def calculate_org_age_from_first_release(org_name, start_date, end_date, engine):
    """
    Calculates the monthly age of a GitHub organization from its first release,
    counting from the first release and displaying from the specified start date.

    Parameters
    ----------
    org_name : str
        GitHub organization name.
    start_date : str
        Start date in YYYY-MM-DD format for starting the display of the age.
    end_date : str
        End date in YYYY-MM-DD format for ending the display of the age.
    engine : sqlalchemy object
        Database connection object used to execute queries.

    Returns
    -------
    pandas.DataFrame
        DataFrame with 'month' and 'age' columns, representing the cumulative age of the organization each month starting from its first release.
    """
    # SQL query to find the earliest release date
    release_query = f"""
        SELECT MIN(release_published_at) as first_release_date
        FROM augur_data.releases
        WHERE release_url LIKE '%%github.com/{org_name}/%%';
    """
    import pandas as pd
    
    # Execute the query
    release_data = pd.read_sql_query(release_query, con=engine)
    first_release_date = release_data.iloc[0]['first_release_date']

    if pd.isnull(first_release_date):
        raise ValueError(f"No valid first release date found for {org_name}. Ensure the org name is correct and releases exist within the DB.")

    # Convert dates from string to period (monthly frequency)
    first_release_period = pd.Period(first_release_date, freq='M')
    start_period = pd.Period(start_date, freq='M')
    end_period = pd.Period(end_date, freq='M')

    # Generate periods from the first release to the specified end date
    all_periods = pd.period_range(start=first_release_period, end=end_period, freq='M')
    display_periods = pd.period_range(start=start_period, end=end_period, freq='M')

    # Calculate age for each month from the first release
    all_ages = [(period - first_release_period).n + 1 for period in all_periods]

    # Prepare the final DataFrame to display ages from the start_date onwards
    age_df = pd.DataFrame({
        'month': [period.strftime('%Y-%m') for period in all_periods],
        'age': all_ages
    })

    # Filter to display from the start_date onwards
    age_df = age_df[age_df['month'].isin([period.strftime('%Y-%m') for period in display_periods])]

    return age_df
    