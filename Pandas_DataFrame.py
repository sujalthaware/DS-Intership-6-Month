import pandas as pd

data = {
    "City": ["Nagpur", "Mumbai", "Delhi", "Pune"],
    "Temperature": [32, 30, 35, 28],
    "Humidity": [55, 70, 40, 60]
}

df = pd.DataFrame(data)

print(df)