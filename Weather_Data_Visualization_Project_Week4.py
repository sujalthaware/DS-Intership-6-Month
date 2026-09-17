# Week 4 - Live Weather Data Visualization
# Client Project: Live Weather Dashboard
# Author: Sujal


##install required libraries in power shell
# pip install requests pandas matplotlib seaborn
## & "C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" -m pip install requests pandas matplotlib seaborn

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. API Configuration

API_KEY = "95cd9836cc83cfef9126d50016a7d812"

cities = input("Enter city name: ").split(",")

weather_data = []

# 2. Fetch Live Weather Data

print("========================================")
print("       LIVE WEATHER DATA PROJECT")
print("========================================")

for city in cities:

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        weather_data.append({
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Feels_Like": data["main"]["feels_like"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Wind_Speed": data["wind"]["speed"],
            "Weather": data["weather"][0]["description"],
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"{city}: Data fetched successfully")

    else:
        print(f"{city}: Unable to fetch data")

# 3. Create Pandas DataFrame


df = pd.DataFrame(weather_data)

if df.empty:
    print("\nNo weather data received.")
    print("Check your API key and internet connection.")
    exit()

print("\nLive Weather Dataset:")
print(df)

# 4. Data Cleaning

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna()
df = df.drop_duplicates()

print("\nCleaned Dataset:")
print(df)

# Save live data
df.to_csv("live_weather_data.csv", index=False)

# 5. Basic Aggregation


print("\n========================================")
print("             DATA SUMMARY")
print("========================================")

print("Total Cities:", len(df))
print("Average Temperature:", round(df["Temperature"].mean(), 2), "°C")
print("Average Humidity:", round(df["Humidity"].mean(), 2), "%")
print("Average Pressure:", round(df["Pressure"].mean(), 2), "hPa")
print("Average Wind Speed:", round(df["Wind_Speed"].mean(), 2), "m/s")


# 6. Visualization Settings


sns.set_theme(style="whitegrid")

# 7. Temperature Bar Chart


plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="City",
    y="Temperature"
)

plt.title("Live Temperature by City")
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("live_temperature_by_city.png")
plt.show()

# 8. Humidity Bar Chart


plt.figure(figsize=(9, 5))

sns.barplot(
    data=df,
    x="City",
    y="Humidity"
)

plt.title("Live Humidity by City")
plt.xlabel("City")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("live_humidity_by_city.png")
plt.show()

# 9. Temperature vs Humidity Scatter Plot


plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Temperature",
    y="Humidity",
    hue="City",
    s=150
)

plt.title("Live Temperature vs Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig("live_temperature_vs_humidity.png")
plt.show()


# 10. Weather Feature Heatmap


numeric_columns = [
    "Temperature",
    "Feels_Like",
    "Humidity",
    "Pressure",
    "Wind_Speed"
]

correlation_matrix = df[numeric_columns].corr()

plt.figure(figsize=(9, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Live Weather Feature Correlation")
plt.tight_layout()
plt.savefig("live_weather_correlation_heatmap.png")
plt.show()

# 11. Final Output


print("\nGenerated Files:")
print("1. live_weather_data.csv")
print("2. live_temperature_by_city.png")
print("3. live_humidity_by_city.png")
print("4. live_temperature_vs_humidity.png")
print("5. live_weather_correlation_heatmap.png")

print("\nLive weather visualization completed successfully!")