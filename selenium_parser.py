import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_data(url):
    headers = {
        'Accep': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',

    }

    r = requests.get(url=url, headers=headers)

    with open('index.html', 'w', encoding='UTF-8') as file:
        file.write(r.text)


    get_hostl_url = 'https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=en&sort=most&hotel_link=/hotel/%HOTEL_ID%&'

    r = requests.get(url=get_hostl_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    hotels_card = soup.find_all('div', class_='hotel_card_dv')

    for hotel_url in hotels_card:
        hotel_url = 'https://www.rsrv.me' + hotel_url.find('a').get('href')
        print(hotel_url)


def get_data_in_selenium(url):
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0')
    try:
        driver = webdriver.Firefox(
            executable_path='C:\\Users\\79857\\PycharmProjects\\MillionAgents_TEST\\geckodriver.exe',
            options=options
        )
        driver.get(url=url)
        time.sleep(5)
        with open('index_selenium111.html', 'w', encoding='UTF-8') as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_data_in_selenium('https://www.youtube.com/c/PythonHubStudio/about')


if __name__ == '__main__':
    main()