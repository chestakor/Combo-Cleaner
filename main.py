import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from clean import process_file, remove_duplicates, clean_specific_lines
from keep_alive import keep_alive

# Replace with your bot token and admin ID
TOKEN = '7386294555:AAHoRvYVyrJ-9JCvGXOWstrYejx2tOLtVgo'
ADMIN_ID = 5429071679

bot = telebot.TeleBot(TOKEN)

user_data = {}

# Check if the user is the admin
def is_admin(user_id):
    return user_id == ADMIN_ID

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"Welcome <b>{message.from_user.first_name}</b>, to the Combo Cleaner Bot!", parse_mode='HTML')

# /help command
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Use /clean command by replying to a .txt file to clean your combos.", parse_mode='HTML')

# Admin-only /clean command
@bot.message_handler(commands=['clean'])
def clean_command(message):
    if is_admin(message.from_user.id):
        if message.reply_to_message and message.reply_to_message.document:
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = f"{message.reply_to_message.document.file_id}.txt"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            total_lines, duplicate_lines, combo_type = process_file(file_path)
            
            # Store file path in user_data instead of passing it in callback data
            user_data[message.from_user.id] = {"file_path": file_path}
            
            # Send initial message
            markup = InlineKeyboardMarkup()
            start_button = InlineKeyboardButton(text="START", callback_data="start")
            customize_button = InlineKeyboardButton(text="Customize", callback_data="customize")
            markup.add(customize_button, start_button)
            
            bot.reply_to(message, f"{combo_type} found ✅\n━━━━━━━━━━━━━━━━\n<b>Type:</b> {combo_type}\n<b>Total:</b> {total_lines}\n<b>Duplicates:</b> {duplicate_lines}\n━━━━━━━━━━━━━━━━\n<b>Bot By:</b> Aftab👑", reply_markup=markup, parse_mode='HTML')
        else:
            bot.reply_to(message, "Please reply to a .txt file with the /clean command.", parse_mode='HTML')
    else:
        bot.reply_to(message, "You are not authorized to use this command.", parse_mode='HTML')

# Handle button callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if user_id not in user_data:
        bot.send_message(call.message.chat.id, "Session expired. Please try again.")
        return
    
    file_path = user_data[user_id]['file_path']
    
    if call.data == "start":
        bot.send_message(call.message.chat.id, "Your combo is being processed sir\nPlease wait", parse_mode='HTML')
        cleaned_file_path, total_lines = remove_duplicates(file_path)
        with open(cleaned_file_path, 'rb') as new_file:
            bot.send_document(call.message.chat.id, new_file, caption=f"Cleaned Combos✅\n_____________________\n<b>Type:</b> Email:Pass\n<b>Total:</b> {total_lines}\n_____________________\n<b>Req by:</b> {call.from_user.username}\n<b>Bot by:</b> Aftab👑", parse_mode='HTML')
        os.remove(cleaned_file_path)
    
    elif call.data == "customize":
        bot.send_message(call.message.chat.id, "Enter first line:", parse_mode='HTML')
        user_data[user_id]['awaiting_first_line'] = True

# Handle customization input
@bot.message_handler(func=lambda message: message.from_user.id in user_data)
def handle_customization(message):
    user_id = message.from_user.id
    if 'awaiting_first_line' in user_data[user_id]:
        try:
            first_line = int(message.text)
            user_data[user_id]['first_line'] = first_line
            bot.send_message(message.chat.id, "Enter last line:", parse_mode='HTML')
            del user_data[user_id]['awaiting_first_line']
            user_data[user_id]['awaiting_last_line'] = True
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid number.", parse_mode='HTML')
    elif 'awaiting_last_line' in user_data[user_id]:
        try:
            last_line = int(message.text)
            first_line = user_data[user_id]['first_line']
            file_path = user_data[user_id]['file_path']
            
            cleaned_file_path, total_lines = clean_specific_lines(file_path, first_line, last_line)
            with open(cleaned_file_path, 'rb') as new_file:
                bot.send_document(message.chat.id, new_file, caption=f"Cleaned Combos✅\n_____________________\n<b>Type:</b> Email:Pass\n<b>Total:</b> {total_lines}\n<b>Range:</b> {first_line}-{last_line}\n_____________________\n<b>Req by:</b> {message.from_user.username}\n<b>Bot by:</b> Aftab👑", parse_mode='HTML')
            
            os.remove(cleaned_file_path)
            del user_data[user_id]
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid number.", parse_mode='HTML')

if __name__ == "__main__":
    keep_alive()
    bot.polling()
