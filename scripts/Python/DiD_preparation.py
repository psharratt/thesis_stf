#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 21:52:47 2024

@author: paulsharratt
"""

"""
In progress:
    S

"""

def merge_metric_dataframes(release_freq_df, issue_response_df, contributor_load_df):
    """Merge individual metric dataframes into a single dataframe for DiD analysis."""
    # Merge on the 'month' column which needs to be present in all dataframes
    from functools import reduce
    data_frames = [release_freq_df, issue_response_df, contributor_load_df]
    did_data = reduce(lambda left, right: pd.merge(left, right, on=["release_month"], how="outer"), data_frames)
    did_data = did_data.rename(columns={'release_month': 'time_period'})
    return did_data



# Assuming `did_data` is the merged DataFrame
did_data.to_csv('data/processed/did_dataset.csv', index=False)
did_data.to_excel('data/processed/did_dataset.xlsx', index=False)
