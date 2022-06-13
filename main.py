import sqlite3
import telebot


def database(country, price):
    pass


def print_information():
    pass


def show_prices(message):
    global saver
    saver = []
    saver.append(message.text.capitalize())
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('от 1000 до 3000')
    button2 = telebot.types.KeyboardButton('от 3000 до 5000')
    button3 = telebot.types.KeyboardButton('от 5000 до 10000')
    button4 = telebot.types.KeyboardButton('Попробовать другой вариант')
    markup.add(button1, button2, button3, button4)

    new_msg = bot.send_message(message.chat.id, 'Выберите диапазон', reply_markup=markup)
    bot.register_next_step_handler(new_msg, take_price)


def take_price(message):
    saver.append(int(message.text.split()[1]))
    saver.append(int(message.text.split()[3]))
    connection = sqlite3.connect('countries.db')
    cursor = connection.cursor()
    try:
        data = cursor.execute('SELECT * FROM `{}` WHERE price BETWEEN ? AND ?'.format(saver[0]), (saver[1], saver[2]-1,)).fetchall()

        for i in data:
            bot.send_message(message.chat.id, 'Название отеля: ' + str(i[1]) + ' Цена: ' + str(i[0]))
            try:
                bot.send_photo(message.chat.id, photo=open('{}.jpg'.format(i[1]), 'rb'))
            except:
                pass
        bot.send_message(message.chat.id, 'Чтобы выбрать другой Диапазон или страну нажмите Попробовать другой вариант')
    except:
        bot.send_message(message.chat.id, 'Вы ввели неправильные данные, нажмите "Попробовать другой вариант"')


bot = telebot.TeleBot('5458246662:AAFLHA5z3zesGAp3gO1maPGqarby8xvnKkc')


@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, 'Здравствуйте, введите одну из стран и далее диапазон цены \n Вы можете попробовать страны: Турция, Египет и ОАЭ')
    msg = bot.send_message(message.chat.id, 'Введите страну чтобы получить отели')
    bot.register_next_step_handler(msg, show_prices)


@bot.message_handler()
def message_hotel(message):
    if message.text == 'Попробовать другой вариант':
        new_start(message)


def new_start(message):
    msg = bot.send_message(message.chat.id, 'Введите страну чтобы получить отели')
    bot.register_next_step_handler(msg, show_prices)


bot.infinity_polling()
