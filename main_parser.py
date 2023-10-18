import pymysql
from html_info import *
from static_parser import *
from dynamic_parser import *


def get_product_price(url):
    static_sites = ["aliexpress", "e2e4online", "citilink"]
    dynamic_sites = ["wildberries", "ozon"]

    # получить название домена сайта
    website_name = get_website_name(url)

    if website_name in static_sites:
        return get_product_price_static(url, website_name)
    elif website_name in dynamic_sites:
        return get_product_price_dynamic(url, website_name)
    else:
        print("Данного сайта нет в базе")
        return None


def get_prev_price(url, user_tag):
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='price_bot'
        )

        cursor = connection.cursor()

        query = "SELECT price FROM old_price WHERE tag = %s AND link = %s"
        cursor.execute(query, (user_tag, url))

        result = cursor.fetchone()

        if result:
            price = result[0]
            return price
        else:
            return None

    except Exception as e:
        print("Ошибка при выполнении запроса:", str(e))
        return None

    finally:
        if connection:
            connection.close()
