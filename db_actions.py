import pymysql
from datetime import time, timedelta, datetime


def make_sql_query(query: str, params):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='price_bot'
    )

    cursor = connection.cursor()

    cursor.execute(query, params)

    connection.commit()
    connection.close()

    return cursor.fetchall()


def add_product_to_db(user_id, link, product_name, price: int, min_price: int, _time: time):
    make_sql_query("INSERT INTO `old_price`(`tag`, `link`, `product_name`, `price`, `min_price`, `add_time`) VALUES ("
                   "%s, %s, %s, %s, %s, %s)",
                   (user_id, link, product_name, price, min_price, _time))


def delete_product_from_bd(user_id, link):
    make_sql_query("DELETE FROM old_price WHERE tag = %s AND link = %s", (user_id, link))


def get_product_list(user_id):
    results = make_sql_query("SELECT `product_name`, `price`, `link`, `min_price` FROM `old_price` WHERE tag = %s",
                             (user_id,))
    product_list = []
    for product_name, price, link, min_price in results:
        product_list.append([product_name, price, link, min_price])

    return product_list


def is_product_added_db(user_id, link):
    results = make_sql_query("SELECT * FROM `old_price` WHERE tag = %s AND link = %s",
                             (user_id, link))
    return len(results) > 0


def get_notification_senders_list(_time: time):
    """ Список товаров добавленных в промежутке (сейчас - полчаса назад; сейчас) любого дня"""
    min_time = (datetime.combine(datetime.today(), _time) - timedelta(minutes=30)).time()
    max_time = _time

    results = make_sql_query("SELECT `tag`, `product_name`, `link`, `price`, `min_price` FROM `old_price` "
                             "WHERE TIME(`add_time`) BETWEEN %s AND %s",
                             (min_time, max_time))
    return results


def update_product_prev_price(link, new_price: int):
    make_sql_query("UPDATE `old_price` SET `price` = %s WHERE link = %s",
                   (new_price, link))