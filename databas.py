import sqlite3
from urllib.request import urlopen as uReq
import random
from bs4 import BeautifulSoup as soup

myurl = "https://books.toscrape.com/catalogue/"
def scrape():
    for i in range(1,50):
        uClient = uReq(myurl+"page-"+str(i)+".html")
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        bookshelf = page_soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
        for books in bookshelf:
            book_title = books.h3.a["title"]
            book_price = books.findAll("p", {"class": "price_color"})
            price = book_price[0].text.strip()
            price1=price.replace("£", "")
            insert_book(book_title, price1)

def insert_book(Title, Price):
    query = "INSERT INTO Books(Title, Price) " "VALUES(?, ?)"
    args = (Title, Price)
    try:
        con = sqlite3.connect("databas.db")
        cur = con.cursor()
        cur.execute(query, args)
        if cur.lastrowid:
            print("last inserted id", cur.lastrowid)
        else:
            print("last inserted id not found")
        con.commit()
    except sqlite3.Error as error:
        print(error)

#below code connects to database and selects the ID from books table
#and fetch all of the id to then use to create a random int for amount
def create_random_amount_db():
    con3 = sqlite3.connect("databas.db")
    cur3 = con3.cursor()
    ID = "SELECT ID FROM books"
    cur3.execute(ID)
    records = cur3.fetchall()
    for row in records:
        rands = random.randint(1,30)
        queries2 = f"UPDATE books SET Amount = {rands} WHERE ID = {row[0]}"
        cur3.execute(queries2)
    con3.commit()

def main():
    create_random_amount_db()
    #scrape()
    #insert_book("temp", "£20")
if __name__ == "__main__":
    main()
