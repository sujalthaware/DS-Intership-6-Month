import pandas as pd

temperatures = pd.Series([30, 32, 31, 35, 28, 33])

print("Temperature Series:")
print(temperatures)

print("\nAverage:", temperatures.mean())
print("Maximum:", temperatures.max())
print("Minimum:", temperatures.min())