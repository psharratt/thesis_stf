install.packages("jsonlite")
install.packages("ggplot2")  # or any other visualization package you prefer

library(jsonlite)
json_data <- fromJSON("/Users/paulsharratt/Documents/Hertie/Semester 3/06 - Master's Thesis/thesis_stf/data/raw/fortran_test/fortran-lang-repos-postman.json")



# This step heavily depends on the structure of your JSON file.
df <- as.data.frame(json_data)


# data processing
library(tidyverse)

selected_df <- df %>%
  select(id, name, full_name, html_url, description)

# View the resulting data frame
print(selected_df)

# presenting the DF
install.packages("gridExtra")
install.packages("ggplot2")

library(gridExtra)
library(ggplot2)
table_plot <- tableGrob(selected_df)
png("selected_df.png", width = 800, height = 600)  # Adjust the size as needed
grid.draw(table_plot)
dev.off()  # Close the PNG device

fortran_lang_repos_postman <- head(selected_df)


