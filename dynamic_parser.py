from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import html_dicts


def get_product_price_sber(url, website_name):
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(webdriver, 10)
    apear_button = wait.until(EC.presence_of_element_located(By.CLASS_NAME,
                                                             "my-modal-plugin-window my-modal my-modal_theme_default my-modal_size_md profile-address-confirm"))
    close_button = browser.find_element(EC.element_to_be_clickable((By.CLASS_NAME, 'close-button')))
    close_button.click()
    awaiting_block = html_dicts.dynamic_dic[website_name][0][0]
    price_block = html_dicts.dynamic_dic[website_name][0][1]
    if awaiting_block is not None:
        WebDriverWait(browser, 100000).until(EC.presence_of_element_located(
            (By.CLASS_NAME, awaiting_block)))
        price_elements = browser.find_element(By.CLASS_NAME, price_block)
        prices_html = BeautifulSoup(price_elements.get_attribute(
            'innerHTML'), features='lxml')
        time.sleep(1)
        # закрываем браузер после всех манипуляций
        browser.quit()
        price = prices_html.text.replace("₽", "").replace("\xa0", "").replace("\u2009", "")
        return int(price)
    else:
        print("Цена не найдена на странице.")
        return None


def get_product_name_sber(url, website_name):
    return 0


def get_product_price_dynamic(url, website_name):
    browser = webdriver.Chrome()
    browser.get(url)

    awaiting_block = html_dicts.dynamic_dic[website_name][0][0]
    price_block = html_dicts.dynamic_dic[website_name][0][1]

    if awaiting_block is not None:
        WebDriverWait(browser, 100000).until(EC.presence_of_element_located(
            (By.CLASS_NAME, awaiting_block)))
        price_elements = browser.find_element(By.CLASS_NAME, price_block)
        prices_html = BeautifulSoup(price_elements.get_attribute(
            'innerHTML'), features='lxml')
        time.sleep(1)
        # закрываем браузер после всех манипуляций
        browser.quit()
        price = prices_html.text.replace("₽", "").replace("\xa0", "").replace("\u2009", "")
        return int(price)
    else:
        print("Цена не найдена на странице.")
        return None


def get_product_name_dynamic(url, website_name):
    browser = webdriver.Chrome()
    browser.get(url)

    awaiting_block = html_dicts.dynamic_dic[website_name][1][0]
    name_block = html_dicts.dynamic_dic[website_name][1][1]

    if awaiting_block is not None:
        WebDriverWait(browser, 10000).until(EC.presence_of_element_located(
            (By.CLASS_NAME, awaiting_block)))
        name_elements = browser.find_element(By.TAG_NAME, name_block)
        names_html = BeautifulSoup(name_elements.get_attribute(
            'innerHTML'), features='lxml')
        time.sleep(1)
        # закрываем браузер после всех манипуляций
        browser.quit()
        name = names_html.text
        return name
    else:
        print("Название не найдено на странице.")
        return None
