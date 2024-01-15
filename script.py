from bs4 import BeautifulSoup
import requests
from datetime import datetime


def url_gen(page_number):
    url = f"https://uk.trustpilot.com/review/dreamcargiveaways.co.uk?page={page_number}"
    return url


def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        html = resp.content
        soup = BeautifulSoup(html, "lxml")
        return soup

    return None


def grab_data(soup):
    elements = soup.find_all("div", attrs={"data-service-review-rating": True})
    review_data = []
    for element in elements:
        data = {
            "review": element["data-service-review-rating"],
            "date": format_date(element.find("time")["datetime"]),
        }
        review_data.append(data)

    return review_data


def format_date(date):
    date = date.replace("Z", "")
    parsed_date = datetime.fromisoformat(date)
    return parsed_date.strftime("%Y-%m-%d")


def main():
    url = url_gen(1)
    soup = parse(url)

    data = grab_data(soup)
    print(data)


if __name__ == "__main__":
    main()
