# Week 2 - Data Cleaning Project

temperatures = [30, 32, 31, 30, 35, 32, 28, 31, 40, 25]

print("Original Data:")
print(temperatures)

# Remove duplicates
cleaned_data = list(set(temperatures))

# Sort the data
cleaned_data.sort()

print("\nAfter Removing Duplicates:")
print(cleaned_data)

# Filter temperatures between 30 and 35
filtered_data = [temp for temp in cleaned_data if 30 <= temp <= 35]

print("\nFiltered Temperatures (30°C to 35°C):")
print(filtered_data)

# Calculate average
average = sum(filtered_data) / len(filtered_data)

print("\nAverage Temperature:")
print(round(average, 2), "°C")