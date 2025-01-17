import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, ScalarFormatter

# Load data
data = pd.read_csv('YS-DI-013.csv')

# Convert the 'DateTime' column to datetime objects
data['DateTime'] = pd.to_datetime(data['DateTime'])
data['RelativeTime_Hours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600


# Formatter function for 2 decimal places
def format_two_decimals(x, pos):
    return f'{x:.2f}'

def format_y_axis(x, pos):
    return f'{x:.2f}'


# Filter columns
columns_to_plot = [
    col for col in data.select_dtypes(include=['float64', 'int64']).columns
    if "MS" not in col and "IS" not in col and col != "RelativeTime_Hours"
]
IS_column = [col for col in data.columns if "IS" in col]  # Identify the "IS" trend
if len(IS_column) != 1:
    raise ValueError("There must be exactly one column containing 'IS'.")
IS_column = IS_column[0]


# Define color mapping for trends
color_mapping = {
    "SM1": "blue",  # All trends containing "SM1" will be blue
    "SM2": "mediumseagreen",  # All trends containing "SM2" will be green
    "PDT": "red",  # All trends containing "PDT" will be red
    "IS": "gray"
}

# Function to get color based on trend name
def get_color(column_name):
    for key, color in color_mapping.items():
        if key in column_name:
            return color
    return "black"  # Default color if no match is found


fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary y-axis (non-MS columns)

for column in columns_to_plot:
    ax1.plot(
        data['RelativeTime_Hours'],
        (data[column] / data[IS_column]),  # Divide the trend by "IS"
        label=f"Recalibrated {column}",
        marker='o',
        linestyle='-',
        color=get_color(column),
        alpha=1.0
    )

ax1.set_xlabel('Relative Time (hours)')
ax1.set_ylabel('Recalibrated Peak Area')  # Primary y-axis label
ax1.yaxis.set_major_formatter(FuncFormatter(format_y_axis))
ax1.xaxis.set_major_formatter(FuncFormatter(format_two_decimals))
ax1.tick_params(axis='y')

# Combine legends for both axes
lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1, labels1, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False)

plt.title('Recalibration Peak Area vs Relative Time (hours)')
plt.show()
