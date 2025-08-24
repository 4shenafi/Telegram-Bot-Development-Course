

# Simple User Profile Bot with SQLite
import telebot
import sqlite3
import re

# Your bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# Create the database and table if not exists
def setup_database():
    conn = sqlite3.connect('user_profiles.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY, name TEXT, phone TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

# /start command: Welcome message
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Use /setprofile to create your profile. Use /help for commands.")


# /help command: List available commands
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Commands:\n"
        "/start - Welcome message\n"
        "/setprofile - Create your profile\n"
        "/updateprofile - Update your profile\n"
        "/seeprofile - View your profile\n"
        "/help - Show this help message"
    )
    bot.reply_to(message, help_text)

# /updateprofile command: Update profile (all fields)
@bot.message_handler(commands=['updateprofile'])
def update_profile(message):
    bot.reply_to(message, "Let's update your profile. What is your new name?")
    bot.register_next_step_handler(message, get_update_name)

# Update flow: get name, phone, age
def get_update_name(message):
    name = message.text
    bot.reply_to(message, "What is your new phone number?")
    bot.register_next_step_handler(message, get_update_phone, name)

def get_update_phone(message, name):
    phone = message.text
    if not re.match(r'^\+?[0-9\s()\-]{7,20}$', phone):
        bot.reply_to(message, "Invalid phone number. Try again.")
        bot.register_next_step_handler(message, get_update_phone, name)
        return
    bot.reply_to(message, "What is your new age?")
    bot.register_next_step_handler(message, get_update_age, name, phone)

def get_update_age(message, name, phone):
    try:
        age = int(message.text)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number for your age.")
        bot.register_next_step_handler(message, get_update_age, name, phone)
        return
    chat_id = message.chat.id
    conn = sqlite3.connect('user_profiles.db')
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO users (chat_id, name, phone, age) VALUES (?, ?, ?, ?)", (chat_id, name, phone, age))
    conn.commit()
    conn.close()
    bot.reply_to(message, "Profile updated! Use /seeprofile to view it.")

# /seeprofile command: Show saved profile
@bot.message_handler(commands=['seeprofile'])
def see_profile(message):
    chat_id = message.chat.id
    conn = sqlite3.connect('user_profiles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, age FROM users WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        name, phone, age = result
        bot.reply_to(message, f"Your profile:\nName: {name}\nPhone: {phone}\nAge: {age}")
    else:
        bot.reply_to(message, "No profile found. Use /setprofile to create one.")

# /setprofile command: Start profile creation
@bot.message_handler(commands=['setprofile'])
def set_profile(message):
    bot.reply_to(message, "What is your name?")
    bot.register_next_step_handler(message, get_name)

# Step 1: Get name
def get_name(message):
    name = message.text
    bot.reply_to(message, "What is your phone number?")
    bot.register_next_step_handler(message, get_phone, name)

# Step 2: Get phone number
def get_phone(message, name):
    phone = message.text
    # Simple phone validation: allows digits, spaces, (), -
    if not re.match(r'^\+?[0-9\s()\-]{7,20}$', phone):
        bot.reply_to(message, "Invalid phone number. Try again.")
        bot.register_next_step_handler(message, get_phone, name)
        return
    bot.reply_to(message, "What is your age?")
    bot.register_next_step_handler(message, get_age, name, phone)

# Step 3: Get age
def get_age(message, name, phone):
    try:
        age = int(message.text)
    except ValueError:
        bot.reply_to(message, "Please enter a valid number for your age.")
        bot.register_next_step_handler(message, get_age, name, phone)
        return
    chat_id = message.chat.id
    # Save profile to database
    conn = sqlite3.connect('user_profiles.db')
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO users (chat_id, name, phone, age) VALUES (?, ?, ?, ?)", (chat_id, name, phone, age))
    conn.commit()
    conn.close()
    bot.reply_to(message, "Profile saved! Use /seeprofile to view it.")

# Main loop: setup database and start bot
if __name__ == '__main__':
    setup_database()
    print("Bot is running...")
    bot.polling()
