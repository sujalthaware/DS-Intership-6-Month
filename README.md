
# Data Science Internship - Month 1

## Weeks 1 to 3: Python, Data Structures, NumPy & Pandas

**Author:** Sujal

---

## 📌 Overview

This repository contains the work completed during the first three weeks of my Data Science Internship.

During these weeks, I learned the fundamentals of Python programming, data structures and functions, and data manipulation using NumPy and Pandas.

The practical projects helped me understand how Python can be used to process, clean, analyze, and prepare data for further Data Science tasks.

---

# 📅 Week 1 - Introduction to Python Programming

## Objective

The objective of Week 1 was to learn the basic concepts of Python programming and understand how Python can be used for simple data processing tasks.

## Topics Covered

- Variables
- Data Types
- Operators
- Input and Output
- Conditional Statements
- Loops
- Basic Functions
- Temperature Conversion
- Calculator Program
- Basic Data Processing

## Hands-On Projects

### 1. Temperature Converter

Created a Python program to convert temperature between Celsius and Fahrenheit.

### 2. Calculator

Created a basic calculator that performs:

- Addition
- Subtraction
- Multiplication
- Division

### 3. Temperature Data Processing

Created a Python script to process temperature data and calculate the average temperature.

## Skills Learned

- Python syntax
- Variables and data types
- Mathematical operations
- `if-else` conditions
- `for` and `while` loops
- Basic data processing
- Taking user input
- Displaying results

---

# 📅 Week 2 - Data Structures and Functions

## Objective

The objective of Week 2 was to understand Python data structures and functions and use them for data transformation and cleaning.

## Topics Covered

- Lists
- Tuples
- Dictionaries
- Sets
- Functions
- Lambda Functions
- List Comprehension
- Recursion
- Data Transformation
- Data Cleaning

## Client Project: Data Cleaning

A temperature dataset was used to demonstrate basic data cleaning techniques.

### Operations Performed

- Created a dataset using Python lists
- Removed duplicate values
- Sorted the cleaned data
- Filtered temperatures within a specific range
- Calculated the average temperature
- Used lambda functions
- Used list comprehension
- Generated squared temperature values

### Example

Original data:

```text
30, 32, 31, 30, 35, 32, 28, 31, 40, 25, 35, 30, 28
````

After removing duplicates:

```text
25, 28, 30, 31, 32, 35, 40
```

Filtered data:

```text
30, 31, 32, 35
```

Average:

```text
32.0°C
```

## Skills Learned

* Working with Python data structures
* Writing reusable functions
* Removing duplicate data
* Filtering data
* Lambda functions
* List comprehension
* Basic data-cleaning techniques

---

# 📅 Week 3 - NumPy and Pandas for Data Manipulation

## Objective

The objective of Week 3 was to learn how NumPy and Pandas are used for numerical calculations, data manipulation, cleaning, and aggregation.

## Topics Covered

### NumPy

* NumPy arrays
* Array creation
* Mathematical operations
* Mean
* Minimum
* Maximum
* Broadcasting
* Converting Pandas data into NumPy arrays

### Pandas

* Series
* DataFrames
* Indexing
* Data selection
* Missing values
* `dropna()`
* Grouping
* Aggregation
* Average calculations

## Client Project: Clean and Aggregate Dataset

The project focused on cleaning a dataset and generating useful summary information from the cleaned data.

### Operations Performed

* Created and loaded a dataset
* Converted data into a Pandas DataFrame
* Inspected the dataset
* Checked for missing values
* Removed records containing missing values
* Calculated average temperature
* Calculated average humidity
* Grouped data by city
* Calculated city-wise average temperature
* Converted Pandas data into a NumPy array
* Performed NumPy calculations
* Applied broadcasting operations

## Example Results

```text
Original Rows: 10
Cleaned Rows: 8
Removed Rows: 2

Average Temperature: 31.38°C
Average Humidity: 59.63%

