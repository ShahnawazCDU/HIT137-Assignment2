import pandas as pd
import numpy as np
import glob
import os

# -------------------- CONFIG --------------------
folder_path = "temperatures"  # Folder containing CSV files
# ------------------------------------------------

# Check if folder exists
if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' does not exist!")
    exit()

csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
if not csv_files:
    print(f"Error: No CSV files found in '{folder_path}'")
    exit()

# Dictionary to hold temperatures for each station
station_data = {}

# Dictionary for seasonal temperatures
season_temps = {"Summer": [], "Autumn": [], "Winter": [], "Spring": []}

# Helper function to determine Australian season from month
def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    elif month in [9, 10, 11]:
        return "Spring"

# -------------------- PROCESS CSV FILES --------------------
for file in csv_files:
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Error reading {file}: {e}")
        continue

    # Check if required columns exist
    required_columns = {"Date", "Station", "Temperature"}
    if not required_columns.issubset(df.columns):
        print(f"Skipping {file}: missing required columns")
        continue

    # Ensure Temperature is numeric
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')

    # Process each row
    for idx, row in df.iterrows():
        temp = row['Temperature']
        station = row['Station']
        try:
            month = pd.to_datetime(row['Date']).month
        except:
            continue  # skip invalid dates

        if pd.isna(temp):
            continue  # skip missing temperatures

        # Add temperature to seasonal list
        season = get_season(month)
        season_temps[season].append(temp)

        # Add temperature to station data
        if station not in station_data:
            station_data[station] = []
        station_data[station].append(temp)

# -------------------- SEASONAL AVERAGE --------------------
with open("average_temp.txt", "w") as f:
    f.write("Seasonal Average Temperatures:\n")
    for season, temps in season_temps.items():
        if temps:
            avg_temp = sum(temps) / len(temps)
            f.write(f"{season}: {avg_temp:.1f}°C\n")
        else:
            f.write(f"{season}: No data\n")

# -------------------- LARGEST TEMPERATURE RANGE --------------------
station_ranges = {}
max_range = -1

for station, temps in station_data.items():
    if not temps:
        continue
    max_temp = max(temps)
    min_temp = min(temps)
    temp_range = max_temp - min_temp
    station_ranges[station] = (temp_range, max_temp, min_temp)
    if temp_range > max_range:
        max_range = temp_range

with open("largest_temp_range_station.txt", "w") as f:
    f.write("Station(s) with Largest Temperature Range:\n")
    for station, (temp_range, max_temp, min_temp) in station_ranges.items():
        if temp_range == max_range:
            f.write(f"Station {station}: Range {temp_range:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")

# -------------------- TEMPERATURE STABILITY --------------------
station_std = {}
for station, temps in station_data.items():
    if not temps:
        continue
    std = np.std(temps)
    station_std[station] = std

if station_std:
    min_std = min(station_std.values())
    max_std = max(station_std.values())
else:
    min_std = max_std = None

with open("temperature_stability_stations.txt", "w") as f:
    f.write("Temperature Stability by Station:\n")
    if min_std is not None:
        for station, std in station_std.items():
            if std == min_std:
                f.write(f"Most Stable: Station {station}: StdDev {std:.1f}°C\n")
        for station, std in station_std.items():
            if std == max_std:
                f.write(f"Most Variable: Station {station}: StdDev {std:.1f}°C\n")
    else:
        f.write("No valid temperature data available.\n")

print("Analysis complete! Check the output text files:")
print("- average_temp.txt")
print("- largest_temp_range_station.txt")
print("- temperature_stability_stations.txt")
