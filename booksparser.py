import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
host = "https://books.toscrape.com/"
link = "https://books.toscrape.com/catalogue/page-1.html"
headers = {"user-agent": user}
csvfile = "books.csv"

def get_html(link):
    r = requests.get(link, headers=headers)
    r.encoding = "utf-8"
    return r

def get_content(url):
    soup = BeautifulSoup(get_html(url).text, "html.parser")
    items = soup.find_all("li", class_="col-xs-6")
    books = []
    for item in items:
        rating_tag = item.find("p", class_="star-rating")
        if rating_tag:
            rating = rating_tag.get("class")[1]  # second class contains rating
        else:
            rating = "No rating"
        books.append(
            {
                "title": item.find("h3").get_text(),
                "price": item.find("p", class_="price_color").get_text(),
                "stars": rating,
                "stock": item.find("p", class_="instock").get_text().strip(),
                "link": "".join([host, item.find("a")["href"].replace('../../../', 'catalogue/')]),
            }
        )
    return books

def save_content(items, file):
    writer = csv.writer(file, delimiter=";")
    for item in items:
        writer.writerow([item["title"], item["price"], item["stars"], item["stock"], item["link"]])

def parser():
    pages = int(input("How many pages do you want?: ").strip())
    html = get_html(link)
    counter = 0

    if html.status_code == 200:
        with open(csvfile, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Title", "Price","Stars", "Stock", "Link"])

            for i in range(1, pages + 1):
                new_books = get_content(f"https://books.toscrape.com/catalogue/page-{i}.html")
                counter += len(new_books)
                save_content(new_books, file)
                print(f"Parsed page № {i}")

        print("✅ Finished! Data saved to CSV.")
        print(f"{counter} pages were successfully saved to CSV.")
    else:
        print("❌ Something went wrong")
parser()