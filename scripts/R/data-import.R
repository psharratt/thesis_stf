library(dplyr)

repo_group_data <- read.csv("/Users/paulsharratt/Documents/Hertie/Semester 4/03 - Master's Thesis/thesis_stf/data/raw/repo-group.csv")

repo_group_filtered <- repo_group_data %>%
  group_by(repo_id) %>%
  filter(n() == 1) %>%
  ungroup()


repo_group_check <- repo_group_data %>%
  group_by(repo_group_id) %>%
  count()

#is it possible that I only have seven organisations in this collection?