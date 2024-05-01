# Install and load packages
library(jsonlite)
library(RPostgreSQL)

# Set working directory and base path
base_path <- "/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/"
setwd(base_path)

# Pulling config file 
config_path <- "config.json"

# Read the config file
config <- fromJSON(config_path)

# Connect to the database using the configuration list
conn <- dbConnect(RPostgreSQL::PostgreSQL(),
                  dbname = config$database,
                  host = config$host,
                  port = config$port,
                  user = config$user,
                  password = config$password)

