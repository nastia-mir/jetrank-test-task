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
    result = {}
    position = 0
    for div in result_divs:
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

        result[f'res{position}'] = website_info

    with open(f'result_{search_term}_{num_top_results}.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    search_term = input("Enter search term: ")
    num_top_results = int(input("Enter number of results: "))
    get_results(search_term, num_top_results)

