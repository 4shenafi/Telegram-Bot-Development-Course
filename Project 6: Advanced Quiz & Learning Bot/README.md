# Advanced Quiz & Learning Bot

This project is part of the Telegram Bot Development Course. It teaches you how to build an advanced quiz bot using Python, pyTelegramBotAPI, and SQLite.

## What Does This Bot Do?
- Runs multi-category quizzes for users, tracking their progress and scores.
- Stores high scores and quiz questions in a local SQLite database (`./quiz_bot.db`).
- Supports multiple subjects (Math, English, Physics) and can be extended with more.
- Uses inline keyboards for answer selection and interactive feedback.
- Shows leaderboards and personal high scores.

## How the Bot Works
1. **Start the Bot**
   - Run `python main.py` after setting your bot token.
   - The bot prints "Bot is running..." and starts listening for messages.
2. **Start a Quiz**
   - Send `/quiz` to begin.
   - The bot will show available categories. Choose one to start.
   - The bot will ask each question in order, using inline buttons for answers.
3. **Answer Questions**
   - Tap the button for your chosen answer.
   - The bot will tell you if you are correct or not, then move to the next question.
4. **Finish and Save Score**
   - After the last question, the bot shows your final score.
   - If your score is higher than your previous high score, it will be saved.
5. **View High Score**
   - Send `/highscore` to see your best score so far.
6. **View Leaderboard**
   - Send `/leaderboard` to see the top 5 scores.
7. **Get Help**
   - Send `/start` for a welcome message and instructions.

## Code Walkthrough
- **Database Setup**
  - `setup_database()`: Creates the SQLite database and tables in the script's directory.
  - Questions and scores are stored in `./quiz_bot.db`.
- **Commands**
  - `/start`: Welcomes the user and gives instructions.
  - `/quiz`: Begins a new quiz and sends the first question.
  - `/highscore`: Shows your highest score from previous quizzes.
  - `/leaderboard`: Shows the top 5 scores.
- **Quiz Logic**
  - `user_quiz_data`: Tracks each user's current question and score.
  - `get_questions_by_category()`: Loads questions for the selected category.
  - `send_question()`: Sends the current question with answer buttons.
  - `handle_answer()`: Processes the user's answer, gives feedback, and moves to the next question.
  - `end_quiz()`: Shows the final score and saves it if it's a new high score.
- **Saving Scores**
  - `save_highscore()`: Updates the database only if the new score is higher than the previous one.
- **Error Handling & Logging**
  - All database and quiz operations use try/except blocks and log errors for easier debugging.

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   ```
2. **Navigate to the project directory**
   ```bash
   cd "Project 6: Advanced Quiz & Learning Bot"
   ```
3. **Install dependencies**
   ```bash
   pip install pyTelegramBotAPI
   ```
4. **Configure your bot token**
   - Get a token from [BotFather](https://t.me/BotFather).
   - Replace `BOT_TOKEN` in `main.py` with your token.
5. **Run the bot**
   ```bash
   python main.py
   ```

## Learning Outcomes
- How to use inline keyboards for interactive quizzes in Telegram bots
- How to track user state for multi-step flows
- How to store and update user scores and questions with SQLite
- How to handle errors and log events for debugging

## License
This project is for educational purposes as part of the Telegram Bot Development Course.
