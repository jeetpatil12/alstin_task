import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Convert 'employees' column to numeric
    df['employees'] = df['employees'].str.split(' - ').str[0].astype(float)  # Taking lower bound as the number of employees
    
    # Handle missing values
    df.fillna(0, inplace=True)
    
    return df

def perform_random_forest(file_path):
    df = load_data(file_path)
    df = preprocess_data(df)

    X = df[['employees', 'investors']]  # Features (predictors)
    y = df['funding']                    # Target (response)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    df['predicted_funding'] = model.predict(X)

    mse = mean_squared_error(y_test, model.predict(X_test))
    r2 = r2_score(y_test, model.predict(X_test))

    print(f'Mean Squared Error: {mse:.2f}')
    print(f'R² Score: {r2:.2f}')

    # Display investment insights for each company
    df['funding_difference'] = df['predicted_funding'] - df['funding']
    df['suggested_funding'] = df['predicted_funding'] * 1.20  # Suggesting 20% more than predicted funding
    
    print("\nInvestment Insights for Each Company:")
    for index, row in df.iterrows():
        if row['funding_difference'] > 0:
            investment_message = (
                f"Company: {row['name']}, "
                f"Actual Funding: ${row['funding']:,.2f}, "
                f"Predicted Funding: ${row['predicted_funding']:,.2f}, "
                f"Funding Difference: ${row['funding_difference']:,.2f}, "
                f"Suggested Funding Needed: ${row['suggested_funding']:,.2f}. "
                f"Recommendation: This company may benefit from additional investment to capitalize on growth opportunities. "
                f"Consider engaging with them to explore potential funding options."
            )
        else:
            investment_message = (
                f"Company: {row['name']}, "
                f"Actual Funding: ${row['funding']:,.2f}, "
                f"Predicted Funding: ${row['predicted_funding']:,.2f}. "
                f"Recommendation: The company appears well-funded relative to its predicted needs. "
                f"Monitor their growth but prioritize other opportunities for investment."
            )
        
        print(investment_message)


file_path = 'processed_output.csv'  
perform_random_forest(file_path)
