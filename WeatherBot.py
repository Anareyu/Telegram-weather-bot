import telebot
from telebot import types
import requests
import json

TOKEN = '6407237705:AAGqYRxlRR1zSf5oDSBENlNL2pgFiqXCzUs'
bot = telebot.TeleBot(TOKEN)

API = '3facb167b165a1a5c30ffdc4acec9858'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Екатеринбург')
    #btn2 = types.KeyboardButton('Санкт-Петербург')
    markup.row(btn1)
    bot.send_message(message.chat.id, "Привет! Я - WeatherBot. Напиши название своего города", reply_markup=markup)




@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)


        bot.send_message(message.chat.id, f'<b>Город</b>: {data["name"]} {data["coord"]["lon"], data["coord"]["lat"]}\n'
                                          f'<b>{data["weather"][0]["main"]}</b>: {data["weather"][0]["description"]}\n'
                                          f'<b>Температура</b>: {round(data["main"]["temp"], 1)}°C\n'
                                          f'<b>Ощущается как</b> {round(data["main"]["feels_like"], 1)}°C\n'
                                          f'<b>Ветер</b>: {round(data["wind"]["speed"], 1)}м/с\n'
                                          f'<b>Влажность</b>: {data["main"]["humidity"]}%\n'
                                          f'<b>Облачность</b>: {data["clouds"]["all"]}%',
                         parse_mode='html')
    elif message.text.strip() == 'translate':
        data = json.loads(res.text)
        WeatherMain = requests.get(f'http://translate.google.ru/translate_a/t?client=x&text={data["name"]}&hl=en&sl=en&tl=ru')
        bot.send_message(message.chat.id, WeatherMain)
    else:
        bot.reply_to(message, 'Название города указано неверно!')



bot.infinity_polling()