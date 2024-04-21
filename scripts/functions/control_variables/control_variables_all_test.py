#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:12:08 2024

@author: paulsharratt
"""


import os

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)


from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.control_variables.no_of_repos_over_time_function import number_of_repos_per_month
from scripts.functions.control_variables.number_of_forks_per_month_function import number_of_forks_per_month
from scripts.functions.control_variables.fetch_org_languages_over_time_function import fetch_org_languages_over_time, fetch_distinct_languages_per_month
from scripts.functions.control_variables.number_of_PRs_per_month_function import fetch_pull_request_data, fetch_pull_request_metrics
from scripts.functions.control_variables.number_of_PRs_per_month_function import fetch_pull_request_data, fetch_pull_request_metrics

from scripts.functions.control_variables.calculate_org_age_function import calculate_org_age_from_first_release

engine = augur_db_connect("scripts/config.json")  # Ensure you have a function to connect to your database

repo_id = 193661
org_name = 'curl'
start_date = "2014-01-01"
end_date = "2024-05-01"



curl_no_of_repos = number_of_repos_per_month(org_name, start_date, end_date, engine)

curl_no_of_forks = number_of_forks_per_month(org_name, start_date, end_date, engine)

curl_language_data = fetch_org_languages_over_time(engine, org_name, start_date, end_date)

curl_distinct_language_data = fetch_distinct_languages_per_month(engine, org_name, start_date, end_date)

curl_PRs_per_month_fetch = fetch_pull_request_metrics(org_name, start_date, end_date, engine)

curl_age = calculate_org_age_from_first_release(org_name, start_date, end_date, engine)



print(curl_distinct_language_data)

print(curl_language_data)

print(curl_no_of_repos)

print(curl_no_of_forks)

print(curl_PRs_per_month_fetch)


#number_of_repos_per_month,