from bs4 import BeautifulSoup
import requests


def get_product_price_static(url, website_name):
    html_dic = {
        "aliexpress": ["div", "snow-price_SnowPrice__mainS__jlh6el"],
        "e2e4online": ["div", "price-block__price _WAIT"],
        "citilink": ["span", "e1j9birj0 e106ikdt0 app-catalog-1f8xctp e1gjr6xo0"],
    }

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        print("Не удалось подключиться к сайту")
        return None

    block = html_dic[website_name][0]
    block_class = html_dic[website_name][1]
    price_block = soup.find(block, class_=block_class)

    if price_block is not None:
        price_text = price_block.text.strip()
        price = price_text.replace(" ", "").replace(",", ".").replace("₽", "").replace("\xa0", "")
        return int(price)
    else:
        print("Цена не найдена на странице.")
        return None
