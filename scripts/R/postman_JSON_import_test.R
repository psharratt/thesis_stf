simon_munzert_repo_commits <- read.csv("/Users/paul/Documents/08 - Hertie/thesis_stf/data/raw/simon_munzert_test/simon_munzert_test_repo_commits.csv")

simon_munzert_repo_commits_processed <- simon_munzert_repo_commits[, c("commit.author.name", "commit.author.date", "commit.committer.date", "commit.message", "url")]

colnames(simon_munzert_repo_commits_processed) <- c("Author Name", "Author Date", "Committer Date", "Message", "URL")



# Specify the full path for the output CSV file
output_file <- "/Users/paul/Documents/08 - Hertie/thesis_stf/data/processed/simon_munzert_repo_commits_processed.csv"

# Write the processed data to the specified CSV file
write.csv(simon_munzert_repo_commits_processed, output_file, row.names = FALSE)
