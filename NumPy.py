import numpy as np

# Create a NumPy array
temperatures = np.array([30, 32, 31, 35, 28, 33])

print("Temperatures:")
print(temperatures)

# Basic operations
print("Average:", np.mean(temperatures))
print("Maximum:", np.max(temperatures))
print("Minimum:", np.min(temperatures))

# Add 2°C to every temperature
new_temperatures = temperatures + 2

print("After adding 2°C:")
print(new_temperatures)