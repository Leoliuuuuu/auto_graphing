import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('YS-DI-013.csv')

# Convert the 'DateTime' column to datetime objects
data['DateTime'] = pd.to_datetime(data['DateTime'])
data['RelativeTime_Hours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600

plt.figure(figsize=(10, 6))
plt.xlabel('Relative Time (hours)')
for column in data:
    if column != 'RelativeTime_Hours':
        plt.plot(data['RelativeTime_Hours'], data[column], label=column)
        plt.ylabel(column)
plt.title('Peak Area vs Relative Time (hours)')
plt.legend()
plt.grid()
plt.show()