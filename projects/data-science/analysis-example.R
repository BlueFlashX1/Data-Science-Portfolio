# Data Science Analysis Example
# Author: Matthew Thompson
# Date: 2025-10-06

# Load required libraries
library(tidyverse)
library(ggplot2)
library(plotly)

# Load and explore data
data(mtcars)
glimpse(mtcars)

# Data analysis
summary_stats <- mtcars %>%
  group_by(cyl) %>%
  summarise(
    count = n(),
    avg_mpg = mean(mpg),
    avg_hp = mean(hp),
    .groups = 'drop'
  )

# Visualization
p1 <- ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  geom_smooth(method = 'lm', se = FALSE) +
  labs(
    title = "Miles per Gallon vs Weight",
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    color = "Cylinders"
  ) +
  theme_minimal()

# Interactive version
interactive_plot <- ggplotly(p1)

# Save results
ggsave("../../assets/images/screenshots/mpg_analysis.png", p1, width = 10, height = 6)

print("Analysis complete!")
