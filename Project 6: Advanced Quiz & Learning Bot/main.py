# Import necessary libraries
import telebot
import sqlite3
import random
import logging
import os
from telebot import types

# --- Configuration ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Create a new bot instance.
bot = telebot.TeleBot(BOT_TOKEN)

# A simple dictionary to manage the state of the quiz for each user.
user_quiz_data = {}


# --- Database Setup and Management ---
# Create the SQLite database and tables in the current directory
def setup_database():
    conn = sqlite3.connect('./quiz_bot.db')
    cursor = conn.cursor()
    # Create highscores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            chat_id INTEGER PRIMARY KEY,
            highscore INTEGER
        )
    ''')
    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    # Insert sample questions if table is empty
    initial_questions = [
        # ...existing code...
        ('Math', 'What is the area of a circle with radius \'r\'?', '$\pi r^2$', '$2\pi r$', '$\pi d$', '$2\pi d$', '$\pi r^2$'),
        ('Math', 'What is the value of 5!?', '25', '120', '100', '50', '120'),
        ('Math', 'A triangle with two equal sides is called a(n) ________ triangle.', 'equilateral', 'isosceles', 'scalene', 'right', 'isosceles'),
        ('Math', 'What is the slope-intercept form of a linear equation?', '$y = mx + b$', '$ax + by = c$', '$x = my + b$', '$y = ax^2 + bx + c$', '$y = mx + b$'),
        ('Math', 'What is the next prime number after 7?', '8', '9', '10', '11', '11'),
        ('English', 'What is a group of crows called?', 'A flock', 'A murder', 'A coven', 'A swarm', 'A murder'),
        ('English', 'Which of these is a synonym for \'benevolent\'?', 'cruel', 'kind', 'greedy', 'angry', 'kind'),
        ('English', 'What is the past tense of \'sing\'?', 'singed', 'sang', 'sung', 'sanged', 'sang'),
        ('English', 'The opposite of \'antonym\' is a(n) ________.', 'homonym', 'synonym', 'acronym', 'palindrome', 'synonym'),
        ('English', 'A sentence with both an independent and a dependent clause is called a(n) ________ sentence.', 'simple', 'compound', 'complex', 'compound-complex', 'complex'),
        ('Physics', 'What is the SI unit of force?', 'Watt', 'Joule', 'Newton', 'Pascal', 'Newton'),
        ('Physics', 'The law of conservation of energy states that energy cannot be created or ________.', 'accelerated', 'destroyed', 'converted', 'generated', 'destroyed'),
        ('Physics', 'What is the formula for calculating force?', '$F = ma$', '$E = mc^2$', '$P = V I$', '$V = IR$', '$F = ma$'),
        ('Physics', 'What is the speed of light in a vacuum?', '$3.0 \times 10^5 \text{ m/s}$', '$3.0 \times 10^8 \text{ km/s}$', '$3.0 \times 10^8 \text{ m/s}$', '$3.0 \times 10^{10} \text{ m/s}$', '$3.0 \times 10^8 \text{ m/s}$'),
        ('Physics', 'The property of matter that resists changes in motion is called ________.', 'density', 'weight', 'mass', 'inertia', 'inertia'),
    ]
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO questions (category, question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?, ?)", initial_questions)
        conn.commit()
    conn.close()

def get_questions_by_category(category):
    """Retrieves questions from the database for a given category."""
    conn = sqlite3.connect('./quiz_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question, option1, option2, option3, option4, answer FROM questions WHERE category=?", (category,))
    questions = cursor.fetchall()
    conn.close()
    # Convert to list of dicts
    question_list = []
    for q in questions:
        question_list.append({
            "question": q[0],
            "options": [q[1], q[2], q[3], q[4]],
            "answer": q[5]
        })
    random.shuffle(question_list)
    return question_list

def save_highscore(chat_id, new_score):
    """Saves a new high score, but only if it's higher than the previous one."""
    conn = sqlite3.connect('./quiz_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT highscore FROM highscores WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    if result:
        current_highscore = result[0]
        if new_score > current_highscore:
            cursor.execute("UPDATE highscores SET highscore=? WHERE chat_id=?", (new_score, chat_id))
            bot.send_message(chat_id, "You've set a new high score! 🎉")
    else:
        cursor.execute("INSERT INTO highscores (chat_id, highscore) VALUES (?, ?)", (chat_id, new_score))
        bot.send_message(chat_id, "This is your first score, now saved as your high score!")
    conn.commit()
    conn.close()

# --- Logging Setup ---

# Set up logging to a file to track errors and events.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_log.log"),
        logging.StreamHandler()
    ]
)

# --- Command Handlers ---

@bot.message_handler(commands=['start'])
def start_command(message):
    """Handles the /start command, welcoming the user."""
    welcome_message = (
        "Hello! I am an advanced quiz bot. "
        "I can test your knowledge in various subjects.\n\n"
        "To start a quiz, please use the /quiz command."
    )
    bot.reply_to(message, welcome_message)
    logging.info(f"User {message.chat.id} started the bot.")

@bot.message_handler(commands=['quiz'])
def show_categories(message):
    """Displays quiz categories for the user to choose from."""
    try:
        conn = sqlite3.connect('./quiz_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM questions")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        # Create reply keyboard for categories
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        for cat in categories:
            markup.add(types.KeyboardButton(cat))
        bot.send_message(
            message.chat.id,
            "Please choose a quiz category:",
            reply_markup=markup
        )
        user_quiz_data[message.chat.id] = {'state': 'awaiting_category'}
        logging.info(f"User {message.chat.id} prompted to choose a category.")
    except Exception as e:
        logging.error(f"Database error in show_categories: {e}")
        bot.reply_to(message, "Sorry, I had an issue getting the quiz categories. Please try again later.")

@bot.message_handler(commands=['highscore'])
def show_highscore(message):
    """Retrieves and displays the user's highest score."""
    try:
        chat_id = message.chat.id
        conn = sqlite3.connect('./quiz_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT highscore FROM highscores WHERE chat_id=?", (chat_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            highscore = result[0]
            bot.reply_to(message, f"🏆 Your current high score is: {highscore} out of 5.")
        else:
            bot.reply_to(message, "You haven't completed a quiz yet! Start one with /quiz.")
        logging.info(f"User {chat_id} requested high score.")
    except Exception as e:
        logging.error(f"Database error in show_highscore: {e}")
        bot.reply_to(message, "Sorry, I had an issue retrieving your high score. Please try again.")

@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(message):
    """Displays the top 5 high scores from the database."""
    try:
        conn = sqlite3.connect('./quiz_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT highscore FROM highscores ORDER BY highscore DESC LIMIT 5")
        top_scores = [row[0] for row in cursor.fetchall()]
        conn.close()
        if top_scores:
            leaderboard_text = "Top 5 High Scores:\n"
            for i, score in enumerate(top_scores):
                leaderboard_text += f"{i + 1}. {score} out of 5\n"
            bot.reply_to(message, leaderboard_text)
        else:
            bot.reply_to(message, "The leaderboard is empty. Be the first to play!")
        logging.info(f"User {message.chat.id} requested the leaderboard.")
    except Exception as e:
        logging.error(f"Database error in show_leaderboard: {e}")
        bot.reply_to(message, "Sorry, I couldn't access the leaderboard right now.")

# --- Multi-Step Conversation Handlers ---

@bot.message_handler(func=lambda message: message.chat.id in user_quiz_data and user_quiz_data[message.chat.id].get('state') == 'awaiting_category')
def start_quiz_from_category(message):
    """Starts the quiz after the user has selected a category."""
    chat_id = message.chat.id
    category = message.text
    
    try:
        questions = get_questions_by_category(category)
        if not questions:
            bot.send_message(chat_id, "I couldn't find any questions for that category. Please choose a valid one from the keyboard.")
            return

        # Initialize the quiz state for this user.
        user_quiz_data[chat_id] = {
            'state': 0,
            'score': 0,
            'questions': questions
        }
        
        # Hide the reply keyboard
        markup = types.ReplyKeyboardRemove(selective=True)
        bot.send_message(chat_id, f"Great choice! Starting the {category} quiz now...", reply_markup=markup)
        
        # Send the first question.
        send_question(chat_id)
        logging.info(f"User {chat_id} started a new quiz in the '{category}' category.")
    
    except Exception as e:
        logging.error(f"Error starting quiz for user {chat_id}: {e}")
        bot.send_message(chat_id, "Sorry, something went wrong while starting the quiz. Please try /quiz again.")

def send_question(chat_id):
    """Sends the current question to the user."""
    try:
        current_question_index = user_quiz_data[chat_id]['state']
        question_data = user_quiz_data[chat_id]['questions'][current_question_index]
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for option in question_data['options']:
            button = types.InlineKeyboardButton(option, callback_data=option)
            markup.add(button)
        
        bot.send_message(
            chat_id, 
            f"Question {current_question_index + 1}/{len(user_quiz_data[chat_id]['questions'])}: {question_data['question']}",
            reply_markup=markup
        )
    except Exception as e:
        logging.error(f"Error sending question to user {chat_id}: {e}")
        bot.send_message(chat_id, "Sorry, an error occurred. The quiz will be ended.")
        if chat_id in user_quiz_data:
            del user_quiz_data[chat_id]

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    """Processes the user's answer from the inline keyboard."""
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    bot.answer_callback_query(call.id)
    
    if chat_id not in user_quiz_data or 'questions' not in user_quiz_data[chat_id]:
        bot.send_message(chat_id, "Please start a new quiz with /quiz.")
        return
        
    current_state = user_quiz_data[chat_id]
    current_question_index = current_state['state']
    
    # Check if the user's answer is correct.
    correct_answer = current_state['questions'][current_question_index]['answer']
    user_answer = call.data
    
    if user_answer == correct_answer:
        current_state['score'] += 1
        bot.send_message(chat_id, "Correct! ✅")
    else:
        bot.send_message(chat_id, f"Incorrect. The correct answer was: {correct_answer} ❌")
        
    current_state['state'] += 1
    
    # Remove the inline keyboard from the previous message.
    bot.edit_message_reply_markup(
        chat_id=chat_id, 
        message_id=message_id, 
        reply_markup=None
    )

    if current_state['state'] >= len(current_state['questions']):
        end_quiz(chat_id)
    else:
        send_question(chat_id)
        
def end_quiz(chat_id):
    """Finalizes the quiz, shows the score, and saves the high score."""
    final_score = user_quiz_data[chat_id]['score']
    total_questions = len(user_quiz_data[chat_id]['questions'])
    
    bot.send_message(
        chat_id,
        f"Quiz finished! 🎉\n\n"
        f"Your final score is: {final_score} out of {total_questions}."
    )
    
    save_highscore(chat_id, final_score)
    
    del user_quiz_data[chat_id]
    logging.info(f"Quiz finished for user {chat_id}. Score: {final_score}/{total_questions}")

# --- Main Bot Loop ---

if __name__ == '__main__':
    setup_database()
    logging.info("Bot is starting...")
    print("Bot is running...")
    bot.polling()
