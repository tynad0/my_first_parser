import requests
from datetime import datetime
from utils.save_to_json import save_to_json
from utils.load_existing_data import load_existing_data
from utils.save_to_excel import save_to_excel
import time
import feedparser

def parse_site2(url, filename) :

    existing_news = load_existing_data(filename)
    existing_links = set(i["news_link"] for i in existing_news)


    relevant_news = []

    rss_url  = url + "feed/"

    feed = feedparser.parse(rss_url)
    
    for e in feed.entries:
        title = e.title
        news_link = e.link
        author = e.author
        date = e.published
        excerpt = e.summary
        
        print(f"{date} --> {title} --> {news_link} --> {author} --> {excerpt}")

        if news_link not in existing_links:
            relevant_news.append(
                {
                    "author": getattr(e, "author", "Unknown"),
                    "author_link": None,
                    "date": getattr(e, "published", "Unknown date"),
                    "title": title,
                    "news_link": news_link,
                    "excerpt": getattr(e, "summary", "")
                }
            )
            existing_links.add(news_link)
            print("Добавлено:", title)
        else:
            print("Уже есть:", title)
            

    all_news = existing_news + relevant_news
    save_to_json(filename, all_news)
    save_to_excel("bleepingcomputer_alldata.xlsx", all_news)

    return all_news