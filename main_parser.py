import pymysql
from html_info import *
from static_parser import *
from dynamic_parser import *
import sites_list


def get_product_price(url):
    # получить название домена сайта
    website_name = get_website_name(url)

    if website_name == "megamarket":
        return get_product_price_sber(url, website_name)

    if website_name == "e2e4online":
        return get_product_price_e2e4(url)

    if website_name in sites_list.static_sites:
        return get_product_price_static(url, website_name)

    if website_name in sites_list.dynamic_sites:
        return get_product_price_dynamic(url, website_name)

    return None


def get_prev_price(url, user_id):
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='price_bot'
        )

        cursor = connection.cursor()

        query = "SELECT price FROM old_price WHERE tag = %s AND link = %s"
        cursor.execute(query, (user_id, url))

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


def get_product_name(url):
    website_name = get_website_name(url)

    if website_name in sites_list.static_sites:
        return get_product_name_static(url, website_name)
    elif (website_name in sites_list.dynamic_sites) and (website_name != "megamarket"):
        return get_product_name_dynamic(url, website_name)
    elif (website_name in sites_list.dynamic_sites) and (website_name == "megamarket"):
        return get_product_name_sber(url, website_name)
    else:
        return None
