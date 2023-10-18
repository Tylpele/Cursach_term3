from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time


def get_product_price_dynamic(url, website_name):
    html_dic = {
        "wildberries": ["price-block__content", "price-block__final-price"],
        "ozon": ["e0", "ky6"]
    }

    browser = webdriver.Chrome('../chromedriver.exe')
    browser.get(url)

    awaiting_block = html_dic[website_name][0]
    price_block = html_dic[website_name][1]

    if awaiting_block is not None:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, awaiting_block)))
        price_elements = browser.find_element(By.CLASS_NAME, price_block)
        prices_html = BeautifulSoup(price_elements.get_attribute(
            'innerHTML'), features='lxml')
        time.sleep(1)
        # закрываем браузер после всех манипуляций
        browser.quit()
        price = prices_html.text.replace("₽", "").replace("\xa0", "")
        return int(price)
    else:
        print("Цена не найдена на странице.")
        return None
