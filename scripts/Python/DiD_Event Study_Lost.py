import os
import pandas as pd
import numpy as np
import linearmodels as lm
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
os.chdir(target_directory)

# Load and preprocess the data
did_data = pd.read_excel("data/DiD/final_did_dataset_log_transformed_v3.xlsx")

# Example dictionary with treatment years
treatment_dates = {
    "apache": "08.11.2023",
    "curl": "10.21.2022",
    "fortran-lang": "11.10.2022",
    "GNOME": "08.03.2023",
    "GStreamer": "10.02.2023",
    "Lullabot": "10.02.2023",
    "NLnetLabs": "10.25.2023",
    "openjs-foundation": "04.19.2023",
    "OpenMathLib": "04.19.2023",
    "openmls": "10.12.2022",
    "openpgpjs": "10.25.2022",
    "pendulum-project": "07.12.2023",
    "php": "11.17.2023",
    "prefix-dev": "10.06.2023",
    "pyca": "04.18.2023",
    "qos-ch": "04.19.2023",
    "rubygems": "10.21.2022",
    "rustls": "06.07.2023",
    "systemd": "09.14.2023",
    "tc39": "10.19.2023",
    "uutils": "10.06.2023",
    "w3c": "10.10.2023",
    "sequoia-pgp": "11.21.2022"
}


# Map these treatment years onto your DataFrame
did_data['month_treated'] = did_data['org_name'].map(treatment_dates)

# Convert dates to pandas datetime format
did_data['month_treated'] = pd.to_datetime(did_data['org_name'].map(treatment_dates))
did_data['time_period'] = pd.to_datetime(did_data['time_period'], format="%m.%d.%Y")

# Calculate the months to treatment
did_data['time_to_treatment'] = (did_data['time_period'] - did_data['month_treated']).dt.days / 30
did_data['time_to_treatment'] = did_data['time_to_treatment'].fillna(0).astype(int)


# Get dummies and exclude one period as reference (e.g., -1)
did_data = pd.get_dummies(did_data, columns=['time_to_treatment'])
did_data.drop(columns='time_to_treatment_-1', inplace=True, errors='ignore')


# Saving file
did_data.to_excel("data/DiD/final_did_dataset_log_transformed_v4.xlsx")


# Assuming the index and entity effects are properly set
did_data.set_index(['org_name', 'time_period'], inplace=True)

# Define dependent and independent variables
dependent_var = 'log_contributors'  # Change this based on your dependent variable
independent_vars = [col for col in did_data.columns if 'T_' in col]  # Treatment dummy variables
control_vars = ['age', 
                'active_repositories',  
                'running_total_open_issues', 
                'unique_pull_requests', 
                'open_pull_requests', 
                'closed_pull_requests']  # Add your control variables


# Combine all explanatory variables
exog_vars = independent_vars + control_vars

# Define the regression model
mod = PanelOLS(did_data[dependent_var], did_data[exog_vars], entity_effects=True, time_effects=True)

# Fit the model
res = mod.fit(cov_type='clustered', cluster_entity=True)

# Print the results
print(res.summary)




import os
import pandas as pd
import numpy as np
import linearmodels as lm
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt

# Define the target directory
target_directory = "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
os.chdir(target_directory)

# Load and preprocess the data
did_data = pd.read_excel("data/DiD/final_did_dataset_log_transformed_v3.xlsx")

# Example dictionary with treatment years
treatment_dates = {
    "apache": "08.11.2023",
    "curl": "10.21.2022",
    "fortran-lang": "11.10.2022",
    "GNOME": "08.03.2023",
    "GStreamer": "10.02.2023",
    "Lullabot": "10.02.2023",
    "NLnetLabs": "10.25.2023",
    "openjs-foundation": "04.19.2023",
    "OpenMathLib": "04.19.2023",
    "openmls": "10.12.2022",
    "openpgpjs": "10.25.2022",
    "pendulum-project": "07.12.2023",
    "php": "11.17.2023",
    "prefix-dev": "10.06.2023",
    "pyca": "04.18.2023",
    "qos-ch": "04.19.2023",
    "rubygems": "10.21.2022",
    "rustls": "06.07.2023",
    "systemd": "09.14.2023",
    "tc39": "10.19.2023",
    "uutils": "10.06.2023",
    "w3c": "10.10.2023",
    "sequoia-pgp": "11.21.2022"
}


# Map these treatment years onto your DataFrame
did_data['month_treated'] = did_data['org_name'].map(treatment_dates)

# Convert dates to pandas datetime format
did_data['month_treated'] = pd.to_datetime(did_data['org_name'].map(treatment_dates))
did_data['time_period'] = pd.to_datetime(did_data['time_period'], format="%m.%d.%Y")

# Calculate the time to treatment in months
did_data['time_to_treatment'] = (did_data['time_period'].dt.year - did_data['month_treated'].dt.year) * 12 + \
                                (did_data['time_period'].dt.month - did_data['month_treated'].dt.month)
did_data['time_to_treatment'] = did_data['time_to_treatment'].fillna(0).astype(int)

# Create interaction dummies and set the index
did_data = pd.get_dummies(did_data, columns=['time_to_treatment'], prefix='INX')
did_data.rename(columns=lambda x: x.replace('-', 'm'), inplace=True)
did_data.drop(columns='INX_m1', inplace=True)
did_data.set_index(['org_name', 'time_period'], inplace=True)

# Define dependent and independent variables
dependent_var = 'log_contributors'
control_vars = ['age', 'active_repositories', 'running_total_open_issues', 'unique_pull_requests', 'open_pull_requests', 'closed_pull_requests']
independent_vars = did_data.columns[did_data.columns.str.startswith('INX')]


