from parsers.site1 import parse_site1
from parsers.site2 import parse_site2

def main():

    target_urls = [
        {
            "url": "https://cybersecuritynews.com/", 
            "type": "html"
        },
        {
            "url": "https://www.bleepingcomputer.com/",
            "type": "rss"
        }
    ]    

    for i in target_urls:
        if i["type"] == "html" :
            print("HTML parsing required...")

            parse_site1(i["url"], "cybernews_alldata.json")


        elif i["type"] == "rss":
            print("RSS parsing required...")  

            parse_site2(i["url"], "bleepingcomputer_alldata.json")
        else:
            print("DETAILS NEEDED")


if __name__ == "__main__":
    main()
    input()