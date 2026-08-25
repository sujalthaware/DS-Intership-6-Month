##Basic Data Processing
"""
##temperatures = [30, 32, 31, 29, 33]

# Calculate total
#total = sum(temperatures)

# Calculate average
average = total / len(temperatures)

# Find highest and lowest temperature
highest = max(temperatures)
lowest = min(temperatures)

# Display results
print("Temperatures:", temperatures)
print("Total:", total)
print("Average:", average)
print("Highest Temperature:", highest)
print("Lowest Temperature:", lowest)
"""



""" 
open power shell and run the following command to install the requests library:
1. Install requests

In the same PowerShell terminal, run:

& "C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" -m pip install requests

Wait until you see something like:

Successfully installed requests ...

2. Run your program again
& "C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" "d:\sujal\programs\Input\Basic_Data_Processing.py"

"""
import requests

city = "Nagpur"
api_key = "9bc031801a0de849e0b3ede218164e61"

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)
print("Response:", response.json())

if response.status_code == 200:
    data = response.json()

    temperature = data["main"]["temp"]
    weather = data["weather"][0]["description"]

    print("\nCity:", city)
    print("Current Temperature:", temperature, "°C")
    print("Weather:", weather)
else:
    print("\nAPI Error:", response.json().get("message"))