#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:53:48 2024

@author: paulsharratt
"""

import os

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"

# Change the current working directory
os.chdir(target_directory)

import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

from scripts.Python.augur_connect import augur_db_connect
from scripts.functions.no_of_open_issues_functions import number_of_open_issues_per_month_v1, get_open_issues_per_month, get_open_issues_per_month_v2

engine = augur_db_connect("scripts/config.json")


repo_id = 193661
org_name = 'curl'
start_date = "2016-01-01"
end_date = "2024-05-01"
# save_directory = 'output/plots/org issue closure time'

curl_open_issues_v1 = number_of_open_issues_per_month_v1(org_name, start_date, end_date, engine)
curl_repo_open_issues_v1 = get_open_issues_per_month(repo_id, start_date, end_date, engine)
curl_repo_open_issues_v2 = get_open_issues_per_month_v2(repo_id, start_date, end_date, engine)

import pandas as pd


curl_open_issues_v1.to_csv('output/metrics/open_issues_curl_test.csv', index=False)

curl_repo_open_issues_v1.to_csv('output/metrics/open_issues_curl_repo_test.csv', index=False)



# it might be down to curl being in several org names...

  
"""
This doesn't quite work yet?, there's something about the cumulative totals, although the current version is much better

Or does it?

"""
