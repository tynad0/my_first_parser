from bs4 import BeautifulSoup
import requests
from datetime import datetime
from utils.save_to_json import save_to_json
from utils.load_existing_data import load_existing_data
from utils.save_to_excel import save_to_excel
import time

def parse_site1(url, filename):
    # ----------------------------------------------------------------------
    existing_news = load_existing_data(filename)
    existing_links = set(i["news_link"] for i in existing_news)

    relevant_news = []  
    # ----------------------------------------------------------------------
    key_words = [ "data breach","method"]

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    })

    for i in key_words:
        page = 1
        while True:  
            filtered_key_word = (i.strip()).replace(" ", "+")
            new_url = url + "page/" + str(page) + "?s=" + filtered_key_word

            try:
                res = session.get(new_url)
                res.raise_for_status()

                soup = BeautifulSoup(res.text, "lxml")

                content_main = soup.find("div", class_="td-ss-main-content")
                content_block = content_main.find_all(class_="td_module_16")
                just_to_know = soup.find("h1").find("span", class_="td-search-query").get_text(strip=True)

                for a in content_block:
                    date = a.find("span", class_="td-post-date").get_text(strip=True)

                    news_date = datetime.strptime(date, "%B %d, %Y")

                    if news_date.year >= 2024:
                        title = a.find(class_="item-details").find("h3").find("a").get_text(strip=True)
                        news_link = a.find(class_="item-details").find("h3").find("a").get("href")
                        author = a.find("span", class_="td-post-author-name").find("a").get_text(strip=True)
                        author_link = a.find("span", class_="td-post-author-name").find("a").get("href")
                        excerpt = a.find("div", class_="td-excerpt").get_text(strip=True)

                        # Здесь я проверяю есть ли уже такая новость 
                        if news_link not in existing_links:
                            relevant_news.append({
                                "keyword": just_to_know,
                                "author": author,
                                "author_link": author_link,
                                "date": date,
                                "title": title,
                                "news_link": news_link,
                                "excerpt": excerpt
                            })
                            existing_links.add(news_link)  # это я добавляю в сет, чтобы было видно что добавилось

                            print("Добавлено:", title)
                        else:
                            print("Уже есть:", title)

                    else:
                        print("Остальное Неактуально")
                        break

                else:
                    page += 1
                    time.sleep(1)
                    continue

                break  # Если break был я прерываю while True и он ищет след ключ слово

            except requests.exceptions.RequestException as e:
                print(f"Произошла ошибка \n {e}")
                break 

    # Здесь я объединяю новые и старые новости ( если новых нет то я обьединяю с пустым массивом ) - конкатенация - они следуют друг за другом
    all_news = existing_news + relevant_news
    save_to_json(filename, all_news)
    save_to_excel("cybersec_alldata.xlsx", all_news)

    return all_news
