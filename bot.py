import telebot
from telebot import types
import os

from data import fish_info, diseases, compatibility

TOKEN = os.getenv("8929864561:AAEaMp8L8LnExiYT-m9WZj-Svjt2I1jtWvg")
BOT = telebot.TeleBot(8929864561:AAEaMp8L8LnExiYT-m9WZj-Svjt2I1jtWvg)

CHANNEL_USERNAME = "@fishparadiseiran"

user_mode = {}

fish_suggestions = {
    "small": "فایتر 🐟\nگوپی 🐟\nمولی 🐟\nپلاتی 🐟\nتترا 🐟",
    "medium": "آنجل 🐠\nگورامی 🐠\nسورم 🐠\nپرت 🐠",
    "large": "اسکار 🐡\nسورم بالغ 🐡\nپرت بزرگ 🐡",
    "giant": "آروانا 🐉\nردتیل 🐟"
}

def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):

    if not is_member(message.from_user.id):

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/fishparadiseiran"))
        markup.add(types.InlineKeyboardButton("✅ عضو شدم", callback_data="check_join"))

        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات ابتدا در کانال عضو شوید.", reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🐟 اطلاعات ماهی‌ها")
    markup.add("🦠 بیماری‌های رایج")
    markup.add("🤝 سازگاری ماهی‌ها")
    markup.add("📏 محاسبه حجم آکواریوم")
    markup.add("🧂 محاسبه نمک")
    markup.add("💧 محاسبه سیفون")
    markup.add("🐟 پیشنهاد ماهی")

    bot.send_message(message.chat.id, "سلام به دستیار پارادیس فیش 🐠", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):

    if is_member(call.from_user.id):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🐟 اطلاعات ماهی‌ها")
        markup.add("🦠 بیماری‌های رایج")
        markup.add("🤝 سازگاری ماهی‌ها")
        markup.add("📏 محاسبه حجم آکواریوم")
        markup.add("🧂 محاسبه نمک")
        markup.add("💧 محاسبه سیفون")
        markup.add("🐟 پیشنهاد ماهی")

        bot.send_message(call.message.chat.id, "✅ عضویت تایید شد.", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "هنوز عضو کانال نیستی 😅")


@bot.message_handler(func=lambda m: True)
def messages(message):

    text = message.text
    chat_id = message.chat.id

    if text == "🐟 اطلاعات ماهی‌ها":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("فایتر", "اسکار")
        markup.add("چانا", "آروانا")
        markup.add("🔙 بازگشت")
        bot.send_message(chat_id, "یک ماهی انتخاب کن:", reply_markup=markup)

    elif text in fish_info:
        bot.send_message(chat_id, fish_info[text])

    elif text == "🦠 بیماری‌های رایج":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("سفیدک", "سوراخی سر")
        markup.add("پوسیدگی باله")
        markup.add("🔙 بازگشت")
        bot.send_message(chat_id, "بیماری مورد نظر:", reply_markup=markup)

    elif text in diseases:
        bot.send_message(chat_id, diseases[text])

    elif text == "🤝 سازگاری ماهی‌ها":
        result = ""
        for fishes, answer in compatibility.items():
            result += f"{fishes[0]} + {fishes[1]}\n{answer}\n\n"
        bot.send_message(chat_id, result)

    elif text == "📏 محاسبه حجم آکواریوم":
        user_mode[chat_id] = "volume"
        bot.send_message(chat_id, "طول عرض ارتفاع را وارد کن:")

    elif len(text.split()) == 3 and user_mode.get(chat_id) == "volume":
        try:
            l, w, h = map(float, text.split())
            v = (l*w*h)/1000
            bot.send_message(chat_id, f"📏 حجم: {int(v)} لیتر\n💧 مفید: {int(v*0.85)}")
            user_mode.pop(chat_id, None)
        except:
            bot.send_message(chat_id, "فرمت اشتباه")

    elif text == "🧂 محاسبه نمک":
        user_mode[chat_id] = "salt"
        bot.send_message(chat_id, "حجم را وارد کن:")

    elif text == "💧 محاسبه سیفون":
        user_mode[chat_id] = "siphon"
        bot.send_message(chat_id, "حجم را وارد کن:")

    elif text.isdigit():
        volume = int(text)
        mode = user_mode.get(chat_id)

        if mode == "salt":
            bot.send_message(chat_id, f"🧂 سبک {volume}g\nمتوسط {volume*2}g\nقوی {volume*3}g")
            user_mode.pop(chat_id, None)

        elif mode == "siphon":
            bot.send_message(chat_id, f"💧20% {int(volume*0.2)}\n30% {int(volume*0.3)}\n50% {int(volume*0.5)}")
            user_mode.pop(chat_id, None)

        elif mode == "fish":
            if volume <= 100:
                r = fish_suggestions["small"]
            elif volume <= 300:
                r = fish_suggestions["medium"]
            elif volume <= 500:
                r = fish_suggestions["large"]
            else:
                r = fish_suggestions["giant"]
            bot.send_message(chat_id, r)
            user_mode.pop(chat_id, None)

    elif text == "🐟 پیشنهاد ماهی":
        user_mode[chat_id] = "fish"
        bot.send_message(chat_id, "حجم آکواریوم را وارد کن:")

    elif text == "🔙 بازگشت":
        user_mode.pop(chat_id, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🐟 اطلاعات ماهی‌ها")
        markup.add("🦠 بیماری‌های رایج")
        markup.add("🤝 سازگاری ماهی‌ها")
        markup.add("📏 محاسبه حجم آکواریوم")
        markup.add("🧂 محاسبه نمک")
        markup.add("💧 محاسبه سیفون")
        markup.add("🐟 پیشنهاد ماهی")
        bot.send_message(chat_id, "منوی اصلی:", reply_markup=markup)


bot.infinity_polling()
