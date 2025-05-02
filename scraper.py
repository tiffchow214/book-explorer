import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = []
for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]
    price = book.select_one(".price_color").text
    rating = book.p["class"][-1]
    books.append({"title": title, "price": price, "rating": rating})

df = pd.DataFrame(books)
df.to_csv("books.csv", index=False)