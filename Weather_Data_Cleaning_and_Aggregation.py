# Week 3 - NumPy and Pandas for Data Manipulation
# Client Project: Weather Data Cleaning and Aggregation
# Author: Sujal

import numpy as np
import pandas as pd


# Create weather dataset

data = {
    "City": [
        "Nagpur",
        "Mumbai",
        "Delhi",
        "Pune",
        "Nagpur",
        "Mumbai",
        "Delhi",
        "Pune",
        "Nagpur",
        "Mumbai"
    ],

    "Temperature": [
        32,
        30,
        np.nan,
        28,
        34,
        31,
        36,
        np.nan,
        33,
        29
    ],

    "Humidity": [
        55,
        70,
        45,
        60,
        np.nan,
        75,
        40,
        65,
        50,
        72
    ]
}

df = pd.DataFrame(data)

print("\nOriginal Dataset:")
print(df)

# Check missing values

print("\nMissing Values:")
print(df.isnull().sum())



# Remove rows containing missing values

cleaned_df = df.dropna()

print("\nCleaned Dataset:")
print(cleaned_df)


# Calculate overall averages

average_temperature = cleaned_df["Temperature"].mean()
average_humidity = cleaned_df["Humidity"].mean()

print("\nOverall Average Temperature:")
print(round(average_temperature, 2), "°C")

print("\nOverall Average Humidity:")
print(round(average_humidity, 2), "%")


# Group data by city

city_average = cleaned_df.groupby("City")[
    "Temperature"
].mean()

print("\nAverage Temperature by City:")
print(city_average)


# NumPy operations

temperature_array = cleaned_df["Temperature"].to_numpy()

print("\nNumPy Temperature Array:")
print(temperature_array)

print("\nNumPy Average:")
print(np.mean(temperature_array))

print("\nNumPy Maximum:")
print(np.max(temperature_array))

print("\nNumPy Minimum:")
print(np.min(temperature_array))


# Broadcasting

adjusted_temperature = temperature_array + 1

print("\nTemperature After Adding 1°C:")
print(adjusted_temperature)


# Final Report

print("              FINAL REPORT")


print("Original Rows:", len(df))
print("Cleaned Rows:", len(cleaned_df))
print("Removed Rows:", len(df) - len(cleaned_df))

print(
    "Average Temperature:",
    round(average_temperature, 2),
    "°C"
)

print(
    "Average Humidity:",
    round(average_humidity, 2),
    "%"
)

print("\nData cleaning and aggregation completed successfully!")