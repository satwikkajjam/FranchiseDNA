"""
Data Processor Module - Cleans and prepares the Census 2011 population dataset.
"""
import pandas as pd
import os
from config import Config


def load_and_clean_dataset():
    """Load the raw Excel dataset and clean it for analysis."""
    raw_path = Config.RAW_DATASET_PATH
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Dataset not found at {raw_path}")

    df = pd.read_excel(raw_path)

    # Filter only 'Total' rows (not Rural/Urban splits) and exclude 'India' row
    df = df[(df['TRU'] == 'Total') & (df['Name'] != 'India')].copy()

    # Keep only useful columns and rename
    df = df[['Name', 'No_HH', 'TOT_P', 'TOT_WORK_P', 'P_LIT']].copy()
    df.columns = ['area', 'households', 'population', 'working_population', 'literate_population']

    # Calculate literacy rate as percentage
    df['literacy_rate'] = round((df['literate_population'] / df['population']) * 100, 2)

    # Clean area names - title case
    df['area'] = df['area'].str.strip().str.title()

    # Reset index
    df = df.reset_index(drop=True)

    return df


def save_cleaned_csv(df=None):
    """Save cleaned dataframe to CSV."""
    if df is None:
        df = load_and_clean_dataset()

    os.makedirs(os.path.dirname(Config.CLEANED_CSV_PATH), exist_ok=True)
    df.to_csv(Config.CLEANED_CSV_PATH, index=False)
    print(f"Cleaned data saved to {Config.CLEANED_CSV_PATH}")
    return df


def get_cleaned_data():
    """Get cleaned data from CSV cache or process fresh."""
    if os.path.exists(Config.CLEANED_CSV_PATH):
        return pd.read_csv(Config.CLEANED_CSV_PATH)
    return save_cleaned_csv()


if __name__ == '__main__':
    df = save_cleaned_csv()
    print(f"Processed {len(df)} areas")
    print(df.head(10).to_string())
