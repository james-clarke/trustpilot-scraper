from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv


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
    try:
        if soup is None:
            raise ValueError("Error.")

        elements = soup.find_all("div", attrs={"data-service-review-rating": True})
        review_data = []
        for element in elements:
            try:
                review = element["data-service-review-rating"]
            except KeyError:
                review = "No rating"

            try:
                date_element = element.find("time")
                date = (
                    format_date(date_element["datetime"])
                    if date_element
                    else "Unknown date"
                )
            except (AttributeError, KeyError):
                date = "Unknown date"

            data = {
                "review": review,
                "date": date,
            }
            review_data.append(data)

        return review_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def format_date(date):
    date = date.replace("Z", "")
    parsed_date = datetime.fromisoformat(date)
    return parsed_date.strftime("%Y-%m-%d")


# Credit to: https://stackoverflow.com/a/952952
def flatten(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list


def write_to_csv(filename, data):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["review", "date"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    main_data_list = []
    for page_number in range(1, 323):
        url = url_gen(page_number)
        soup = parse(url)
        data = grab_data(soup)
        main_data_list.append(data)

    main_data_list = flatten(main_data_list)

    write_to_csv("data.csv", main_data_list)


if __name__ == "__main__":
    main()
