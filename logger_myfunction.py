import requests
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime

file_path = 'log_file.txt'

keywords = ['дизайн', 'фото', 'web', 'python']

headers = {
    'Cookie': '_ym_d=1638026663; _ym_uid=1609598471639506820; _ga=GA1.2.1877746598.1638026663; hl=ru; fl=ru; '
              '__gads=ID=060adc68d899746f-229e145d24cd0034:T=1642620115:S=ALNI_MbR-NRmbEzkTAF2g9wScu8RBFOkVQ; '
              '_gid=GA1.2.2022388619.1644769484; _ym_isad=2; visited_articles=488720:280238:553900; _gat=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.174 YaBrowser/22.1.2.834 Yowser/2.5 Safari/537.36 '
}

url = 'https://habr.com/ru/all/'
ret = requests.get(url, headers=headers)
ret.raise_for_status()
source = ret.text
soup = BeautifulSoup(source, 'lxml')
articles = soup.find_all('article')


def get_log_path(path):
    def get_logfile(some_function):
        def foo(*args, **kwargs):
            result = some_function(*args, **kwargs)
            file_line = ('***<{}> Функция:<{}> Args:<{}> Kwargs:<{}> Результат:<{}>\n'.format(datetime.now()
                                                                                              .strftime(
                "%d %B %Y, %H:%M:%S"), some_function.__name__, args, kwargs, result))
            with open(path, 'a+', encoding='utf-8') as file:
                file.write(file_line)
            return result

        return foo

    return get_logfile


@get_log_path(file_path)
def web_scrapper(some_keywords):
    for article in articles:
        headline = article.find('h2').text
        hubs = article.find('a', class_='tm-article-snippet__hubs-item-link').text
        post_preview = article.find('div').text
        post_link = article.find('a', class_='tm-article-snippet__title-link').get('href')
        public_date = article.find('span', class_='tm-article-snippet__datetime-published').text

        for search_word in some_keywords:
            if (search_word.lower() in headline.lower()) or (search_word.lower() in post_preview.lower()) or \
                    (search_word.lower() in hubs.lower()):
                pprint(f'Дата: {public_date} - Заголовок: {headline} - Ссылка: habr.com{post_link}')
    return [public_date, headline, 'habr.com' + post_link]


if __name__ == '__main__':
    web_scrapper(keywords)
