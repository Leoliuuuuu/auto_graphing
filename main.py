import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load data
data = pd.read_csv('YS-DI-013.csv')

# Convert the 'DateTime' column to datetime objects
data['DateTime'] = pd.to_datetime(data['DateTime'])
data['RelativeTime_Hours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600


# Formatter function for 2 decimal places
def format_two_decimals(x, pos):
    return f'{x:.2f}'


plt.figure(figsize=(10, 6))
plt.xlabel('Relative Time (hours)')
for column in data.select_dtypes(include=['float64', 'int64']).columns:
    if column != 'RelativeTime_Hours':
        plt.plot(data['RelativeTime_Hours'], data[column], label=column)
plt.ylabel("Peak Area")
# Format axes to show 2 decimal places
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_two_decimals))
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_two_decimals))

plt.title('Peak Area vs Relative Time (hours)')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)  # Adjust ncol for the number of columns
# plt.grid()
plt.show()
