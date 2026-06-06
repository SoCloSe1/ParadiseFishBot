import telebot
from data import fish_info, diseases
print("شروع برنامه")
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام، به دستیار پارادیس فیش خوش اومدی 🐟")

print("Bot Started")

bot.infinity_polling()