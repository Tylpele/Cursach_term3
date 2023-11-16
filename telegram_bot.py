import asyncio
from main_parser import *
from db_actions import *
from html_info import *
from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN_API = "5634121116:AAEE-utFMkGewUNOOKPAKv-ai89ogJL8a3c"
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()


# состояния
class State(StatesGroup):
    waiting_add_url = State()
    waiting_delete_url = State()
    waiting_min_price = State()


# команда /start
@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)  # cоздание кнопки
    btn_add = types.KeyboardButton("Добавить товар")  # текст кнопки
    btn_delete = types.KeyboardButton("Удалить товар")
    btn_watch_product = types.KeyboardButton("Посмотреть товары")
    keyboard.add(btn_add)  # добавление кнопки на клавиатуру
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
                                            "Ссылки типа bit.ly, goo.gl и другие сокращенные ссылки считываться <b>не</b> будут.",
                           parse_mode="HTML", reply_markup=keyboard)


async def send_notifications_periodically():
    while True:
        # список товаров, и людей которым надо отправить уведомление в данный момент
        senders_list = get_notification_senders_list(datetime.now().time())

        for i in range(len(senders_list)):
            user_id = senders_list[i][0]
            product_name = senders_list[i][1]
            link = senders_list[i][2]
            price = get_product_price(link)
            prev_price = senders_list[i][3]
            min_price = senders_list[i][4]

            # обновление прошлого значения цены в БД
            update_product_prev_price(link, price)

            # если цена на 5% выше заданной, уведомление все еще придет
            if price <= min_price + 0.05 * min_price:
                await send_notification(user_id, product_name, link, price, prev_price)

        # проверка каждые 30 минут
        await asyncio.sleep(1800)


async def send_notification(user_id, product_name, link, price: int, prev_price: int):
    if prev_price - price > 0:
        await bot.send_message(user_id,
                               f"Товар \"{product_name}\" теперь стоит <b>{price}₽</b> ({link}) . <i>(пред. цена {prev_price}₽)</i>. "
                               f"Цена снизилась на {prev_price - price}₽.", parse_mode="HTML")
    elif prev_price - price < 0:
        await bot.send_message(user_id,
                               f"Товар \"{product_name}\" теперь стоит <b>{price}₽</b> ({link}) . <i>(пред. цена {prev_price}₽)</i>. "
                               f"Цена повысилась на {price - prev_price}₽.", parse_mode="HTML")
    else:
        await bot.send_message(user_id,
                               f"Товар \"{product_name}\" теперь стоит <b>{price}₽</b> ({link}) . <i>(пред. цена {prev_price}₽)</i>. "
                               f"Цена товара не изменилась", parse_mode="HTML")
    # кнопка "отменить отслеживание"


@dp.message_handler(lambda message: message.text == "Добавить товар")
async def state_add_url(message: types.Message, state: FSMContext):
    await message.reply("Вставьте ссылку на товар: ")
    await state.set_state(State.waiting_add_url.state)


@dp.message_handler(state=State.waiting_add_url.state)
async def add_url(message: types.Message, state: FSMContext):
    url = message.text

    if is_correct_link(url) is False:
        await message.answer("Данного сайта нет в базе или ссылка некорректна")
        await state.finish()
        return

    await state.set_state(State.waiting_min_price.state)
    await state.update_data(url=url)
    await message.answer("Введите цену товара, которая бы Вас устроила:")


@dp.message_handler(state=State.waiting_min_price)
async def get_min_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    url = data.get("url")

    if not message.text.isdigit():
        await message.answer("Некорректный формат числа. Попробуйте еще раз:")
        return

    min_price = int(message.text)

    if min_price < 1:
        await message.answer("Некорректная цена. Попробуйте еще раз:")
        return

    await message.answer("Запрос обрабатывается")

    # привод ссылок к общему виду
    new_url = make_standart_link(url)

    if is_product_added_db(user_id, new_url):
        await message.answer("Товар уже был ранее добавлен")
        await state.finish()
        return

    price = get_product_price(new_url)
    product_name = get_product_name(new_url)

    if price is None or product_name is None:
        await message.answer("Данные с сайта не парсятся. Попробуйте еще раз позже")
        await state.finish()
        return

    add_product_to_db(user_id, new_url, product_name, price, min_price, message.date.time())

    await message.answer("Товар добавлен")
    await state.finish()


@dp.message_handler(lambda message: message.text == "Удалить товар")
async def state_delete_url(message: types.Message, state: FSMContext):
    product_list = get_product_list(message.from_user.id)
    await state.update_data(product_list=product_list)

    if len(product_list) == 0:
        await message.reply("Вы еще не добавили ни одного товара.")
        await state.finish()
        return

    reply = "<b>Какой товар вы хотите перестать отслеживать?</b> (Введите число возле товара, или введите 0 чтобы " \
            "отменить)\n\n"

    for i in range(len(product_list)):
        reply += f"{i + 1}. {product_list[i][0]}: <i>{product_list[i][1]}₽</i> ({product_list[i][2]})\n" \
                 f"- Предпочитаемая цена: {product_list[i][3]}₽\n"

    await message.reply(reply, parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(State.waiting_delete_url.state)


@dp.message_handler(state=State.waiting_delete_url)
async def delete_product(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not message.text.isdigit():
        await message.answer("Некорректный номер. Введите еще раз:")
        return

    product_num = int(message.text)

    data = await state.get_data()
    product_list = data.get("product_list")

    if product_num == 0:
        await message.answer("Отменено.")
        await state.finish()
        return

    if product_num > len(product_list) or product_num < 1:
        await message.answer("Некорректный номер. Введите еще раз:")
        return

    link = product_list[product_num - 1][2]

    delete_product_from_bd(user_id, link)

    await message.answer("Товар удален")
    await state.finish()


@dp.message_handler(lambda message: message.text == "Посмотреть товары")
async def watch_all_product(message: types.Message):
    user_id = message.from_user.id
    product_list = get_product_list(user_id)

    if len(product_list) == 0:
        await message.reply("Вы еще не добавили ни одного товара")
        return

    reply = "<b>Список добавленных товаров:\n\n</b>"

    for i in range(len(product_list)):
        reply += f"{i + 1}. {product_list[i][0]}: <b>{product_list[i][1]}₽</b> ({product_list[i][2]}) " \
                 f"- Предпочитаемая цена: {product_list[i][3]}₽\n"

    await message.reply(reply, parse_mode="HTML", disable_web_page_preview=True)


def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(send_notifications_periodically())

    executor.start_polling(dp)
