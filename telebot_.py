from telebot import TeleBot, types
from parse_rate import parser
from dotenv import load_dotenv
import os

load_dotenv()

bot = TeleBot(token=os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start_bot(message):
    # создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_usd = types.KeyboardButton("USD")
    btn_eur = types.KeyboardButton("EUR")
    btn_rub = types.KeyboardButton("RUB")

    keyboard.add(btn_usd, btn_eur, btn_rub)

    bot.send_message(
        message.chat.id,
        "Выберите валюту:",
        reply_markup=keyboard
    )


@bot.message_handler()
def typing(message):
    with open('info.log', 'a') as file:
        file.write(f'{message.chat.first_name} -> {message.text}\n')
    currency = message.text.upper()

    if currency in ["USD", "EUR", "RUB"]:
        data = parser(currency)
        bot.send_message(message.chat.id, f"{currency}: {data}")
    else:
        bot.send_message(message.chat.id, "Выберите валюту кнопками.")


bot.polling()