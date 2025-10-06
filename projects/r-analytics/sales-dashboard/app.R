# Sales Dashboard - Interactive Shiny Application
# Author: Matthew Thompson
# Date: 2025-10-06

library(shiny)
library(shinydashboard)
library(plotly)
library(DT)
library(dplyr)

# Sample data
sales_data <- data.frame(
  month = month.name,
  sales = c(150, 180, 220, 195, 240, 280, 310, 295, 320, 340, 365, 400),
  profit = c(45, 54, 66, 58, 72, 84, 93, 88, 96, 102, 109, 120)
)

# UI
ui <- dashboardPage(
  dashboardHeader(title = "Sales Analytics Dashboard"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard"),
      menuItem("Data Table", tabName = "data")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem("dashboard",
        fluidRow(
          box(plotlyOutput("sales_plot"), width = 6),
          box(plotlyOutput("profit_plot"), width = 6)
        )
      ),
      tabItem("data",
        DT::dataTableOutput("data_table")
      )
    )
  )
)

# Server
server <- function(input, output) {
  output$sales_plot <- renderPlotly({
    p <- plot_ly(sales_data, x = ~month, y = ~sales, type = 'scatter', mode = 'lines+markers') %>%
      layout(title = "Monthly Sales Trend")
    p
  })
  
  output$profit_plot <- renderPlotly({
    p <- plot_ly(sales_data, x = ~month, y = ~profit, type = 'bar') %>%
      layout(title = "Monthly Profit")
    p
  })
  
  output$data_table <- DT::renderDataTable({
    DT::datatable(sales_data, options = list(pageLength = 12))
  })
}

shinyApp(ui = ui, server = server)
