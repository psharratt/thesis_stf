#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:51:32 2024

@author: paulsharratt
"""


def did_preparation(orgs_info, global_start_date, global_end_date, time_interval, engine):
    """
    Prepare data for Difference-in-Differences analysis by aggregating data over specified time intervals.

    Parameters:
    orgs_info : list of tuples
        Each tuple contains ('org_name', 'treatment_start_date', 'treatment_end_date').
    global_start_date : str
        Global start date for the data collection in 'YYYY-MM-DD' format.
    global_end_date : str
        Global end date for the data collection in 'YYYY-MM-DD' format.
    time_interval : str
        Time interval for the data aggregation, e.g., 'M' for month, 'Q' for quarter.
    engine : sqlalchemy.engine.base.Engine
        SQL Alchemy database engine object.

    Returns:
    pd.DataFrame
        A DataFrame suitable for DiD analysis.
    """
    import pandas as pd
    from scripts.functions.release_frequency_functions import get_org_release_frequency_over_time
    full_df = pd.DataFrame()

    for org_name, treatment_start, treatment_end in orgs_info:
        treatment_start = pd.to_datetime(treatment_start)
        treatment_end = pd.to_datetime(treatment_end)

        # Generating date range for the org based on global dates
        date_range = pd.date_range(start=global_start_date, end=global_end_date, freq=time_interval)
        org_df = pd.DataFrame(date_range, columns=['date'])
        org_df['time_period'] = (org_df['date'] - pd.to_datetime(global_start_date)).dt.days // 30  # example for monthly

        release_data = get_org_release_frequency_over_time(org_name, global_start_date, global_end_date, engine)
        release_data['time_period'] = pd.to_datetime(release_data['release_month']).dt.to_period('M').view(int)

        # Merge and cleanup
        org_df = org_df.merge(release_data, on='time_period', how='left')
        
        # Fill missing data 
        num_cols = org_df.select_dtypes(include=['float64', 'int']).columns
        org_df[num_cols] = org_df[num_cols].fillna(0)  # Replace NaNs in numeric columns with 0s
        date_cols = org_df.select_dtypes(include=['datetime64[ns]']).columns
        org_df[date_cols] = org_df[date_cols].fillna(pd.Timestamp('1970-01-01'))  # Example, replace NaNs in datetime columns if any

        # Seting 'treated' status based on date
        org_df['treated'] = org_df['date'].apply(lambda x: 1 if treatment_start <= x <= treatment_end else 0)

        # Add organization info
        org_df['org_name'] = org_name
        org_df['is_treatment_group'] = 1

        # Append to full DataFrame
        full_df = pd.concat([full_df, org_df], ignore_index=True)

    # Adjust 'time_period' index to start from 0 
    full_df['time_period'] -= full_df['time_period'].min()

    return full_df

