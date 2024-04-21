#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:49:02 2024

@author: paulsharratt
"""

def get_org_repo_info_extended(org_name, engine):
    """
    Retrieves aggregated repository information for a specific GitHub organization.
    
    Parameters
    ----------
    org_name : str
        GitHub organization name.
    engine : sqlalchemy database object
        Database connection object used to execute queries.

    Returns
    -------
    org_repo_info : DataFrame
        DataFrame containing aggregated repository statistics for the organization.
    """
    import pandas as pd
    import logging

    # Set up logging
    logging.basicConfig(filename='repo_info_error_log.log', level=logging.ERROR, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

    try:
        query = f"""
            SELECT
                MIN(repo.created_at) AS first_project_start_date,
                SUM(repo.forks_count) AS total_number_of_forks,
                SUM(repo.stargazers_count) AS total_number_of_stars,
                ARRAY_AGG(DISTINCT repo.language) FILTER (WHERE repo.language IS NOT NULL) AS languages_used,
                COUNT(repo.repo_id) FILTER (WHERE repo.repo_archived = 'True') AS count_archived_repos,
                COUNT(repo.repo_id) FILTER (WHERE repo.forked_from IS NOT NULL) AS count_forked_repos
            FROM
                augur_data.repo
            JOIN
                augur_data.repo_groups ON repo.repo_group_id = repo_groups.repo_group_id
            WHERE
                LOWER(repo_groups.rg_name) = LOWER('{org_name}')
            GROUP BY repo_groups.rg_name;
            """

        org_repo_info = pd.read_sql_query(query, con=engine)
        return org_repo_info

    except Exception as e:
        logging.error(f"Database query failed for organization {org_name}: {e}", exc_info=True)
        return pd.DataFrame()  # Return an empty DataFrame on failure
