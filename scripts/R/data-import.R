library(dplyr)

repo_group_data <- read.csv("/Users/paul/Documents/08 - Hertie/thesis_stf/data/raw/repo-group.csv")

repo_group_filtered <- repo_group_data %>%
  group_by(repo_id) %>%
  filter(n() == 1) %>%
  ungroup()

