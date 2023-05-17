import json

import requests
from bs4 import BeautifulSoup


def get_results(search_term, num_top_results):
    base_url = "https://www.google.com/search?q="
    search_term = search_term.replace(" ", "+")
    url = base_url + search_term + "&num=" + str(num_top_results)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result_divs = soup.find_all("div", attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"})
    position = 0
    with open('result.json', 'w', encoding='utf-8') as file:
        for div in result_divs:
            # print(div.prettify())
            website_info = {}
            position += 1
            website_info['position'] = position
            try:
                title = div.find("h3").getText()
                website_info['title'] = title
            except:
                website_info['title'] = ""

            try:
                result_url = div.find("a", href=True)['href']
                website_info['url'] = result_url.split('&')[0][7:]
            except:
                website_info['url'] = ""

            try:
                description = div.find("div", attrs={"class": "BNeawe s3v9rd AP7Wnd"}).getText()
                website_info['description'] = description
            except:
                website_info['description'] = ""

            json.dump(website_info, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    search_term = input("Enter search term: ")
    num_top_results = int(input("Enter number of results: "))
    get_results(search_term, num_top_results)

