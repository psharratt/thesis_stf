# Load the necessary libraries
library(plotly)
library(tidyr)
library(readxl)
library(ggplot2)


fortran <- read_excel("~/Documents/08 - Hertie/thesis_stf/data/raw/fortran_test/fortran_fpm_pushes_commits.xlsx")

#### option ####

# Contract start and end dates (in "YYYY-MM-DD" format)
contract_start <- as.Date("2023-04-01")  # April 1, 2023
contract_end <- as.Date("2023-06-30")    # June 30, 2023

fortran_ed <- fortran %>%
  select(-stf)

# Filter the data to start from January 2022
fortran_filtered <- fortran_ed[fortran_ed$event_month >= as.Date("2022-01-01"), ]

# Create the time series plot
fortran_plotly_ts_2 <- ts_plot(fortran_filtered,
                             title = "Fortran FPM Monthly Pushes and Commits with Contract",
                             Xtitle = "Time",
                             Ytitle = "Billion Cubic Feet",
                             slider = TRUE,
                             Xgrid = TRUE,
                             Ygrid = TRUE) %>%
  
  # Add vertical line for contract start
  add_lines(x = list(x = contract_start, x = contract_start), 
            y = list(y = -Inf, y = Inf),
            line = list(color = "green", dash = "dash"),
            name = "Contract Start") %>%
  
  layout(paper_bgcolor = "white",
         plot_bgcolor = "white",
         font = list(color = "black"),
         yaxis = list(linecolor = "#6b6b6b",
                      zerolinecolor = "#6b6b6b",
                      gridcolor = "#444444"),
         xaxis = list(linecolor = "#6b6b6b",
                      zerolinecolor = "#6b6b6b",
                      gridcolor = "#444444"))

fortran_plotly_ts_2


#### other option ####


# Create period to hold the 3 months of 2015
period <- c("2023-04-01/2023-07-01")

# Highlight the first three months of 2015 
chart.TimeSeries(fortran$event_month, period.areas = period)

# Highlight the first three months of 2015 in light grey
chart.TimeSeries(data$citigroup, period.areas = period, period.color = "lightgrey")


##### another option #####


# Load the necessary libraries
library(plotly)
library(tidyr)

# Contract start and end dates (in "YYYY-MM-DD" format)
contract_start <- as.Date("2023-04-01")  # April 1, 2023
contract_end <- as.Date("2023-07-01")    # July 1, 2023

# Filter the data to start from January 2022
fortran_filtered <- fortran[fortran$event_month >= as.Date("2022-01-01"), ]

# Create the time series plot
fortran_plotly_ts <- ts_plot(fortran_filtered,
                             title = "Fortran FPM Monthly Pushes and Commits with Contract Duration",
                             Xtitle = "Time",
                             Ytitle = "Billion Cubic Feet",
                             slider = TRUE,
                             Xgrid = TRUE,
                             Ygrid = TRUE)

# Add a rectangle to highlight the contract duration
fortran_plotly_ts <- fortran_plotly_ts %>%
  add_rect(
    x0 = contract_start,
    x1 = contract_end,
    y0 = -Inf,
    y1 = Inf,
    fillcolor = "lightgrey",
    opacity = 0.3,
    line = list(width = 0)
  )

# Adjust the appearance of the plot
fortran_plotly_ts <- layout(fortran_plotly_ts,
                            paper_bgcolor = "white",
                            plot_bgcolor = "white",
                            font = list(color = "black"),
                            yaxis = list(linecolor = "grey",
                                         zerolinecolor = "grey",
                                         gridcolor = "grey"),
                            xaxis = list(linecolor = "grey",
                                         zerolinecolor = "grey",
                                         gridcolor = "grey"))

fortran_plotly_ts






#### BEST option ####

# Your existing code to create the plot
fig <- plot_ly(fortran, x = ~event_month, y = ~pushes, name = "Pushes", type = "bar") %>%
  add_trace(x = ~event_month, y = ~commits, name = "Commits", type = "bar")

# Add shapes, annotations, and relabel axes
fig <- layout(fig, title = 'Fortran FPM Pushes and Commits Over Time',
              shapes = list(
                list(type = "rect",
                     fillcolor = "blue", line = list(color = "blue"), opacity = 0.3,
                     x0 = as.Date("2023-04-01"), x1 = as.Date("2023-06-30"), xref = "x",
                     y0 = 0, y1 = 0.95, yref = "paper")
              ),
              annotations = list(
                list(
                  x = as.Date("2023-05-01"),
                  y = 0.98,
                  text = "STF contract",
                  showarrow = FALSE,
                  font = list(size = 14),
                  xref = "x",
                  yref = "paper"
                )
              ),
              xaxis = list(title = "Event Month"),  
              yaxis = list(title = "Commits & Pushes")   
)


fig





