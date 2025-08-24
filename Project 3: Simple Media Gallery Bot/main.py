# Import the telebot library. You'll need to install it first: pip install pyTelegramBotAPI
import telebot
from telebot import types

# --- Configuration ---
# Get your unique bot token from BotFather on Telegram.
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Create a new bot instance.
bot = telebot.TeleBot(BOT_TOKEN)

# A list of media items. You can replace these with your own URLs or file IDs.
# 'photo' requires a JPG or PNG.
# 'video' and 'gif' work similarly.
# The `file_id` is the ID Telegram assigns to a file after you've uploaded it.
# Using file_id is faster, but for this example, we'll use URLs.
MEDIA_ITEMS = [
    {
        'type': 'photo',
        'url': 'https://static.vecteezy.com/system/resources/thumbnails/040/890/255/small_2x/ai-generated-empty-wooden-table-on-the-natural-background-for-product-display-free-photo.jpg',
        'caption': 'This is the first image in the gallery.'
    },
    {
        'type': 'photo',
        'url': 'https://png.pngtree.com/thumb_back/fh260/background/20230411/pngtree-nature-forest-sun-ecology-image_2256183.jpg',
        'caption': 'Here is the second photo for you.'
    },
    {
        'type': 'video',
        'url': 'https://v.ftcdn.net/14/60/39/86/240_F_1460398696_eq4zgMIpE4pktp2qajp9qBmVq2JJyuvJ_ST.mp4',
        'caption': 'A short sample video.'
    },
    {
        'type': 'photo',
        'url': 'https://cdn.pixabay.com/photo/2025/08/02/03/27/squirrel-9749860_1280.jpg',
        'caption': 'This is the final photo.'
    }
]

# A simple dictionary to store the current media index for each user.
# This allows the bot to handle multiple users independently.
user_data = {}

# --- Helper Functions ---

# A function to build the inline keyboard.
def build_gallery_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    # The 'callback_data' is what the bot receives when a button is pressed.
    # It allows you to identify which button was clicked.
    next_button = types.InlineKeyboardButton("Next", callback_data='next')
    previous_button = types.InlineKeyboardButton("Previous", callback_data='previous')
    exit_button = types.InlineKeyboardButton("Exit Gallery", callback_data='exit')
    markup.add(previous_button, next_button, exit_button)
    return markup

# A function to send the current media item to the user.
def send_gallery_item(chat_id, message_id, index):
    item = MEDIA_ITEMS[index]
    
    # We need to use InputMedia to edit the message.
    if item['type'] == 'photo':
        media = types.InputMediaPhoto(item['url'], caption=item['caption'])
    elif item['type'] == 'video':
        media = types.InputMediaVideo(item['url'], caption=item['caption'])
    else:
        # Fallback for unsupported types
        bot.send_message(chat_id, "Sorry, this media type is not supported.")
        return

    # Edit the message to show the new media and update the keyboard.
    bot.edit_message_media(
        media=media,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=build_gallery_keyboard()
    )


# --- Command Handler ---

# This function handles the /gallery command.
@bot.message_handler(commands=['gallery'])
def show_gallery(message):
    chat_id = message.chat.id
    
    # Initialize the user's index to the first item (0).
    user_data[chat_id] = 0
    
    # Send the first item from the list. We use send_photo here as a starting point.
    # You could also use send_video, etc. depending on your first item's type.
    # The `reply_markup` attaches the inline keyboard to this message.
    bot.send_photo(
        chat_id,
        MEDIA_ITEMS[0]['url'],
        caption=MEDIA_ITEMS[0]['caption'],
        reply_markup=build_gallery_keyboard()
    )

# --- Callback Query Handler ---

# This handler processes all button presses from inline keyboards.
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    # Get the user's current index, or default to 0 if not found.
    current_index = user_data.get(chat_id, 0)
    
    if call.data == 'next':
        # Increment the index and use the modulo operator (%) to loop back to the beginning.
        new_index = (current_index + 1) % len(MEDIA_ITEMS)
        user_data[chat_id] = new_index
        
        # Call the helper function to edit the message and show the new media.
        send_gallery_item(chat_id, message_id, new_index)
        
    elif call.data == 'previous':
        # Decrement the index. If it goes below 0, loop back to the end of the list.
        new_index = (current_index - 1 + len(MEDIA_ITEMS)) % len(MEDIA_ITEMS)
        user_data[chat_id] = new_index

        send_gallery_item(chat_id, message_id, new_index)
        
    elif call.data == 'exit':
        # Acknowledge the user's action and remove the keyboard.
        # We can edit the message to just show text and no keyboard.
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None  # Set reply_markup to None to remove it.
        )
        bot.send_message(chat_id, "Gallery exited. Hope you enjoyed it!")
    
    # Always answer the callback query to let Telegram know you've received it.
    # This removes the "loading" state from the button.
    bot.answer_callback_query(call.id)

# --- Start the Bot ---

# This line starts the bot.
print("Bot is running...")
bot.polling()
