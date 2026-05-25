# Regenerate the 4 README-thumbnail PNGs from the same data the Rmd uses.
# Source the Rmd's data once (via knitr::purl or by re-reading the CSVs);
# here we re-read the CSVs directly because the data prep is light.
#
# Each plot is restyled for thumbnail readability (larger axis text, visible
# legends, on-chart titles). The original Rmd is unchanged so the final
# course-submission PDF in reports/ stays bit-identical.
#
# Run:
#   source("setup.R")                     # if you haven't already
#   Rscript scripts/export_readme_figures.R

suppressPackageStartupMessages({
  library(tidyverse)
  library(readxl)
  library(ggalluvial)
  library(viridis)
  library(patchwork)
})

dir.create("images", showWarnings = FALSE)

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Cougar prey distribution (pie chart)
# ─────────────────────────────────────────────────────────────────────────────
cougars <- read_xlsx("data/Cougar Killsites.xlsx")

cougar_species <- cougars %>%
  filter(!is.na(PreySpeciesSingle)) %>%
  mutate(
    PreySpeciesGroup = case_when(
      PreySpeciesSingle %in% c("Mule Deer", "Bighorn Sheep", "Feral Horse",
                               "Pronghorn", "Scavenged - Mule Deer",
                               "Unknown Ungulates") ~ "Wild Ungulates",
      PreySpeciesSingle %in% c("Small Mammal", "Porcupine",
                               "Bird", "Beaver", "Badger") ~ "Small Animals",
      PreySpeciesSingle %in% c("Domestic Dog", "Domestic Sheep",
                               "Scavenged - Domestic Cow",
                               "Domestic Cattle") ~ "Domestic Animals",
      PreySpeciesSingle %in% c("Black Bear", "Coyote", "Red Fox",
                               "Bobcat") ~ "Carnivores",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(!is.na(PreySpeciesGroup))

cougar_pie_data <- cougar_species %>%
  count(PreySpeciesGroup) %>%
  mutate(
    pct = n / sum(n) * 100,
    label = sprintf("%s\n%d (%.1f%%)", PreySpeciesGroup, n, pct)
  )

prey_colors <- c(
  "Wild Ungulates"   = "#EEF921",
  "Small Animals"    = "#F58849",
  "Carnivores"       = "#C60BA5",
  "Domestic Animals" = "#DB5C68"
)

p1 <- ggplot(cougar_pie_data, aes(x = "", y = n, fill = PreySpeciesGroup)) +
  geom_bar(stat = "identity", width = 1, color = "white", linewidth = 1) +
  coord_polar("y", start = 0) +
  scale_fill_manual(values = prey_colors, name = "Prey category") +
  labs(
    title = "Figure 1. Cougar prey distribution by category",
    subtitle = sprintf("n = %d kill events, grouped into 4 ecological categories", sum(cougar_pie_data$n)),
    caption = "Wild ungulates dominate; domestic animals are the least common prey."
  ) +
  theme_void(base_size = 13) +
  theme(
    legend.position = "right",
    legend.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold", size = 15, hjust = 0),
    plot.subtitle = element_text(size = 11, hjust = 0, color = "grey30"),
    plot.caption = element_text(size = 10, hjust = 0, color = "grey30", margin = margin(t = 8))
  )

ggsave("images/figure-1-cougar-prey-pie.png", p1, width = 8, height = 5.5, dpi = 150, bg = "white")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Cougar kills over time (grouped bar)
# ─────────────────────────────────────────────────────────────────────────────
p2 <- ggplot(cougar_species, aes(x = factor(Year), fill = PreySpeciesGroup)) +
  geom_bar(position = "dodge", stat = "count") +
  scale_fill_manual(values = prey_colors, name = "Prey category") +
  labs(
    title = "Figure 2. Cougar kills by category, year over year",
    subtitle = "Wild ungulates dominate every year; 2012-2015 has missing records",
    x = "Year",
    y = "Number of cougar kills"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    legend.position = "right",
    legend.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold", size = 15),
    plot.subtitle = element_text(size = 11, color = "grey30"),
    axis.title = element_text(face = "bold")
  )

ggsave("images/figure-2-cougar-kills-by-year.png", p2, width = 9, height = 5.5, dpi = 150, bg = "white")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Top 5 dangerous jobs (line + alluvial)
# ─────────────────────────────────────────────────────────────────────────────
dangerous_job <- read_csv("data/Dangerous Jobs.csv", show_col_types = FALSE)

removed_dupes <- dangerous_job %>%
  group_by(MajorGroup, MinorGroup, BroadOccupation, DetailedOccupation, Cause) %>%
  distinct(Fatalities, .keep_all = TRUE)

replaced_NA <- removed_dupes %>%
  mutate(
    NAICS           = as.character(NAICS),
    NAICS           = ifelse(is.na(NAICS), "UNKNOWN", NAICS),
    MajorGroup      = ifelse(is.na(MajorGroup), "UNKNOWN", MajorGroup),
    MinorGroup      = ifelse(is.na(MinorGroup), "UNKNOWN", MinorGroup),
    BroadOccupation = ifelse(is.na(BroadOccupation), "UNKNOWN", BroadOccupation),
    Fatalities      = ifelse(is.na(Fatalities), 0, Fatalities)
  )

grouped_data <- replaced_NA %>%
  filter(Cause == "Total.Fatalities" & DetailedOccupation != "Total") %>%
  dplyr::select(Year, DetailedOccupation, Fatalities) %>%
  group_by(DetailedOccupation, Year) %>%
  summarize(Fatalities = sum(Fatalities, na.rm = TRUE), .groups = "drop")

required_years <- 2015:2023
valid_occupations <- grouped_data %>%
  group_by(DetailedOccupation) %>%
  filter(all(required_years %in% Year)) %>%
  ungroup()

top_5_names <- valid_occupations %>%
  group_by(DetailedOccupation) %>%
  summarize(Total_Fatalities = sum(Fatalities), .groups = "drop") %>%
  slice_max(Total_Fatalities, n = 5) %>%
  pull(DetailedOccupation)

top_5_occupations <- valid_occupations %>%
  filter(DetailedOccupation %in% top_5_names)

more_cause <- replaced_NA %>%
  filter(DetailedOccupation %in% top_5_names & Cause != "Total.Fatalities")

plot_3a <- ggplot(top_5_occupations,
                  aes(x = Year, y = Fatalities,
                      group = DetailedOccupation,
                      color = DetailedOccupation)) +
  geom_line(linewidth = 1.1) +
  geom_point(size = 2) +
  scale_color_viridis(discrete = TRUE, name = "Occupation") +
  scale_x_continuous(breaks = required_years) +
  labs(
    title = "Panel A: Fatality trends, top 5 most dangerous occupations (2015-2023)",
    x = "Year",
    y = "Fatalities"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "right",
    legend.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold", size = 13),
    axis.title = element_text(face = "bold"),
    axis.text.x = element_text(angle = 0)
  )

cause_totals <- more_cause %>%
  group_by(Cause) %>%
  summarise(Total_Fatalities = sum(Fatalities), .groups = "drop") %>%
  arrange(desc(Total_Fatalities))

more_cause$Cause <- factor(more_cause$Cause, levels = cause_totals$Cause)

plot_3b <- ggplot(more_cause,
                  aes(axis1 = DetailedOccupation, axis2 = Cause, y = Fatalities)) +
  geom_alluvium(aes(fill = DetailedOccupation), alpha = 0.9) +
  geom_stratum(fill = "grey95", color = "grey50") +
  geom_text(stat = "stratum", aes(label = after_stat(stratum)), size = 2.6) +
  scale_x_discrete(limits = c("Occupation", "Cause"), expand = c(0.1, 0.05)) +
  scale_fill_viridis(discrete = TRUE, guide = "none") +
  labs(
    title = "Panel B: Cause-of-fatality flows for the same 5 occupations",
    y = "Fatalities"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    panel.grid = element_blank(),
    axis.text.y = element_text(),
    axis.text.x = element_text(face = "bold", size = 11),
    axis.title.x = element_blank(),
    axis.title.y = element_text(face = "bold"),
    plot.title = element_text(face = "bold", size = 13)
  )

combined_plot <- (plot_3a / plot_3b) +
  plot_annotation(
    title = "Figure 3. Top 5 most dangerous occupations: trends + cause-of-fatality flows",
    theme = theme(plot.title = element_text(face = "bold", size = 16))
  )

ggsave("images/figure-3-dangerous-jobs.png", combined_plot, width = 11, height = 11, dpi = 150, bg = "white")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 4: HPI faceted area plots
# ─────────────────────────────────────────────────────────────────────────────
housing_price <- read_csv("data/Housing Price Index.xlsx - Data.csv", show_col_types = FALSE)

housing_price2 <- housing_price %>%
  mutate(
    Date = as.POSIXct(Date, format = "%m/%d/%Y"),
    Year = year(Date)
  )

mean_acrossdivisons <- housing_price2 %>%
  group_by(Year) %>%
  summarize(across(matches("(SA)|(NSA)"), mean, na.rm = TRUE), .groups = "drop")

major_regionsmean <- mean_acrossdivisons %>%
  mutate(
    Northeast_SA  = rowMeans(dplyr::select(., matches("New\\.England\\(SA\\)|Middle\\.Atlantic\\(SA\\)")), na.rm = TRUE),
    Midwest_SA    = rowMeans(dplyr::select(., matches("East\\.North\\.Central\\(SA\\)|West\\.North\\.Central\\(SA\\)")), na.rm = TRUE),
    South_SA      = rowMeans(dplyr::select(., matches("South\\.Atlantic\\(SA\\)|East\\.South\\.Central\\(SA\\)|West\\.South\\.Central\\(SA\\)")), na.rm = TRUE),
    West_SA       = rowMeans(dplyr::select(., matches("Mountain\\(SA\\)|Pacific\\(SA\\)")), na.rm = TRUE),
    Northeast_NSA = rowMeans(dplyr::select(., matches("New\\.England\\(NSA\\)|Middle\\.Atlantic\\(NSA\\)")), na.rm = TRUE),
    Midwest_NSA   = rowMeans(dplyr::select(., matches("East\\.North\\.Central\\(NSA\\)|West\\.North\\.Central\\(NSA\\)")), na.rm = TRUE),
    South_NSA     = rowMeans(dplyr::select(., matches("South\\.Atlantic\\(NSA\\)|East\\.South\\.Central\\(NSA\\)|West\\.South\\.Central\\(NSA\\)")), na.rm = TRUE),
    West_NSA      = rowMeans(dplyr::select(., matches("Mountain\\(NSA\\)|Pacific\\(NSA\\)")), na.rm = TRUE)
  )

plot_data <- major_regionsmean %>%
  pivot_longer(
    cols = c(Northeast_SA, Midwest_SA, South_SA, West_SA,
             Northeast_NSA, Midwest_NSA, South_NSA, West_NSA),
    names_to = "Type",
    values_to = "HPI"
  ) %>%
  mutate(
    Region = case_when(
      grepl("Northeast", Type) ~ "Northeast",
      grepl("Midwest", Type)   ~ "Midwest",
      grepl("South", Type)     ~ "South",
      grepl("West", Type)      ~ "West"
    ),
    Adjusted = ifelse(grepl("_SA", Type), "Seasonally Adjusted", "Non-Adjusted")
  ) %>%
  dplyr::select(Year, Type, Region, HPI, Adjusted)

p4 <- ggplot() +
  geom_area(
    data = filter(plot_data, Adjusted == "Seasonally Adjusted"),
    aes(x = Year, y = HPI, fill = Adjusted, group = Type), alpha = 0.4
  ) +
  geom_line(
    data = filter(plot_data, Adjusted == "Non-Adjusted"),
    aes(x = Year, y = HPI, color = Adjusted, group = Type), linewidth = 1
  ) +
  scale_color_manual(values = c("Non-Adjusted" = "#1f4e8c"), name = "HPI series") +
  scale_fill_manual(values = c("Seasonally Adjusted" = "#5fa5e8"), name = "HPI series") +
  facet_wrap(~Region, scales = "fixed", nrow = 2) +
  labs(
    title = "Figure 4. Housing Price Index by U.S. region",
    subtitle = "Seasonally adjusted (filled) vs. non-adjusted (line); all regions rise to ~2005, dip 2008-2010, recover post-2010",
    x = "Year",
    y = "Average HPI"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(face = "bold"),
    strip.text = element_text(face = "bold", size = 13),
    plot.title = element_text(face = "bold", size = 15),
    plot.subtitle = element_text(size = 11, color = "grey30"),
    axis.title = element_text(face = "bold")
  )

ggsave("images/figure-4-hpi-by-region.png", p4, width = 10, height = 6.5, dpi = 150, bg = "white")

cat("Done. Generated 4 PNGs in images/:\n")
for (f in list.files("images", "\\.png$", full.names = TRUE)) {
  info <- file.info(f)
  cat(sprintf("  %s  (%.0f KB)\n", f, info$size / 1024))
}
