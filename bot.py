import telebot
from telebot import types
print("شروع برنامه")
from config import TOKEN
from data import fish_info, diseases

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🐟 اطلاعات ماهی‌ها")
    markup.add("🦠 بیماری‌های رایج")

    bot.send_message(
        message.chat.id,
        "سلام، به دستیار پارادیس فیش خوش اومدی 🐠",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def messages(message):

    text = message.text

    if text == "🐟 اطلاعات ماهی‌ها":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add("فایتر", "اسکار")
        markup.add("چانا", "آروانا")
        markup.add("🔙 بازگشت")

        bot.send_message(
            message.chat.id,
            "یک ماهی انتخاب کن:",
            reply_markup=markup
        )

    elif text in fish_info:

        bot.send_message(
            message.chat.id,
            fish_info[text]
        )

    elif text == "🦠 بیماری‌های رایج":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add("سفیدک", "سوراخی سر")
        markup.add("پوسیدگی باله")
        markup.add("🔙 بازگشت")

        bot.send_message(
            message.chat.id,
            "بیماری مورد نظر را انتخاب کن:",
            reply_markup=markup
        )

    elif text in diseases:

        bot.send_message(
            message.chat.id,
            diseases[text]
        )

    elif text == "🔙 بازگشت":

        start(message)

print("Bot Started")

bot.infinity_polling()