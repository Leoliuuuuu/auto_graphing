import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from itertools import cycle

# Load data
data = pd.read_csv('YS-DI-027_1.5_Ar-Br.csv')

# Convert the 'DateTime' column to datetime objects
data['DateTime'] = pd.to_datetime(data['DateTime'])
data['RelativeTime_Hours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600


# Formatter function for 2 decimal places
def format_two_decimals(x, pos):
    return f'{x:.2f}'


def format_y_axis(x, pos):
    return f'{x:.2f}'


# Filter out unwanted trends (like "RelativeTime_Hours")
columns_to_plot = [col for col in data.select_dtypes(include=['float64', 'int64']).columns if col != "RelativeTime_Hours"]
columns_with_ms = [col for col in columns_to_plot if "MS" in col]
columns_without_ms = [col for col in columns_to_plot if col not in columns_with_ms]


# Define color mapping for trends
color_mapping = {
    "SM1": "blue",  # All trends containing "SM1" will be blue
    "SM2": "mediumseagreen",  # All trends containing "SM2" will be green
    "PDT": "red",  # All trends containing "PDT" will be red
    "IS": "gray"
}


# Function to get color based on trend name

allowed_colors = [
    "orange", "purple", "pink", "yellow", "brown",
    "cyan", "magenta", "lime", "teal", "navy", "maroon"
]

color_iterator = cycle(allowed_colors)
def get_color(column_name):
    for key, color in color_mapping.items():
        if key in column_name:
            return color
    return next(color_iterator)

# Ask for the timestamp or default to max normalization
timestamp = input("Enter the timestamp, or press Enter to normalize by max: ")
if timestamp:
    try:
        normalize_row = data.loc[data['DateTime'] == timestamp]
        if normalize_row.empty:
            raise ValueError("Timestamp not found in the data.")
        normalize_row = normalize_row.iloc[0]
        print(normalize_row)
        print(f"Normalizing to the row with DateTime: {timestamp}")
    except Exception as e:
        print(f"Error: {e}")
        print("Defaulting to normalization by maximum value.")
        normalize_row = None
else:
    normalize_row = None

# Normalize data
normalized_data = data.copy()
for column in columns_to_plot:
    if normalize_row is not None:
        normalized_data[column] = data[column] / normalize_row[column]
    else:
        print(column)
        factor = float(input("whats the factor you want?"))
        normalized_data[column] = data[column] / data[column].max() * factor


fig, ax1 = plt.subplots(figsize=(10, 6))

# Primary y-axis (non-MS columns)
for column in columns_without_ms:
    ax1.plot(
        normalized_data['RelativeTime_Hours'],
        normalized_data[column],
        label=column,
        marker='o',
        linestyle='-',
        color=get_color(column),
        alpha=1.0
    )
ax1.set_xlabel('Relative Time (hours)')
ax1.set_ylabel('Normalized Value')  # Primary y-axis label
ax1.yaxis.set_major_formatter(FuncFormatter(format_y_axis))
ax1.xaxis.set_major_formatter(FuncFormatter(format_two_decimals))
ax1.tick_params(axis='y')

# Combine legends for both axes
lines1, labels1 = ax1.get_legend_handles_labels()
ax1.legend(lines1, labels1, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False)


# Secondary y-axis (MS columns)
if columns_with_ms:
    ax2 = ax1.twinx()
    for column in columns_with_ms:
        ax2.plot(
            normalized_data['RelativeTime_Hours'],
            normalized_data[column],
            label=column,
            marker='o',  # Empty circle marker
            linestyle='--',
            markerfacecolor='none',
            color=get_color(column),
            alpha=1.0
        )
    ax2.set_ylabel('Normalized MS Data')  # Secondary y-axis label
    ax2.yaxis.set_major_formatter(FuncFormatter(format_y_axis))
    ax1.xaxis.set_major_formatter(FuncFormatter(format_two_decimals))
    ax2.tick_params(axis='y')

    # Align the two y-axes and enforce non-negative limits with padding at both ends
    min_y = min(ax1.get_ylim()[0], ax2.get_ylim()[0]) - 0.05 * max(ax1.get_ylim()[1],
                                                                   ax2.get_ylim()[1])  # Add 5% padding below
    # max_y = max(ax1.get_ylim()[1], ax2.get_ylim()[1]) * 1.05  # Add 5% padding above
    ax1.set_ylim(min_y)
    ax2.set_ylim(min_y)

    # Combine legends for both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False)



plt.title('Normalized Trends vs Relative Time (hours)')
plt.show()