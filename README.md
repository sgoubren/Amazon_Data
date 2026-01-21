# Amazon Consumer Purchase Trends Analysis

This project analyzes consumer purchasing patterns and spending trends using Amazon purchase data. It uses an end-to-end data pipeline workflow, from data retrieval and cleaning to visualization and reporting.

## Overview

The goal of this project is to explore and understand consumer behavior through Amazon purchase data. Insights include spending trends and patterns over time. The analysis leverages AWS cloud tools for ETL, Python/Pandas for data wrangling, and Streamlit for interactive dashboards to communicate insights.

## Features

- **Automated ETL Workflow:** Retrieves, cleans, and consolidates data using AWS services (S3, Glue, Athena, SageMaker).
- **Data Analysis & Visualization:** Explores trends in purchase frequency and spending habits.
- **Interactive Dashboard:** Presents results via an interactive dashboard built with Streamlit.

## Technologies & Tools

- **Languages & Libraries:** Python, Pandas, NumPy, Matplotlib, Seaborn, Jupyter
- **Cloud & Big Data:** AWS S3, Glue, Athena, SageMaker
- **Visualization:** Streamlit, Matplotlib, Seaborn
- **Data Processing:** ETL, Data Cleaning, Aggregation

## Project Workflow

1. **Data Retrieval:** Downloaded raw Amazon purchase history data.
2. **Data Cleaning & Transformation:** Structured unorganized data into analyzable format; handled missing values and duplicates.
3. **Data Aggregation & ETL:** Loaded cleaned data into AWS S3 and used Glue and Athena for query-based transformations.
4. **Data Analysis:** Explored trends in spending, purchase frequency.
5. **Visualization & Dashboard:** Built interactive dashboard for clear insight discovery and reporting.

## Insights & Findings

- Spending peaks and plunges during specific months, highlighting seasonality in consumer behavior.
- Certain products dominate purchase frequency and total spend.
- Frequent repeat purchases show Amazon is a staple for house products.

