#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:51:32 2024

@author: paulsharratt
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def did_preparation(orgs_info, start_date, end_date, time_interval, engine):
    """
    Prepare data for Difference-in-Differences analysis.
    
    Parameters:
    orgs_info : list of tuples
        List of tuples where each tuple contains (org_name, treatment_start, treatment_end).
    start_date : str
        Global start date for the data collection in 'YYYY-MM-DD' format.
    end_date : str
        Global end date for the data collection in 'YYYY-MM-DD' format.
    time_interval : str
        Time interval for the data aggregation, e.g., 'M' for month, 'Q' for quarter.
    engine : sqlalchemy.engine.base.Engine
        SQL Alchemy database engine object.

    Returns:
    pd.DataFrame
        A DataFrame suitable for DiD analysis.
    """
    # Initialize an empty DataFrame to hold all aggregated data
    full_df = pd.DataFrame()

    for org_name, treatment_start, treatment_end in orgs_info:
        treatment_start = pd.to_datetime(treatment_start)
        treatment_end = pd.to_datetime(treatment_end)

        release_data = get_org_release_frequency_over_time(org_name, start_date, end_date, engine)
        release_data['time_period'] = pd.to_datetime(release_data['release_month']).dt.to_period(time_interval)
        
        org_df = pd.DataFrame({
            'time_period': pd.date_range(start=start_date, end=end_date, freq=time_interval)
        })
        org_df['time_period'] = org_df['time_period'].dt.to_period(time_interval)
        
        # Merge release data
        org_df = org_df.merge(release_data, how='left', left_on='time_period', right_on='time_period')
        org_df.fillna(0, inplace=True)  # Replace NaNs with 0s for counts

        # Set treated status
        org_df['treated'] = org_df['time_period'].apply(lambda x: 1 if treatment_start <= x.to_timestamp() <= treatment_end else 0)
        

        # Add organization identification
        org_df['org_name'] = org_name
        org_df['is_treatment_group'] = 1  # Since this function processes only treated orgs

        # Append to the full DDF
        full_df = pd.concat([full_df, org_df], ignore_index=True)
    
    # Normalize 'time_period' to start from 0
    full_df['time_period'] = (full_df['time_period'] - full_df['time_period'].min()).n

    return full_df

