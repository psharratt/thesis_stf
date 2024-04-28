# Load necessary packages
if (!requireNamespace("fixest", quietly = TRUE)) install.packages("fixest")
if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")
if (!requireNamespace("writexl", quietly = TRUE)) install.packages("writexl")
if (!requireNamespace("lmtest", quietly = TRUE)) install.packages("lmtest")
if (!requireNamespace("broom", quietly = TRUE)) install.packages("broom")
if (!requireNamespace("knitr", quietly = TRUE)) install.packages("knitr")
if (!requireNamespace("kableExtra", quietly = TRUE)) install.packages("kableExtra")
if (!requireNamespace("did2s", quietly = TRUE)) install.packages("did2s")

library(fixest)
library(readxl)
library(dplyr)
library(writexl)
library(lmtest)
library(ggplot2)
library(broom)
library(knitr)
library(kableExtra)
library(did2s)



# Load Data from R package
data("df_het", package = "did2s")


# Mean for treatment group-year
agg <- aggregate(df_het$dep_var, by=list(g = df_het$g, year = df_het$year), FUN = mean)

agg$g <- as.character(agg$g)
agg$g <- ifelse(agg$g == "0", "Never Treated", agg$g)

never <- agg[agg$g == "Never Treated", ]
g1 <- agg[agg$g == "2000", ]
g2 <- agg[agg$g == "2010", ]


plot(0, 0, xlim = c(1990,2020), ylim = c(4,7.2), type = "n",
     main = "Data-generating Process", ylab = "Outcome", xlab = "Year")
abline(v = c(1999.5, 2009.5), lty = 2)
lines(never$year, never$x, col = "#8e549f", type = "b", pch = 15)
lines(g1$year, g1$x, col = "#497eb3", type = "b", pch = 17)
lines(g2$year, g2$x, col = "#d2382c", type = "b", pch = 16)
legend(x=1990, y=7.1, col = c("#8e549f", "#497eb3", "#d2382c"), 
       pch = c(15, 17, 16),
       legend = c("Never Treated", "2000", "2010"))



# Static
static <- did2s(df_het, 
                yname = "dep_var", first_stage = ~ 0 | state + year, 
                second_stage = ~i(treat, ref=FALSE), treatment = "treat", 
                cluster_var = "state")

fixest::etable(static)



# Event Study
es <- did2s(df_het,
            yname = "dep_var", first_stage = ~ 0 | state + year, 
            second_stage = ~i(rel_year, ref=c(-1, Inf)), treatment = "treat", 
            cluster_var = "state")



fixest::iplot(es, main = "Event study: Staggered treatment", xlab = "Relative time to treatment", col = "steelblue", ref.line = -0.5)

# Add the (mean) true effects
true_effects = head(tapply((df_het$te + df_het$te_dynamic), df_het$rel_year, mean), -1)
points(-20:20, true_effects, pch = 20, col = "black")

# Legend
legend(x=-20, y=3, col = c("steelblue", "black"), pch = c(20, 20), 
       legend = c("Two-stage estimate", "True effect"))