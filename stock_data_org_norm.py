import pandas as pd
import numpy as np
import os

# Load the dataset
file_path = "nifty50.csv"  # Input file
df = pd.read_csv(file_path)

# Extract the dataset name without extension
dataset_name = os.path.splitext(os.path.basename(file_path))[0]

# Create the main directory based on dataset name
main_dir = f"data/{dataset_name}/"
os.makedirs(main_dir, exist_ok=True)

# Convert 'date' column to datetime and split into date and time
df['date'] = pd.to_datetime(df['date'])
df['date_only'] = df['date'].dt.date
df['time_only'] = df['date'].dt.time

# Drop original date column
df.drop(columns=['date'], inplace=True)

# Remove all time columns after 15:25
time_threshold = pd.to_datetime("15:25:00").time()
df = df[df['time_only'] <= time_threshold]

# List of feature columns to process
feature_columns = ['open', 'high', 'low', 'sma5', 'sma10', 'sma15', 'close']

# Process each feature individually
for feature in feature_columns:
    # Create directory for the feature inside the dataset directory
    feature_dir = os.path.join(main_dir, feature)
    os.makedirs(feature_dir, exist_ok=True)

    # Create dataset with only date, time, and the selected feature
    df_feature = df[['date_only', 'time_only', feature]].copy()

    # Pivot to reshape data (date as rows, time as columns)
    df_pivot = df_feature.pivot(index='date_only', columns='time_only', values=feature)

    # Remove rows that have at least one null value
    df_pivot_cleaned = df_pivot.dropna()

    # 1️⃣ Save the Cleaned Raw Data (No Normalization)
    raw_file = os.path.join(feature_dir, f"{feature}_raw.csv")
    df_pivot_cleaned.to_csv(raw_file)

    # 2️⃣ Save the Log Return Data
    log_return_file = os.path.join(feature_dir, f"{feature}_log_return.csv")
    df_log_return = np.log(df_pivot_cleaned.div(df_pivot_cleaned.iloc[:, 0], axis=0))
    df_log_return.to_csv(log_return_file)

    # 3️⃣ Save the Percentage Change Data
    pct_change_file = os.path.join(feature_dir, f"{feature}_pct_change.csv")
    df_pct_change = df_pivot_cleaned.sub(df_pivot_cleaned.iloc[:, 0], axis=0).div(df_pivot_cleaned.iloc[:, 0], axis=0) * 100
    df_pct_change.to_csv(pct_change_file)

    print(f"Processed and saved files in: {feature_dir}")

# Final confirmation
print(f"All features processed! Cleaned datasets are saved inside: {main_dir}")

import pandas as pd
import numpy as np
import os

# Load the dataset
file_path = "nifty50.csv"  # Input file
df = pd.read_csv(file_path)

# Extract the dataset name without extension
dataset_name = os.path.splitext(os.path.basename(file_path))[0]

# Create the main directory based on dataset name
main_dir = f"data/{dataset_name}/"
os.makedirs(main_dir, exist_ok=True)

# Convert 'date' column to datetime and extract relevant parts
df['date'] = pd.to_datetime(df['date'])
df['date_only'] = df['date'].dt.date
df['time_only'] = df['date'].dt.time
df['weekday'] = df['date'].dt.strftime('%A')  # Extract day of the week

# Drop original date column
df.drop(columns=['date'], inplace=True)

# Remove all time columns after 15:25
time_threshold = pd.to_datetime("15:25:00").time()
df = df[df['time_only'] <= time_threshold]

# List of feature columns to process
feature_columns = ['open', 'high', 'low', 'sma5', 'sma10', 'sma15', 'close']

# Process each feature individually
for feature in feature_columns:
    feature_dir = os.path.join(main_dir, feature)
    os.makedirs(feature_dir, exist_ok=True)
    
    for weekday in df['weekday'].unique():
        # Filter data for the specific weekday
        df_weekday = df[df['weekday'] == weekday]
        df_feature = df_weekday[['date_only', 'time_only', feature]].copy()
        
        # Pivot to reshape data (date as rows, time as columns)
        df_pivot = df_feature.pivot(index='date_only', columns='time_only', values=feature)
        
        # Remove rows that have at least one null value
        df_pivot_cleaned = df_pivot.dropna()
        
        # Create directory for weekday
        weekday_dir = os.path.join(feature_dir, weekday)
        os.makedirs(weekday_dir, exist_ok=True)
        
        # 1️⃣ Save the Cleaned Raw Data (No Normalization)
        raw_file = os.path.join(weekday_dir, f"{feature}_{weekday}_raw.csv")
        df_pivot_cleaned.to_csv(raw_file)
        
        # 2️⃣ Save the Log Return Data
        log_return_file = os.path.join(weekday_dir, f"{feature}_{weekday}_log_return.csv")
        df_log_return = np.log(df_pivot_cleaned.div(df_pivot_cleaned.iloc[:, 0], axis=0))
        df_log_return.to_csv(log_return_file)
        
        # 3️⃣ Save the Percentage Change Data
        pct_change_file = os.path.join(weekday_dir, f"{feature}_{weekday}_pct_change.csv")
        df_pct_change = df_pivot_cleaned.sub(df_pivot_cleaned.iloc[:, 0], axis=0).div(df_pivot_cleaned.iloc[:, 0], axis=0) * 100
        df_pct_change.to_csv(pct_change_file)
        
        print(f"Processed and saved {feature} data for {weekday} in: {weekday_dir}")

# Final confirmation
print(f"All features processed! Cleaned datasets are saved inside: {main_dir}")
