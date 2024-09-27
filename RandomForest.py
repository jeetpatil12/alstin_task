import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the processed data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Preprocess the data
def preprocess_data(df):
    # Convert 'employees' column to numeric
    df['employees'] = df['employees'].str.split(' - ').str[0].astype(float)  # Taking lower bound as the number of employees
    
    # Handle missing values
    df.fillna(0, inplace=True)
    
    return df

# Function to perform Random Forest regression and provide insights
def perform_random_forest(file_path):
    df = load_data(file_path)
    df = preprocess_data(df)

    # Prepare data for modeling
    X = df[['employees', 'investors']]  # Features (predictors)
    y = df['funding']                    # Target (response)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions for the entire dataset
    df['predicted_funding'] = model.predict(X)

    # Evaluate the model
    mse = mean_squared_error(y_test, model.predict(X_test))
    r2 = r2_score(y_test, model.predict(X_test))
    
    # Print evaluation metrics
    print(f'Mean Squared Error: {mse:.2f}')
    print(f'R² Score: {r2:.2f}')

    # Print feature importances
    feature_importances = model.feature_importances_
    for i, col in enumerate(X.columns):
        print(f"Feature: {col}, Importance: {feature_importances[i]:.4f}")

    # Display insights for each company
    df['funding_difference'] = df['predicted_funding'] - df['funding']
    print("\nInsights for Each Company:")
    for index, row in df.iterrows():
        print(f"Company: {row['name']}, Actual Funding: ${row['funding']:,.2f}, "
              f"Predicted Funding: ${row['predicted_funding']:,.2f}, "
              f"Funding Difference: ${row['funding_difference']:,.2f}, "
              f"Employees: {row['employees']}, Investors: {row['investors']}")

# Example usage
file_path = 'processed_output.csv'  # Ensure this is the path to your processed CSV
perform_random_forest(file_path)
