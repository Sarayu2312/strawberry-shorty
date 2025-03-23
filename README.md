# Strawberry Shorty: Ollama Model Interface for Environmental Data Analysis

## Overview

**Project Name:** Strawberry Shorty - Ollama Model Interface

**Description:** The Strawberry Shorty project is a web application designed to analyze and interpret environmental data using advanced language models. This tool allows users to upload CSV, TXT, and JSON files containing environmental measurements such as wind speed, temperature, CO2 concentration, and more. The application provides comprehensive data analysis, including summary statistics, time-series plots, and correlation heatmaps, all of which are integrated into a detailed prompt for the language model to generate insightful reports.

## Key Features

1. **Data Upload:**
   - Easily upload CSV, TXT, and JSON files.
   
2. **Data Preprocessing:**
   - Automatically converts the `DateTime` column to a proper datetime format.
   
3. **Data Analysis:**
   - **Summary Statistics:** Provides a quick overview of numerical columns.
   - **Time-series Plots:** Visualizes wind speed and temperature trends at different heights over time.
   - **Correlation Heatmap:** Displays correlations between key environmental variables.
   
4. **Language Model Integration:**
   - Uses Ollama to analyze the data and provide insightful reports without generating code.
   
5. **Interactive UI:**
   - User-friendly interface with checkboxes to include specific data and visualizations in the analysis prompt.
   
6. **Conversation History:**
   - Keeps track of user inputs and model responses for reference.

## Benefits

- **Insightful Analysis:** Get detailed insights and potential explanations for observed data trends and anomalies.
- **Visualization:** Visual aids help in understanding complex data relationships.
- **Automation:** Streamlines the data analysis process, saving time and effort.
- **Customizable:** Users can include specific data and visualizations in the analysis prompt.

## Use Cases

- **Environmental Monitoring:** Analyze environmental data from sensors and instruments.
- **Research and Development:** Gain insights for scientific research projects.
- **Decision Making:** Support decision-making processes with data-driven insights.

## Technology Stack

- **Frontend:** Streamlit for building the web application.
- **Data Processing:** Pandas for data manipulation and analysis.
- **Visualization:** Matplotlib and Seaborn for creating plots and heatmaps.
- **Language Model:** Ollama for generating insights and reports.

## Installation

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Ollama client library
- Pandas
- Matplotlib
- Seaborn

### Steps to Install

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Sarayu2312/strawberry-shorty/
   cd strawberry-shorty
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload Data:**
   - Click on the "Upload a file (CSV, TXT, etc.)" button and select your CSV, TXT, or JSON file.

2. **View Summary and Visualizations:**
   - The application will display summary statistics, time-series plots, and correlation heatmaps.

3. **Include Data in Prompt:**
   - Use the checkboxes to include specific data and visualizations in the analysis prompt.

4. **Generate Insights:**
   - Enter your prompt in the "Enter your prompt" text area and click "Generate Conversation" to get insights from Ollama.

5. **Review Conversation History:**
   - The conversation history will display your inputs and the model's responses.

## Example

### Upload CSV File
- **File:** `environmental_data.csv`
- **Contents:**
  ```csv
  DateTime,WindSpeed_1m[m/s],WindSpeed_3m[m/s],Temp_1m[degC],Temp_3m[degC],RH_1m[%],CO2_MNT[ppm],CO2_desert[ppm],AirPress_hPa
  2023-01-01 00:00:00,1.2,1.5,15.0,16.0,60,400,410,1012
  2023-01-01 01:00:00,1.3,1.6,15.2,16.2,61,405,415,1013
  ...
  ```

### Summary Statistics
- The application will display the summary statistics of the numerical columns.

### Time-series Plots
- Visualizations of wind speed and temperature trends at different heights over time.

### Correlation Heatmap
- Correlation matrix of key environmental variables.

### Generate Insights
- Enter your prompt, e.g., "Analyze the trends and correlations in the environmental data."
- Click "Generate Conversation" to get insights from Ollama.

