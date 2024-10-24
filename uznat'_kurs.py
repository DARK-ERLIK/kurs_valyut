import telebot

from telebot import types

bot = telebot.TeleBot("7653258903:AAHo5KYRAS9GjZ87D2h4lOuDVdN1R5xD37I")

# Примерные курсы валют
USD_RATE = 12850  # 1 доллар в сумах
EUR_RATE = 13870  # 1 евро в сумах
RUB_RATE = 140    # 1 рубль в сумах

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    # Приветствие
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в бот по конвертации валют!")
    # Создание кнопки для начала конвертации
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Конвертировать сумму")
    markup.add(start_button)
    bot.send_message(user_id, "Нажмите кнопку для начала конвертации:", reply_markup=markup)

# Обработка нажатий на кнопки
@bot.message_handler(content_types=['text'])
def handle_conversion(message):
    if message.text == "Конвертировать сумму":
        # Запрашиваем сумму для конвертации
        bot.send_message(message.from_user.id, "Введите сумму в сумах, которую хотите конвертировать:")
        bot.register_next_step_handler(message, validate_input)

def validate_input(message):
    # Проверяем, является ли введенный текст числом
    if message.text.isdigit():
        amount_in_sums = float(message.text)
        convert_currency(message, amount_in_sums)
    else:
        bot.send_message(message.from_user.id, "Ошибка! Введите корректное число.")
        bot.register_next_step_handler(message, validate_input)

def convert_currency(message, amount_in_sums):
    # Конвертация валют
    amount_in_usd = round(amount_in_sums / USD_RATE, 2)
    amount_in_eur = round(amount_in_sums / EUR_RATE, 2)
    amount_in_rub = round(amount_in_sums / RUB_RATE, 2)

    # Формируем ответное сообщение
    response = (f"Сумма в сумах: {amount_in_sums} UZB\n"
                f"В долларах: {amount_in_usd} $\n"
                f"В евро: {amount_in_eur} €\n"
                f"В рублях: {amount_in_rub} ₽")

    bot.send_message(message.from_user.id, response)

# Запускаем бота
bot.infinity_polling()