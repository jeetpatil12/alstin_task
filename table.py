import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import csv
import pandas as pd


# Function to scrape the data
def scrape_table(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table - you might need to inspect the HTML structure for the correct selector
    table = soup.find('table')  # Adjust based on the actual structure of the page

    # # Extracting the table headers
    # headers = []
    # for th in table.find_all('th', scope='col'):
    #     headers.append(th.text.strip())

    # Extracting the table rows
    rows = []
    company_names= []
    for tr in table.find_all('tr')[1:]:  # Skip the first header row
        cells = tr.find_all('td')
        company_name = tr.find('div', class_='text-base font-semibold truncate').text.strip()
        company_names.append(company_name)
        row = [cell.text.strip() for cell in cells]
        rows.append(row)
    
    return company_names, rows

def generate_companies_json(company_names, rows):
    company_json = []
    for i in range(1, len(company_names) + 1):
        company_json.append({
            'name': company_names[i-1],
            'score': rows[i-1][1],
            'funding': rows[i-1][2],
            'investors': rows[i-1][3],
            'employees': rows[i-1][4],
            'industries': rows[i-1][5],
            'business_model': rows[i-1][6],
            'location': rows[i-1][7],
            'outsource': rows[i-1][8],
            'contact': rows[i-1][9],
        })
    return company_json

def generate_csv(json):
   # Convert the JSON data into a pandas DataFrame
    df = pd.DataFrame(json)

    # Generate CSV from the DataFrame
    df.to_csv('output.csv', index=False)

    print("CSV file generated successfully.")

def store_in_mongodb(json):
    client = MongoClient("mongodb+srv://admin:admin@cluster0.yj94m.mongodb.net/")
    db = client['data']
    collection = db['companies']

    collection.insert_many(json)
    client.close()
    generate_csv(json)

    print('done')

# URL of the website containing the table
url = "https://www.seedtable.com/manufacturing-startups-germany"  # Replace this with the actual URL

# Scrape the table and display it
companies, rows = scrape_table(url)
data = generate_companies_json(companies, rows)
store_in_mongodb(data)
