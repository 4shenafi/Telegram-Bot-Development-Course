# Multi-Step Quiz Bot

This project is part of the Telegram Bot Development Course. It teaches you how to build a multi-step quiz bot using Python, pyTelegramBotAPI, and SQLite.

## What Does This Bot Do?
- Runs a multi-question quiz for each user, tracking their progress and score.
- Stores each user's high score in a local SQLite database in the same directory as the script.
- Uses inline keyboards for answer selection and interactive feedback.

## How the Bot Works
1. **Start the Quiz**
   - Send `/start` to begin a new quiz.
   - The bot will ask each question in order, using inline buttons for answers.
2. **Answer Questions**
   - Tap the button for your chosen answer.
   - The bot will tell you if you are correct or not, then move to the next question.
3. **Finish and Save Score**
   - After the last question, the bot shows your final score.
   - If your score is higher than your previous high score, it will be saved.
4. **View High Score**
   - Send `/highscore` to see your best score so far.

## Code Walkthrough
- **Database Setup**
  - `setup_database()`: Creates the SQLite database and `highscores` table in the script's directory.
  - `get_db_path()`: Ensures the database is always created in the same folder as the code.
- **Commands**
  - `/start`: Begins a new quiz and sends the first question.
  - `/highscore`: Shows your highest score from previous quizzes.
- **Quiz Logic**
  - `user_quiz_data`: Tracks each user's current question and score.
  - `QUIZ_QUESTIONS`: List of questions, options, and correct answers.
  - `send_question()`: Sends the current question with answer buttons.
  - `handle_answer()`: Processes the user's answer, gives feedback, and moves to the next question.
  - `end_quiz()`: Shows the final score and saves it if it's a new high score.
- **Saving Scores**
  - `save_highscore()`: Updates the database only if the new score is higher than the previous one.

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   ```
2. **Navigate to the project directory**
   ```bash
   cd "Project 5: Multi-Step Quiz Bot"
   ```
3. **Install dependencies**
   ```bash
   pip install pyTelegramBotAPI
   ```
4. **Configure your bot token**
   - Get a token from [BotFather](https://t.me/BotFather).
   - Replace `BOT_TOKEN` in `main..py` with your token.
5. **Run the bot**
   ```bash
   python main..py
   ```

## Learning Outcomes
- How to use inline keyboards for interactive quizzes in Telegram bots
- How to track user state for multi-step flows
- How to store and update user scores with SQLite

## License
This project is for educational purposes as part of the Telegram Bot Development Course.
