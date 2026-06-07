import telebot
from telebot import types
import os

TOKEN = "8929864561:AAEaMp8L8LnExiYT-m9WZj-Svjt2I1jtWvg"
from data import fish_info, diseases, compatibility

print("شروع برنامه")

bot = telebot.TeleBot(TOKEN)

user_mode = {}

fish_suggestions = {
    "small": "✅ فایتر\n✅ گوپی\n✅ مولی\n✅ پلاتی\n✅ تترا",
    "medium": "✅ آنجل\n✅ گورامی\n✅ سورم جوان\n✅ پرت",
    "large": "✅ اسکار\n✅ سورم\n✅ پرت بالغ",
    "giant": "✅ آروانا\n✅ ردتیل\n✅ اسکار بالغ"
}


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🐟 اطلاعات ماهی‌ها")
    markup.add("🦠 بیماری‌های رایج")
    markup.add("🤝 سازگاری ماهی‌ها")
    markup.add("📏 محاسبه حجم آکواریوم")
    markup.add("🧂 محاسبه نمک")
    markup.add("💧 محاسبه سیفون")
    markup.add("🐟 پیشنهاد ماهی")

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

        bot.send_message(message.chat.id, fish_info[text])

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

        bot.send_message(message.chat.id, diseases[text])

    elif text == "🤝 سازگاری ماهی‌ها":

        result = ""

        for fishes, answer in compatibility.items():
            result += f"{fishes[0]} + {fishes[1]}\n{answer}\n\n"

        bot.send_message(message.chat.id, result)

    elif text == "🐟 پیشنهاد ماهی":

        user_mode[message.chat.id] = "fish"

        bot.send_message(
            message.chat.id,
            "حجم آکواریوم را به لیتر وارد کن:"
        )

    elif text == "📏 محاسبه حجم آکواریوم":

        bot.send_message(
            message.chat.id,
            "ابعاد آکواریوم را وارد کن:\n\nطول عرض ارتفاع\n\nمثال:\n120 50 60"
        )

    elif text == "🧂 محاسبه نمک":

        user_mode[message.chat.id] = "salt"

        bot.send_message(
            message.chat.id,
            "حجم آکواریوم را به لیتر وارد کن:"
        )

    elif text == "💧 محاسبه سیفون":

        user_mode[message.chat.id] = "siphon"

        bot.send_message(
            message.chat.id,
            "حجم آکواریوم را به لیتر وارد کن:"
        )

    elif len(text.split()) == 3:

        try:

            length, width, height = map(float, text.split())

            volume = (length * width * height) / 1000
            useful_volume = int(volume * 0.85)
            heater = int(volume)
            filter_rate = int(volume * 5)

            bot.send_message(
                message.chat.id,
                f"📏 حجم خام: {int(volume)} لیتر\n\n"
                f"💧 حجم مفید: {useful_volume} لیتر\n\n"
                f"🔥 بخاری پیشنهادی: {heater} وات\n\n"
                f"🌊 فیلتر پیشنهادی: {filter_rate} لیتر بر ساعت"
            )

        except:
            pass

    elif text.isdigit():

        volume = int(text)
        mode = user_mode.get(message.chat.id)

        if mode == "fish":

            if volume <= 100:
                result = fish_suggestions["small"]
            elif volume <= 300:
                result = fish_suggestions["medium"]
            elif volume <= 500:
                result = fish_suggestions["large"]
            else:
                result = fish_suggestions["giant"]

            bot.send_message(
                message.chat.id,
                f"🐟 ماهی‌های پیشنهادی برای {volume} لیتر:\n\n{result}"
            )

        elif mode == "salt":

            bot.send_message(
                message.chat.id,
                f"🧂 نمک درمانی سبک: {volume} گرم\n\n"
                f"🧂 نمک درمانی متوسط: {volume * 2} گرم\n\n"
                f"🧂 نمک درمانی قوی: {volume * 3} گرم"
            )

        elif mode == "siphon":

            bot.send_message(
                message.chat.id,
                f"💧 سیفون 20٪: {int(volume * 0.2)} لیتر\n\n"
                f"💧 سیفون 30٪: {int(volume * 0.3)} لیتر\n\n"
                f"💧 سیفون 50٪: {int(volume * 0.5)} لیتر"
            )

    elif text == "🔙 بازگشت":

        user_mode.pop(message.chat.id, None)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        markup.add("🐟 اطلاعات ماهی‌ها")
        markup.add("🦠 بیماری‌های رایج")
        markup.add("🤝 سازگاری ماهی‌ها")
        markup.add("📏 محاسبه حجم آکواریوم")
        markup.add("🧂 محاسبه نمک")
        markup.add("💧 محاسبه سیفون")
        markup.add("🐟 پیشنهاد ماهی")

        bot.send_message(
            message.chat.id,
            "منوی اصلی:",
            reply_markup=markup
        )


print("Bot Started")

bot.infinity_polling()
