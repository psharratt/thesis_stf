
# Public Money, Public Code: Evaluating the Impact of Public Investment in Open-Source Digital Infrastructure

## Thesis for the Hertie School's Master of Data Science for Public Policy

This repository contains the data and analysis scripts for my master's thesis conducted at the Hertie School, Berlin, under the supervision of Prof. Simon Munzert and in partnership with the Sovereign Tech Fund. The study investigates the correlation between public investment and the health of open-source software projects hosted on GitHub.

### Abstract

Amidst the growing reliance on open-source software for digital infrastructure, understanding the dynamics of public investment and the communal well-being of such software is pivotal. This research examines the correlation between financial support from the Sovereign Tech Fund and measurements of OSS ecosystem health on GitHub, using a Difference-in-Differences method estimated with two way fixed effects to scrutinize the impact of investment.

### Repository Structure

- `/pap`: Contains the Pre-Analysis Proposal of the thesis and associated R Markdown files for generating the document.
  - `/figures`: Graphical representations and visualizations used in the thesis.
- `/scripts`: 
  - `/SQL`: SQL scripts for data collection from the CHAOSS Augur software suite & database.
  - `/Python`: Python scripts for data collection, processing, and analysis.
  - `/functions`: Python functions with nested SQL string queries for data collection
  - `/R`: R scripts for statistical analysis and generating figures.
- `/output`: 
  - `/summaries`: Summary files of the analyzed metrics.
  - `/tables`: Generated tables used in the thesis.
  - `/final plots`: Plots and graphs used in the final document.
- `/data`: 
  - `/DID`: Directory for Difference-in-Differences related datasets.
  - `/processed`: Processed data files ready for analysis.
  - `/raw`: Raw data files as obtained from the sources.

### Data

The data analyzed in this thesis is collected from the Augur software suite of the CHAOSS project, which tracks development activities across various open-source software projects alongside investment data from the Sovereign Tech Fund.

### Scripts

- `/SQL`, `/Python`, `/R`: Contains the scripts used for data extraction, cleaning, transformation, and analysis.

### Output

- `/metrics`: Summaries of the DiD analysis.
- `/tables`, `/plots`: Data representations and visual outputs for thesis.

### Archive

This project is completed and serves as an archive for the thesis work. However, queries and discussions are welcome. Please reach out to [my Hertie email](mailto:22924@students.hertie-school.org).

### Acknowledgements

Special thanks to Prof. Simon Munzert for his guidance, Dawn Foster & Sean Goggins of the CHAOSS Project for their collaboration and insights, and my colleagues at the Sovereign Tech Fund for their support.

### License

This work is licensed under [MIT License](LICENSE.MIT).

