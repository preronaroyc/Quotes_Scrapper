import sqlite3

# Function to create a database and a table 
def create_database(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute('''
                   CREATE TABLE quotes(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quote TEXT NOT NULL,
                       author TEXT NOT NULL,
                       tags TEXT NOT NULL
                   )
                   ''')
    con.commit()
    con.close()
    print("Created database and table quotes!")
    
# Function to insert data in table
def insert_quotes(db_name, quotes):
    # Converting values of quotes to string before insertion
    quotes = [(str(quote or ""), str(author or ""), str(tags or "")) for quote, author, tags in quotes]
    
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.executemany(''' 
                       INSERT INTO quotes(quote, author, tags)
                       VALUES(?,?,?)
                       ''', quotes)
    con.commit()
    con.close()
    print(f"Inserted quotes in table quotes!")
    
# Function to query database
def query(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute('''
                   SELECT *
                   FROM quotes
                   ''')
    rows = cursor.fetchall()
    con.close()
    return rows

if __name__ == "__main__":
    # Extract all rows from scrape_db database
    rows = query("scrape_db")
    
    # Print first 5 rows
    for row in rows[:5]:
        print(f"Quote: {row[1]}, Author: {row[2]}, Tags: {row[3]}")
