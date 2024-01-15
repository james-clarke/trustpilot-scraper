from bs4 import BeautifulSoup
import requests


def url_gen(page_number):
    url = f"https://uk.trustpilot.com/review/dreamcargiveaways.co.uk?page={page_number}"
    return url


def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
    }
    resp = requests.get(url, headers=headers)
    html = resp.content
    soup = BeautifulSoup(html, "lxml")
    return soup


def main():
    url = url_gen(1)
    print(url)
    


if __name__ == "__main__":
    main()
