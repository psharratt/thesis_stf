

process_and_save_data <- function(input_file) {
  # Read the input CSV file into a dataframe
  original_data <- read.csv(input_file)
  
  # Select specific columns
  selected_columns <- original_data[, c("commit.author.name", "commit.author.date", "commit.committer.date", "commit.message", "url")]
  
  # Rename the selected columns
  colnames(selected_columns) <- c("author_name", "author_date", "committer_date", "message", "url")
  
  # Specify the full path for the output CSV file
  output_file <- "/Users/paul/Documents/08 - Hertie/thesis_stf/data/processed_data.csv"
  
  # Write the processed data to the specified CSV file
  write.csv(selected_columns, output_file, row.names = FALSE)
  
  cat("Data processing and saving complete.\n")
}

