import pandas as pd
import matplotlib.pyplot as plt

def load_csv(file_path):
    """Load CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def convert_to_relative_time(df):
    """Convert first column to relative time (hours)."""
    time_column = df.columns[0]  # Assume first column is time

    try:
        df[time_column] = pd.to_numeric(df[time_column])  # Try converting to numbers
    except ValueError:
        df[time_column] = pd.to_datetime(df[time_column])  # Try parsing datetime
        df[time_column] = (df[time_column] - df[time_column].iloc[0]).dt.total_seconds()

    df[time_column] = df[time_column] / 3600.0  # Convert seconds to hours
    return df


def select_trends(df):
    """Let user select which trends to plot."""
    print("Available columns:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    selected_indices = input("Enter column numbers to plot (comma separated): ")
    selected_indices = [int(i) for i in selected_indices.split(",")]

    return [df.columns[i] for i in selected_indices]

def plot_trends(df, selected_columns):
    """Plot selected trends over time."""
    time_column = df.columns[0]  # Assume first column is time
    plt.figure(figsize=(10, 6))

    for col in selected_columns:
        plt.plot(df[time_column], df[col], label=col)

    plt.xlabel("Relative Time (hours)")
    plt.ylabel("Value")
    plt.legend()
    plt.title("Trend Plot")
    plt.show()


# === MAIN SCRIPT ===
file_path = input("Enter CSV file path: ")
df = load_csv(file_path)

if df is not None:
    df = convert_to_relative_time(df)
    selected_columns = select_trends(df)
    plot_trends(df, selected_columns)