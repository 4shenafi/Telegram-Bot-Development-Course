# User Profile Bot with SQLite

This project is part of the Telegram Bot Development Course. It teaches you how to build a simple user profile bot using Python, pyTelegramBotAPI, and SQLite.

## What Does This Bot Do?
- Lets users create, view, and update their profile (name, phone, age) via Telegram commands.
- Stores user data in a local SQLite database.
- Guides users step-by-step through profile creation and updating.

## How the Bot Works
1. **Start the Bot**
   - Run `python main.py` after setting your bot token.
   - The bot prints "Bot is running..." and starts listening for messages.
2. **Create Your Profile**
   - Send `/setprofile` to begin.
   - The bot will ask for your name, phone number, and age, one by one.
   - Your data is saved in the database.
3. **View Your Profile**
   - Send `/seeprofile` to see your saved information.
4. **Update Your Profile**
   - Send `/updateprofile` to change your name, phone, and age.
   - The bot will ask for all fields again and update your profile.
5. **Get Help**
   - Send `/help` to see all available commands and their descriptions.

## Code Walkthrough
- **Database Setup**
  - `setup_database()`: Creates the SQLite database and table if not present.
- **Commands**
  - `/start`: Welcomes the user and gives instructions.
  - `/help`: Lists all commands and their usage.
  - `/setprofile`: Starts the profile creation flow (asks for name, phone, age).
  - `/updateprofile`: Starts the profile update flow (asks for name, phone, age).
  - `/seeprofile`: Shows the user's saved profile.
- **Step Handlers**
  - The bot uses `register_next_step_handler` to guide users through each step.
  - Each step validates input and moves to the next question.
- **Validation**
  - Phone numbers are checked with a simple regex.
  - Age must be a valid integer.
- **Saving Data**
  - Data is saved or updated in the SQLite database using `REPLACE INTO`.

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   ```
2. **Navigate to the project directory**
   ```bash
   cd "Project 4: User Profile Bot with SQLite"
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
- How to use step handlers for multi-step user input in Telegram bots
- How to store and retrieve user data with SQLite
- How to validate user input and guide users interactively

## License
This project is for educational purposes as part of the Telegram Bot Development Course.
