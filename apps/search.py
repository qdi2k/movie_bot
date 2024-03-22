import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get

from apps.useragent import get_useragent

load_dotenv()


def search_query(query, type_movie='series'):
    term = f'site:www.kinopoisk.ru/{type_movie} {query}'
    resp = get(
        url="https://www.google.com/search",
        headers={"User-Agent": get_useragent()},
        params={"q": term, "hl": "ru"},
        timeout=5
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    result_block = soup.find_all("div", attrs={"class": "g"})
    if result_block:
        for result in result_block:
            link = result.find("a", href=True)
            title = result.find("h3")
            description = result.find("div", {"style": "-webkit-line-clamp:2"})
            if link and title and description:
                if link["href"].split("/")[-2].isdigit():
                    return {
                        'link': f'https://w2.kpfr.wiki/{type_movie}/'
                                f'{link["href"].split("/")[-2]}',
                        'title': title.text,
                        'description': description.text[:-4] + '...',
                    }
    return None


if __name__ == '__main__':
    print(search_query('теория большого взрыва'))
