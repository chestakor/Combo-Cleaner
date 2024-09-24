import os
import telebot
from clean import process_file
from keep_alive import keep_alive

# Replace with your bot token and admin ID
TOKEN = '7386294555:AAHoRvYVyrJ-9JCvGXOWstrYejx2tOLtVgo'
ADMIN_ID = 5429071679

bot = telebot.TeleBot(TOKEN)

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
    bot.reply_to(message, "Use /clean command by replying to a .txt file.")

# Admin-only /clean command
@bot.message_handler(commands=['clean'])
def clean(message):
    if is_admin(message.from_user.id):
        if message.reply_to_message and message.reply_to_message.document:
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = f"{message.reply_to_message.document.file_id}.txt"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            process_file(bot, message, file_path)
            os.remove(file_path)
        else:
            bot.reply_to(message, "Please reply to a .txt file with the /clean command.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

if __name__ == "__main__":
    keep_alive()
    bot.polling()
