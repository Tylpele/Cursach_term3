from bs4 import BeautifulSoup
import requests
import html_dicts


def get_product_price_static(url, website_name):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        print("Не удалось подключиться к сайту")
        return None

    block = html_dicts.static_dic[website_name][0][0]
    block_class = html_dicts.static_dic[website_name][0][1]
    price_block = soup.find(block, class_=block_class)

    if price_block is not None:
        price_text = price_block.text.strip()
        price = price_text.replace(" ", "").replace(",", ".").replace("₽", "").replace("\xa0", "")
        return int(float(price))

    print("Цена не найдена на странице.")
    return None


def get_product_price_e2e4(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        print("Не удалось подключиться к сайту")
        return None

    # на е2е4 два варианта класса для цен
    block = html_dicts.static_dic["e2e4online"][0][0]
    block_class1 = html_dicts.static_dic["e2e4online"][0][1][0]
    block_class2 = html_dicts.static_dic["e2e4online"][0][1][1]
    price_block1 = soup.find(block, class_=block_class1)
    price_block2 = soup.find(block, class_=block_class2)

    if price_block1 is not None:
        price_text = price_block1.text.strip()
        price = price_text.replace(" ", "").replace(",", ".").replace("₽", "").replace("\xa0", "")
        return int(float(price))

    if price_block2 is not None:
        price_text = price_block2.text.strip()
        price = price_text.replace(" ", "").replace(",", ".").replace("₽", "").replace("\xa0", "")
        return int(float(price))

    print("Цена не найдена на странице.")
    return None


def get_product_name_static(url, website_name):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
    except:
        print("Не удалось подключиться к сайту")
        return None

    block = html_dicts.static_dic[website_name][1][0]
    block_class = html_dicts.static_dic[website_name][1][1]
    name_block = soup.find(block, class_=block_class)

    if name_block is not None:
        return name_block.text
    else:
        return None
