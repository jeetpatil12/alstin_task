import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# Base URL of the website
base_url = "https://wellfound.com/10-of-10-in-2023"
page_url = "catalogue/page-{}.html"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_company_details(company_url):
    soup = get_soup(company_url)
    title = soup.findAll('h4', class_='heading-10')
    print(title)
    # title = soup.find('h1').text
    # price = soup.find('p', class_='price_color').text
    # stock = soup.find('p', class_='instock availability').text.strip()
    # description = soup.find('meta', attrs={'name': 'description'})['content'].strip()
    # product_type = soup.find('th', string='Product Type').find_next_sibling('td').text
    # price_incl_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
    # tax = soup.find('th', string='Tax').find_next_sibling('td').text
    # availability = soup.find('th', string='Availability').find_next_sibling('td').text
    # num_reviews = soup.find('th', string='Number of reviews').find_next_sibling('td').text
    # image_url = soup.find('img')['src']
    # # Convert relative URL to absolute URL
    # image_url = 'http://books.toscrape.com' + image_url.replace('../../', '/')
    # rating = soup.find('p', class_='star-rating')['class'][1]  # Extract the rating

    # return {
    #     'title': title,
    #     'price': price,
    #     'stock': stock,
    #     'description': description,
    #     'product_type': product_type,
    #     'price_incl_tax': price_incl_tax,
    #     'tax': tax,
    #     'availability': availability,
    #     'num_reviews': num_reviews,
    #     'image_url': image_url,
    #     'rating': rating
    # }

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    books = []
    for article in soup.find_all('article', class_='product_pod'):
        bookUrl = base_url + 'catalogue/' + article.a['href']
        bookDetails = scrape_company_details(bookUrl)
        books.append(bookDetails)
    return books

def scrape_all_pages():
    # Scrape data from the first 5 pages (adjust the range as needed)
    all_books = []
    for page in range(1, 51):
        url = base_url + page_url.format(page)
        books = scrape_page(url)
        all_books.extend(books)
        
    return all_books

def encode_data(data):
    # Encode the string data to bytes, then to base64, and back to a string
    return base64.b64encode(data.encode()).decode()


def store_books_in_mongodb(books):
    client = MongoClient("mongodb+srv://admin:admin@cluster0.nccwyqw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client['test']
    collection = db['books']
    encoded_books = []
    for book in books:
        encoded_book = {
        'title': encode_data(book['title']),
        'price': encode_data(book['price']),
        'stock': encode_data(book['stock']),
        'description': encode_data(book['description']),
        'product_type': encode_data(book['product_type']),
        'price_incl_tax': encode_data(book['price_incl_tax']),
        'tax': encode_data(book['tax']),
        'availability': encode_data(book['availability']),
        'num_reviews': encode_data(book['num_reviews']),
        'image_url': encode_data(book['image_url']),
        'rating': encode_data(book['rating'])
    }
        encoded_books.append(encoded_book)

    collection.insert_many(encoded_books)
    client.close()

if __name__ == '__main__':
    # books_data = scrape_all_pages()
    # store_books_in_mongodb(books_data)
    scrape_company_details(base_url)