from main_parser import *
from aiogram import Bot, types, Dispatcher, executor

# def run_bot():
#
#
#     product_url = 'https://www.wildberries.ru/catalog/179432152/detail.aspx'
#     user_tag = 'test'
#
#     # стандартизация ссылки
#     if not product_url.startswith("https://www.") and not product_url.startswith("http://www."):
#         if not product_url.startswith("www."):
#             product_url = "https://www." + product_url
#         else:
#             product_url = "https://" + product_url
#
#     # копейки не учитываются в ценах, цены в int
#     price = get_product_price(product_url)
#     prev_price = get_prev_price(product_url, user_tag)
#
#     # if price:
#     #     print(f"Цена товара: {price}")
#     #     print(f"Предыдущая цена товара: {prev_price}")
#     #     if price < prev_price:
#     #         print("скидка")

TOKEN_API = "5634121116:AAEE-utFMkGewUNOOKPAKv-ai89ogJL8a3c"
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


# команда /start
@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Привет!\n"
                                            "\n"
                                            "Этот бот поможет вам отслеживать изменение цен на товары. Нажмите \"Добавить товар\",\n"
                                            "чтобы начать отслеживание. Также вы можете посмотреть список отслеживаемых товаров "
                                            "и удалить товары, которые уже вам не интересны.\n"
                                            "При изменении цены отслеживаемого товара бот пришлет вам уведомление в течение нескольких часов.\n"
                                            "\n"
                                            "<b>Сайты, на которых в данный момент возможен трекинг цен:</b>\n"
                                            "Aliexpress, e2e4, Citilink, Wildberries, Ozon.\n"
                                            "В будущем список будет пополняться.\n"
                                            "\n"
                                            "Ссылки типа bit.ly, goo.gl и другие сокращенные ссылки считываться <b>не</b> будут.", parse_mode="HTML")


# отправка уведомления
async def send_notification(user_id, link, price: int, prev_price: int):
    await bot.send_message(user_id,
                           f"Товар по ссылке {link} теперь стоит <b>{price}₽</b>. <i>(пред. цена {prev_price}₽)</i>."
                           f"Цена снизилась на {prev_price - price}₽.", parse_mode="HTML")
                            # кнопка "отменить отслеживание"


# главное меню
# "Нажмите на одну из кнопок ниже."
#
# "<b>Сайты, на которых в данный момент возможен трекинг цен:</b>"
# "Aliexpress, e2e4, Citilink, Wildberries, Ozon."
#
# "Ссылки типа bit.ly, goo.gl и другие сокращенные ссылки считываться <b>не</b> будут."
#
#   снизу три кнопки .


# кнопка "добавить товар"
# "Скиньте ссылку на товар: "
# 2 варианта: 1 - ссылка не считалась - "Ссылка введена некорректно или сайта нет в базе."
#             2 - ссылка считалась - "Какая цена товара вас устроит? Напишите 0, если размер скидки не важен."
#                 занести в бд тег юзера, ссылку, время ввода ссылки, мин. цену товара
#
# возвращение в главное меню


# кнопка "посмотреть товары"
# ?


# кнопка "удалить товар"
# ?

def run_bot():
    executor.start_polling(dp)
