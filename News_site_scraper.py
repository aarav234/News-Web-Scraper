from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from  sqlite4  import  SQLite4

# Init database object, singleton pattern restricts multiple objects per db
database = SQLite4("news_article_database.db")
# Connect to db and creates execution thread
database.connect()
# Create test database and specify columns
database.create_table("news_articles", ["caption", "img_url", "article_url", "author", "date_time"])

# Using urllib to access the news site
url = "https://timesofindia.indiatimes.com/"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
# Finding all Headline articles on the times of india news site
headline_articles = soup.find_all("figure", {"class": "_YVis"})
# Iterating through the list to acces each article
for article in headline_articles:
    try:
        # finding relevent information on the article
        caption = article.a.div.div.img.attrs["alt"]
        img_url = article.a.div.div.img.attrs["src"]
        article_url = article.a.attrs["href"]
        new_html = urlopen(article_url)
        new_soup = BeautifulSoup(new_html, "html.parser")
        # going into each article to find the author and the date and time stamps
        article_meta_data = new_soup.find_all("div", {"class": "byline"})
        try:
            for item in article_meta_data:
                author = item.a.get_text()
                date_time = item.span.get_text()
                database.insert("news_articles", {"caption": caption , "img_url": img_url, "article_url": article_url, "author": author, "date_time": date_time})

        except AttributeError:
            pass
    except AttributeError:
        pass


    