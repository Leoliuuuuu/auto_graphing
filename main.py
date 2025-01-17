import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('your_file.csv')

# Convert the 'DateTime' column to datetime objects
data['DateTime'] = pd.to_datetime(data['DateTime'])
data['RelativeTime_Hours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600