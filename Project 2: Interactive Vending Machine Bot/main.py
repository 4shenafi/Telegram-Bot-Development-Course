import telebot
from telebot import types
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    item_soda = types.KeyboardButton('Soda')
    item_chips = types.KeyboardButton('Chips')
    item_candy = types.KeyboardButton('Candy')
    markup.add(item_soda, item_chips, item_candy)
    bot.send_message(
        message.chat.id,
        "Welcome to the Vending Machine! Please select an item:",
        reply_markup=markup
    )

@bot.message_handler(commands=['mystery'])
def mystery_item(message):
    bot.reply_to(message, "You've discovered the hidden Mystery Box! ✨")

@bot.message_handler(func=lambda message: message.text in ["Soda", "Chips", "Candy"])
def vend_item(message):
    if message.text == "Soda":
        bot.reply_to(message, "Here's your refreshing Soda! 🥤")
    elif message.text == "Chips":
        bot.reply_to(message, "Crunch, crunch! Here are your tasty Chips! 🥔")
    elif message.text == "Candy":
        bot.reply_to(message, "Sweet tooth satisfied! Here is your delicious Candy! 🍬")

print("Bot is running...")
bot.polling()
