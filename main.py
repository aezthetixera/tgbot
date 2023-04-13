import os
import pyowm

import requests
import envate
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler

secret_token = envate.TOKEN
chat_id = envate.CHAT_ID


URL = 'https://api.thecatapi.com/v1/images/search'


updater = Updater(token=secret_token)
bot = Bot(token=secret_token)


# cat
def get_new_image(URL):
    response = requests.get(URL).json()
    print(response[0]['url'])
    return response[0]['url']


# dog
URL1 = 'https://dog.ceo/api/breeds/image/random'
def get_new_image_dog(URL1):
    response = requests.get(URL1).json()
    print(response['message'])
    return response['message']


def get_weather(message, update, context):
    city = message.text
    chat = update.effective_chat
    name = chat.first_name
    from pyowm import owm
    from pyowm.utils.config import get_default_config

    while True:
        try:
            city = message.text
            config_dict = get_default_config()
            config_dict['connection']['use_ssl'] = False
            config_dict['connection']["verify_ssl_certs"] = False

            owm = pyowm.OWM('8464e9be40f0d0257e7d232120eef878', config_dict)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            w = observation.weather
            break
        except Exception:
            print("Такого города не существует, попробуйте еще раз.")

    temperature = w.temperature('celsius')['temp']

    context.bot.send_message("В городе >>" + city + " сейчас температура >> "  + str(
        temperature) + "°" + " (цельсий).")
    if w.detailed_status == 'clear sky':
        context.bot.send_message( 'Погода в указаном городе >> ' + 'Ясно.')
    elif w.detailed_status == 'light rain':
        context.bot.send_message( 'Погода в указаном городе >> ' + 'Легкий доджь.')
    elif w.detailed_status == 'overcast clouds':
        context.bot.send_message('Погода в указаном городе >> ' + 'Пасмурно.')
    elif w.detailed_status == 'moderate rain':
        context.bot.send_message('Погода в указаном городе >> ' + 'Умеренный дождь.')
    elif w.detailed_status == 'heavy intensity rain':
        context.bot.send_message('Погода в указаном городе >> ' + 'Ливень.')
    elif w.detailed_status == 'broken clouds':
        context.bot.send_message('Погода в указаном городе >> ' + 'Облачно с прояснениями.')
    elif w.detailed_status == 'light snow':
        context.bot.send_message('Погода в указаном городе >> '  + 'Небольшой снег.')
    elif w.detailed_status == 'rain and snow':
        context.bot.send_message('Погода в указаном городе >> ' +  'Дождь со снегом.')
    elif w.detailed_status == 'scattered clouds':
        context.bot.send_message('Погода в указаном городе >> ' + 'Незначительная облачность.')
    elif w.detailed_status == 'sunny':
        context.bot.send_message('Погода в указаном городе >> '  + 'Солнечно.')

    context.bot.send_message('Скорость ветра(м/с) в указаном городе >> '+ str(w.wind().get("speed", 0)), "м/с")
    print('')

@bot.message_handler(content_types=['text'])
def getweather1(message, update, context):
    chat = update.effective_chat
    msg = context.bot.send_message(chat.id, "В каком городе вы хотите узнать погоду?")
    get_weather(message)

def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    buttons = ReplyKeyboardMarkup([
        ['/newcat', '/newdog'],
        ['/cat_and_dog', "/weather"]
    ], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Спасибо, что запустили меня, {name}, могу предложить котиков и собачек, для этого нажмите на кнопку /newcat, /newdog. """,
                             reply_markup=buttons
    )
    bot.send_photo(chat.id, get_new_image(URL))


def give_new_cat(update, context):
    while True:
        try:

            chat = update.effective_chat
            context.bot.send_photo(chat.id, get_new_image(URL))
            break
        except Exception:
            print('url cat err.')

def give_new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image_dog(URL1))


def say_hi(update, context):
    chat = update.effective_chat
    name = chat.first_name

    bot.send_photo(chat.id, get_new_image(URL))
    bot.send_photo(chat.id, get_new_image_dog(URL1))


def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', give_new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', give_new_dog))
    updater.dispatcher.add_handler(CommandHandler('cat_and_dog', say_hi))
    updater.dispatcher.add_handler(CommandHandler("weather", getweather1))
    updater.start_polling()


main()