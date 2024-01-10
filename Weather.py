import telebot
from telebot import types
import requests
from config import API_KEY, BOT_TOKEN
import json

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):

    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Start"))
    bot.send_message(message.chat.id, f"Good day my friend {message.from_user.first_name} my name is Weatherbot.\n"
                                      f"I'm there to help you =)\n"
                                      f"Press the button start and know the weather\n",
                     reply_markup=markup)
    bot.register_next_step_handler(message, weather)


def filter_weather(data):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={data}&appid={API_KEY}&units=metric")
    seas = res.json()["weather"][0]["main"]
    degree = res.json()["main"]["temp"]
    list_of_both = [degree, seas]
    return list_of_both


def weather(message):
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton("Tashkent", callback_data="Tashkent")
    but2 = types.InlineKeyboardButton("New-York", callback_data="New york")
    markup.row(but1, but2)
    but3 = types.InlineKeyboardButton("Canada", callback_data="Canada")
    but4 = types.InlineKeyboardButton("Other", callback_data="Other")
    markup.row(but3, but4)
    bot.reply_to(message, "Here you can choose witch city", reply_markup=markup)


@bot.callback_query_handler(func=lambda cal: True)
def callback(call):

    seasons = {
        "Clouds": "cloud.jpeg",
        "Rain": "rainy.jpeg",
        "Smoke": "smoke.png",
        "Snow": "snow.jpeg"
    }
    print(call.data)
    if call.data == "Other":
            bot.send_message(call.message.chat.id, "Here you can write your city: ")
            bot.register_next_step_handler(call.message, handle_other_city_input)
    else:
        degree = filter_weather(call.data)[0]
        season = filter_weather(call.data)[1]
        if season in seasons:
            with open(seasons[season], "rb") as file:
                bot.send_photo(call.message.chat.id, file)

        bot.reply_to(call.message, f"Weather in {call.data}: {degree}, {season}")

    # match call.data:
    #     case "Tashkent":
    #         bot.reply_to(call.message, f"Weather in Tashkent: {degree}, {season}")
    #
    #     case "New york":
    #         bot.reply_to(call.message, f"Weather in New york: {degree}, {season}")
    #
    #     case "Canada":
    #         bot.reply_to(call.message, f"Weather in Canada: {degree}, {season}")
    #         # bot.register_next_step_handler(call.message, weather)
    #
    #     case "Other":
    #         bot.send_message(call.message.chat.id, "Here you can write your own city: ")
    #         bot.register_next_step_handler(call.message, handle_other_city_input)


def handle_other_city_input(message):
    user_input = message.text
    chat_id = message.chat.id

    degree = filter_weather(user_input)[0]
    season = filter_weather(user_input)[1]
    seasons = {
        "Clouds": "cloud.jpeg",
        "Rain": "rainy.jpeg",
        "Smoke": "smoke.png",
        "Snow": "snow.jpeg"
    }
    try:
        if season in seasons:
            with open(seasons[season], "rb") as file:
                bot.send_photo(message.chat.id, file)
        bot.reply_to(message, f"Weather in {user_input}: {degree}, {season}")
    except Exception:
        bot.send_message(chat_id, "Try one more time")
        bot.register_next_step_handler(message, handle_other_city_input)


bot.polling(none_stop=True)

