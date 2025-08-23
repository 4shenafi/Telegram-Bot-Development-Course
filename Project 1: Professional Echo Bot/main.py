# Import the telebot library. Install with: pip install pyTelegramBotAPI
import telebot

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am a simple echo bot. Send me a message and I'll send it right back!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "I'm a very basic bot. I just echo back any message you send me.")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

print("Bot is running...")
bot.polling()
