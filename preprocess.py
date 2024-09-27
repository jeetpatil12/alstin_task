import pandas as pd
import re

# Function to convert funding string to float
def convert_funding(funding):
    if isinstance(funding, str):
        # Remove whitespace and dollar sign
        funding = funding.strip().replace('$', '')
        print(f"Processing funding: '{funding}'")  # Debugging output
        # Check for millions or billions and convert accordingly
        match = re.match(r'([\d.,]+)([MB]?)', funding)
        if match:
            value, unit = match.groups()
            value = float(value.replace(',', ''))  # Remove commas for conversion
            if unit == 'M':
                return value * 1_000_000  # Convert millions to float
            elif unit == 'B':
                return value * 1_000_000_000  # Convert billions to float
            else:
                return value  # If no unit, return the raw value
        print("No match found, returning None.")  # Debugging output
        return None  # If it doesn't match, return None
    return funding  # If not a string, return as is

# Read the CSV file
def preprocess_csv(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Selecting only necessary columns for investment
        necessary_columns = ['name', 'funding', 'investors', 'employees', 'location', ]
        df = df[necessary_columns]

        # Convert funding to numeric
        df['funding'] = df['funding'].apply(convert_funding)

        # Handle missing values by filling them with 'N/A' or drop rows if necessary
        df.fillna("N/A", inplace=True)

        # Remove any duplicates
        df.drop_duplicates(subset=['name'], inplace=True)

        print("Processed DataFrame:")
        print(df)

        # Save the processed data to a new CSV file
        df.to_csv('processed_output.csv', index=False)
        print("Processed data saved to 'processed_output.csv'.")

    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")

# Example usage
file_path = 'output.csv'  # Change this to your actual file path
preprocess_csv(file_path)
