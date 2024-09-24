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
    bot.reply_to(message, f"Welcome {message.from_user.first_name}, to the Combo Cleaner Bot!")

# /help command
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Use /combo command by replying to a .txt file to clean your combos.")

# Admin-only /combo command
@bot.message_handler(commands=['combo'])
def combo(message):
    if is_admin(message.from_user.id):
        if message.reply_to_message and message.reply_to_message.document:
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = f"{message.reply_to_message.document.file_id}.txt"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            total_lines, duplicate_lines, combo_type = process_file(file_path)
            
            # Send initial message
            markup = InlineKeyboardMarkup()
            start_button = InlineKeyboardButton(text="START", callback_data=f"start_{file_path}")
            customize_button = InlineKeyboardButton(text="Customize", callback_data=f"customize_{file_path}")
            markup.add(customize_button, start_button)
            
            bot.reply_to(message, f"{combo_type} found ✅\n━━━━━━━━━━━━━━━━\nType: {combo_type}\nTotal: {total_lines}\nDuplicates: {duplicate_lines}\n━━━━━━━━━━━━━━━━\nBot By: Aftab👑", reply_markup=markup)
        else:
            bot.reply_to(message, "Please reply to a .txt file with the /combo command.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Handle button callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, file_path = call.data.split('_', 1)
    
    if action == "start":
        bot.send_message(call.message.chat.id, "Your combo is being processed sir\nPlease wait")
        cleaned_file_path, total_lines = remove_duplicates(file_path)
        with open(cleaned_file_path, 'rb') as new_file:
            bot.send_document(call.message.chat.id, new_file, caption=f"Cleaned Combos✅\n_____________________\nType: Email:Pass\nTotal: {total_lines}\n_____________________\nReq by: {call.from_user.username}\nBot by: Aftab👑")
        os.remove(cleaned_file_path)
    
    elif action == "customize":
        user_data[call.from_user.id] = {"file_path": file_path}
        bot.send_message(call.message.chat.id, "Enter first line:")

# Handle customization input
@bot.message_handler(func=lambda message: message.from_user.id in user_data)
def handle_customization(message):
    user_input = message.text
    if 'first_line' not in user_data[message.from_user.id]:
        user_data[message.from_user.id]['first_line'] = int(user_input)
        bot.send_message(message.chat.id, "Enter last line:")
    else:
        last_line = int(user_input)
        first_line = user_data[message.from_user.id]['first_line']
        file_path = user_data[message.from_user.id]['file_path']
        
        cleaned_file_path, total_lines = clean_specific_lines(file_path, first_line, last_line)
        with open(cleaned_file_path, 'rb') as new_file:
            bot.send_document(message.chat.id, new_file, caption=f"Cleaned Combos✅\n_____________________\nType: Email:Pass\nTotal: {total_lines}\nRange: {first_line}-{last_line}\n_____________________\nReq by: {message.from_user.username}\nBot by: Aftab👑")
        
        os.remove(cleaned_file_path)
        del user_data[message.from_user.id]

if __name__ == "__main__":
    keep_alive()
    bot.polling()
