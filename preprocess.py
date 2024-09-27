import pandas as pd
import re


def convert_funding(funding):
    if isinstance(funding, str):
        
        funding = funding.strip().replace('$', '')
        print(f"Processing funding: '{funding}'")  
        # Check for millions or billions and convert accordingly
        match = re.match(r'([\d.,]+)([MB]?)', funding)
        if match:
            value, unit = match.groups()
            value = float(value.replace(',', ''))  
            if unit == 'M':
                return value * 1_000_000  
            elif unit == 'B':
                return value * 1_000_000_000  
            else:
                return value  
        print("No match found, returning None.")  
        return None 
    return funding  


def preprocess_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        
        necessary_columns = ['name', 'funding', 'investors', 'employees', 'location', ]
        df = df[necessary_columns]

        df['funding'] = df['funding'].apply(convert_funding)

        df.fillna("N/A", inplace=True)

        df.drop_duplicates(subset=['name'], inplace=True)

        print("Processed DataFrame:")
        print(df)

        df.to_csv('processed_output.csv', index=False)
        print("Processed data saved to 'processed_output.csv'.")

    except Exception as e:
        print(f"An error occurred during preprocessing: {e}")

file_path = 'output.csv'  
preprocess_csv(file_path)
