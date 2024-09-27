import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pandas as pd

# Function to scrape the data
def scrape_table(url):
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")
            return None, None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            print("Table not found on the webpage.")
            return None, None

        rows = []
        company_names = []
        for tr in table.find_all('tr')[1:]:
            cells = tr.find_all('td')
            company_name = tr.find('div', class_='text-base font-semibold truncate')
            company_names.append(company_name.text.strip() if company_name else "N/A")
            row = [cell.text.strip() if cell else "N/A" for cell in cells]
            rows.append(row)
        
        return company_names, rows
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None, None

# Generate JSON structure from scraped data
def generate_companies_json(company_names, rows):
    company_json = []
    try:
        for i in range(len(company_names)):
            row = rows[i] if i < len(rows) else ["N/A"] * 10
            company_json.append({
                'name': company_names[i],
                'score': row[1] if len(row) > 1 else "N/A",
                'funding': row[2] if len(row) > 2 else "N/A",
                'investors': row[3] if len(row) > 3 else "N/A",
                'employees': row[4] if len(row) > 4 else "N/A",
                'industries': row[5] if len(row) > 5 else "N/A",
                'business_model': row[6] if len(row) > 6 else "N/A",
                'location': row[7] if len(row) > 7 else "N/A",
                'outsource': row[8] if len(row) > 8 else "N/A",
                'contact': row[9] if len(row) > 9 else "N/A",
            })
    except IndexError as e:
        print(f"An error occurred while generating JSON: {e}")
    return company_json

# Convert JSON data into CSV
def generate_csv(json_data):
    try:
        df = pd.DataFrame(json_data)
        df.to_csv('output.csv', index=False)
        print("CSV file generated successfully.")
    except Exception as e:
        print(f"An error occurred while generating CSV: {e}")

# Store data in MongoDB and then generate CSV
def store_in_mongodb(json_data):
    try:
        client = MongoClient("mongodb+srv://admin:admin@cluster0.yj94m.mongodb.net/")
        db = client['data']
        collection = db['companies']
        collection.insert_many(json_data)
        client.close()
        print("Data stored in MongoDB successfully.")
        generate_csv(json_data)
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")

# URL of the website to scrape
url = "https://www.seedtable.com/manufacturing-startups-germany"  

companies, rows = scrape_table(url)
if companies and rows:
    data = generate_companies_json(companies, rows)
    if data:
        store_in_mongodb(data)