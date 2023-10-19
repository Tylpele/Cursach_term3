from main_parser import *
from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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
dp = Dispatcher(bot, storage=MemoryStorage()) #разрешение боту юзать оперативку или как-то так
storage = MemoryStorage() # доступ к опративки в целом для машины состояний


class State(StatesGroup):
    waiting_add_url= State()
    waiting_delete_url=State()

# команда /start
@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True) #cоздание кнопки
    btn_add = types.KeyboardButton("Добавить товар") #текст кнопки
    btn_delete = types.KeyboardButton("Удалить товар")
    btn_watch_product=types.KeyboardButton("Посмотреть товары")
    keyboard.add(btn_add) #добавление кнопки на клавиатуру
    keyboard.add(btn_delete, btn_watch_product)
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
                                            "Ссылки типа bit.ly, goo.gl и другие сокращенные ссылки считываться <b>не</b> будут.", parse_mode="HTML", reply_markup=keyboard)



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

#НЕ ТРОГАТЬ задания состоянния для ожидания url
@dp.message_handler(lambda message: message.text == "Добавить товар") #обработка нажатия кнопки по её тексту
async def state_add_url(message: types.Message, state: FSMContext):
    await message.reply("Какой товар вы хотите добавить?") #что отошлет бот когда переходит в состояния ожидания
    await state.set_state(State.waiting_add_url.state) #сам переход в состояние ожидания

#ТРОГАТЬ добавление именно в txt файл url
@dp.message_handler(state=State.waiting_add_url) #запуск функции из-за состояния НЕ ТРОГАТЬ
async def add_product(message: types.Message, state: FSMContext): #НЕ ТРОГАТЬ
    await state.update_data(new_url=message.text, encodig ="utf-8")# сбор текста из сообщения НЕ ТРОГАТЬ
    #ВОТ ЭТО НАДО ТРОГАТЬ
    #запись в файл
    new_url=message.text+"\n"
    with open("URl.txt", "a+", encoding="utf-8") as url_file:
        url_file.write(f"{new_url}")
    await message.answer("Товар добавлен") #сообщение об успешной записи куда-то
    await state.finish() #завершения состояния НЕ ТРОГАТЬ


@dp.message_handler(lambda message: message.text == "Удалить товар")
async def state_add_url(message: types.Message, state: FSMContext):
    await message.reply("Какой товар вы хотите перестать отслеживать?")
    await state.set_state(State.waiting_delete_url.state)


@dp.message_handler(state=State.waiting_delete_url)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(deleted_url=message.text, encoding ="utf-8")

   #типа удаление
    #
    #
    #
    await message.answer("Товар удален")
    await state.finish()



@dp.message_handler(lambda message: message.text == "Посмотреть товары")
async def watch_all_product(message: types.Message):
    ##Типа сбор инфы из бд
    await message.answer("Типа вывод ссылок")
def run_bot():
    executor.start_polling(dp)



