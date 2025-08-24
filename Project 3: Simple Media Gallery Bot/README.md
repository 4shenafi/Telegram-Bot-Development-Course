
# Simple Media Gallery Bot

This project is part of the Telegram Bot Development Course. It demonstrates how to build a media gallery bot using Python and the pyTelegramBotAPI library.

## What Does This Bot Do?
- Lets users browse a gallery of images and videos using inline navigation buttons (Next, Previous, Exit).
- Each media item has a caption and is displayed in chat.
- The gallery loops through items, so users can keep browsing.

## How the Bot Works
1. **Start the Bot**
   - Run `python main.py` after setting your bot token.
   - The bot will print "Bot is running..." and begin polling for messages.
2. **Open the Gallery**
   - Send `/gallery` in your chat with the bot.
   - The bot sends the first image with navigation buttons below it.
3. **Navigate the Gallery**
   - Use "Next" and "Previous" buttons to move through the gallery items.
   - The gallery loops, so "Next" after the last item returns to the first.
   - "Exit Gallery" removes the navigation buttons and sends a goodbye message.

## Code Explanation
- **Configuration**
  - `BOT_TOKEN`: Your Telegram bot token from BotFather.
  - `MEDIA_ITEMS`: List of media items (images/videos) with URLs and captions.
  - `user_data`: Tracks each user's current gallery position.
- **Keyboard & Navigation**
  - `build_gallery_keyboard()`: Creates inline buttons for navigation.
  - `send_gallery_item()`: Edits the current message to show the selected media item.
- **Handlers**
  - `/gallery` command: Starts the gallery for the user, sends the first item.
  - Callback query handler: Responds to button presses, updates the gallery view, or exits.
- **Bot Startup**
  - `bot.polling()`: Starts the bot and keeps it running.

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   ```
2. **Navigate to the project directory**
   ```bash
   cd "Project 3: Simple Media Gallery Bot"
   ```
3. **Install dependencies**
   ```bash
   pip install pyTelegramBotAPI
   ```
4. **Configure your bot token**
   - Get a token from [BotFather](https://t.me/BotFather).
   - Replace `YOUR_BOT_TOKEN_HERE` in `main.py` with your token.
5. **Run the bot**
   ```bash
   python main.py
   ```

## Learning Outcomes
- How to use inline keyboards for navigation in Telegram bots
- How to send and edit media messages
- How to manage user state for interactive features

## License
This project is for educational purposes as part of the Telegram Bot Development Course.
