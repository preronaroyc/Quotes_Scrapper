# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import sqlite3
from data_handle import create_database, insert_quotes

BASE_URL = "https://quotes.toscrape.com/page/{}/"

# Function to scrape quote, author name and keywords
def scrape_quotes(page):
    url = BASE_URL.format(page) 
    response = requests.get(url)
    
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes_div = soup.find_all("div", class_ = "quote")
    quotes = []
    
    for quote in quotes_div:
        text = quote.find("span", class_ = "text").get_text(strip = True)
        author = quote.find("small", class_ = "author").get_text(strip = True)
        tags = quote.find_all("a", class_ = "tag")
        tags = [tag.get_text(strip = True) for tag in tags]
        quotes.append((text, author, tags))
    return quotes

#Function to repeat scrapping in all pages
def scrape_all_quotes():
    page = 1
    all_quotes = []
    
    while(page):
        quotes = scrape_quotes(page)
        if not quotes:
            break;
        all_quotes.extend(quotes)
        print(f"Scrapped all quotes of page {page}")
        page = page + 1
    return all_quotes

if __name__ == "__main__":
    # Create a database "scrape_db"
    create_database(db_name = "scrape_db")
    
    # Scrape all quotes from url
    all_quotes = scrape_all_quotes()
    
    print(f"Scrapped a total of {len(all_quotes)}")
    #print(all_quotes[0])
    
    # Insert quotes into quotes table in scrape_db database
    insert_quotes(db_name = "scrape_db", quotes = all_quotes)
    

    