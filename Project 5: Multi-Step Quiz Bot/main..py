# Import the necessary libraries.
import telebot
import sqlite3
import os
from telebot import types

# --- Configuration ---
# Get your unique bot token from BotFather on Telegram.
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Create a new bot instance.
bot = telebot.TeleBot(BOT_TOKEN)

# A simple dictionary to manage the state of the quiz for each user.
# The keys are chat IDs, and the values are dictionaries with 'state' and 'score'.
user_quiz_data = {}

# The list of quiz questions, answers, and the correct options.
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Jupiter", "Venus", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is 7 times 8?",
        "options": ["49", "56", "64", "72"],
        "answer": "56"
    },
    {
        "question": "In which year did the Titanic sink?",
        "options": ["1910", "1912", "1914", "1916"],
        "answer": "1912"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    }
]

# --- Database Setup ---

def get_db_path():
    # Always create the DB in the same directory as this script
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz_scores.db')

def setup_database():
    """Establishes a connection to the SQLite database and creates the 'highscores' table."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            chat_id INTEGER PRIMARY KEY,
            highscore INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# --- Command Handlers ---

@bot.message_handler(commands=['start'])
def start_quiz(message):
    """Handles the /start command and begins the quiz."""
    chat_id = message.chat.id
    
    # Initialize the user's quiz state.
    user_quiz_data[chat_id] = {'state': 0, 'score': 0}
    
    # Send the first question.
    send_question(chat_id)

@bot.message_handler(commands=['highscore'])
def show_highscore(message):
    """Retrieves and displays the user's highest score."""
    chat_id = message.chat.id
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT highscore FROM highscores WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        highscore = result[0]
        bot.reply_to(message, f"🏆 Your current high score is: {highscore} out of {len(QUIZ_QUESTIONS)}.")
    else:
        bot.reply_to(message, "You haven't completed a quiz yet! Start one with /start.")

# --- Quiz Logic Functions ---

def send_question(chat_id):
    """Sends the current question to the user."""
    # Get the current question index from the user's state.
    current_question_index = user_quiz_data[chat_id]['state']
    
    # Get the question details from the list.
    question_data = QUIZ_QUESTIONS[current_question_index]
    
    # Create an inline keyboard for the answer options.
    markup = types.InlineKeyboardMarkup(row_width=1)
    for option in question_data['options']:
        # The callback data is the option itself, so we can check it later.
        button = types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)
    
    # Send the question with the inline keyboard.
    bot.send_message(
        chat_id, 
        f"Question {current_question_index + 1}/{len(QUIZ_QUESTIONS)}: {question_data['question']}",
        reply_markup=markup
    )

# --- Callback Query Handler ---

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    """Processes the user's answer from the inline keyboard."""
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    # Acknowledge the button press to remove the "loading" state.
    bot.answer_callback_query(call.id)
    
    # Get the user's current quiz data.
    if chat_id not in user_quiz_data:
        bot.send_message(chat_id, "Please start a new quiz with /start.")
        return
        
    current_state = user_quiz_data[chat_id]
    current_question_index = current_state['state']
    
    # Check if the user's answer is correct.
    correct_answer = QUIZ_QUESTIONS[current_question_index]['answer']
    user_answer = call.data
    
    if user_answer == correct_answer:
        current_state['score'] += 1
        bot.send_message(chat_id, "Correct! ✅")
    else:
        bot.send_message(chat_id, f"Incorrect. The correct answer was: {correct_answer} ❌")
        
    # Increment the question index.
    current_state['state'] += 1
    
    # Check if the quiz is finished.
    if current_state['state'] >= len(QUIZ_QUESTIONS):
        end_quiz(chat_id)
    else:
        # Send the next question.
        send_question(chat_id)
        
    # Remove the inline keyboard from the previous message for a cleaner UI.
    bot.edit_message_reply_markup(
        chat_id=chat_id, 
        message_id=message_id, 
        reply_markup=None
    )

def end_quiz(chat_id):
    """Finalizes the quiz, shows the score, and saves the high score."""
    final_score = user_quiz_data[chat_id]['score']
    total_questions = len(QUIZ_QUESTIONS)
    
    # Inform the user of their final score.
    bot.send_message(
        chat_id,
        f"Quiz finished! 🎉\n\n"
        f"Your final score is: {final_score} out of {total_questions}."
    )
    
    # Save the score to the database.
    save_highscore(chat_id, final_score)
    
    # Reset the user's state.
    del user_quiz_data[chat_id]

# --- Database Interaction Function ---

def save_highscore(chat_id, new_score):
    """Saves a new high score, but only if it's higher than the previous one."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Check for an existing high score.
    cursor.execute("SELECT highscore FROM highscores WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    
    if result:
        current_highscore = result[0]
        # Only update if the new score is higher.
        if new_score > current_highscore:
            cursor.execute("UPDATE highscores SET highscore=? WHERE chat_id=?", (new_score, chat_id))
            bot.send_message(chat_id, "You've set a new high score! �")
        else:
            bot.send_message(chat_id, "You didn't beat your high score. Try again!")
    else:
        # Insert a new record if one doesn't exist.
        cursor.execute("INSERT INTO highscores (chat_id, highscore) VALUES (?, ?)", (chat_id, new_score))
        bot.send_message(chat_id, "This is your first score, now saved as your high score!")
    
    conn.commit()
    conn.close()

# --- Main Bot Loop ---

if __name__ == '__main__':
    # Set up the database before the bot starts polling.
    setup_database()
    print("Bot is running...")
    # Start the bot and let it listen for messages.
    bot.polling()
    