City-wise Average Temperature:
Delhi
Mumbai
Nagpur
Pune
```

## Skills Learned

* Numerical data processing with NumPy
* Data manipulation with Pandas
* Working with Series and DataFrames
* Handling missing values
* Data aggregation
* Grouping datasets
* Statistical calculations
* Preparing clean data for analysis

---

# 🛠️ Technologies Used

* Python
* NumPy
* Pandas
* VS Code
* PowerShell

---

# 📂 Project Structure

```text
DS-Intership-6-Month/
│
├── week_1_month_1/
│   ├── temperature_converter.py
│   ├── calculator.py
│   ├── temperature_processing.py
│   └── README.md
│
├── week_2_month_1/
│   ├── Week2_Data_Cleaning.py
│   ├── README.md
│   └── concepts_summary.txt
│
└── week_3_month_1/
    ├── NumPy.py
    ├── Pandas_Series.py
    ├── Week3_NumPy_Pandas_Project.py
    ├── README.md
    └── concepts_summary.txt
```

---

# 📊 Overall Learning Outcome

During Weeks 1 to 3, I developed a foundation in Python programming and data manipulation.

I learned how to:

1. Write basic Python programs.
2. Work with variables and different data types.
3. Use conditions and loops.
4. Work with lists, tuples, dictionaries, and sets.
5. Create and use functions.
6. Clean and transform basic datasets.
7. Perform numerical calculations using NumPy.
8. Create and manipulate Pandas Series and DataFrames.
9. Handle missing and duplicate data.
10. Group and aggregate datasets.
11. Calculate useful statistical values such as averages, minimums, and maximums.

These concepts provide the foundation for the upcoming Data Science topics such as **Data Visualization, Exploratory Data Analysis (EDA), Machine Learning, and Model Building**.

# Data Science Internship - Month 1

## Week 4: Data Visualization with Matplotlib and Seaborn

**Client Project:** Real-Time Weather Data Visualization Dashboard

**Author:** Sujal

---

## 📌 Project Overview

The objective of this project is to collect, process, analyze, and visualize
real-time weather data using Python.

Instead of using a static dataset, this project collects current weather
information from an external weather API for multiple cities.

The collected data is processed using Pandas and visualized using Matplotlib
and Seaborn.

The project demonstrates a basic real-world Data Science workflow:

    API Data
       ↓
    Data Collection
       ↓
    Pandas DataFrame
       ↓
    Data Cleaning
       ↓
    Data Analysis
       ↓
    Data Visualization
       ↓
    CSV Export

---

# 🎯 Objectives

The main objectives of this project are:

- Collect real-time weather data using an API.
- Work with external real-world data.
- Create a Pandas DataFrame from API data.
- Check and handle missing values.
- Remove duplicate records.
- Calculate weather statistics.
- Compare weather conditions between cities.
- Create visualizations using Matplotlib.
- Create advanced visualizations using Seaborn.
- Analyze relationships between weather features.
- Save processed data into a CSV file.

---

# 📚 Theory

During Week 4, the following concepts were studied:

## Matplotlib

Matplotlib is a Python library used for creating data visualizations.

Important concepts learned:

- Figure
- Axes
- Line plots
- Bar charts
- Scatter plots
- Titles
- X-axis and Y-axis labels
- Legends
- Figure size
- Saving plots

## Seaborn

Seaborn is a Python visualization library built on top of Matplotlib.

It is useful for statistical and advanced visualizations.

Concepts learned:

- Bar plots
- Scatter plots
- Histograms
- Boxplots
- Heatmaps
- Correlation analysis
- Pairplots

---

# 🌐 Real-Time Data Source

This project uses a weather API to collect current weather information.

The API provides information such as:

- City
- Temperature
- Feels-like temperature
- Humidity
- Atmospheric pressure
- Wind speed
- Weather condition
- Data collection time

The data is retrieved dynamically whenever the Python program is executed.

---

# 🛠️ Technologies Used

- Python
- Requests
- Pandas
- Matplotlib
- Seaborn
- OpenWeather API
- VS Code
- PowerShell

---

# 📂 Project Structure

```text
week_4_month_1/
│
├── Week4_Live_Weather_Visualization.py
│
├── live_weather_data.csv
│
├── live_temperature_by_city.png
├── live_humidity_by_city.png
├── live_temperature_vs_humidity.png
├── live_weather_correlation_heatmap.png
│
└── README.md
