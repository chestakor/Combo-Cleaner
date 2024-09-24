import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your bot token and admin ID
TOKEN = '7386294555:AAHoRvYVyrJ-9JCvGXOWstrYejx2tOLtVgo'
ADMIN_ID = 5429071679

# Create a Flask app to keep the bot alive
app = Flask(__name__)

# Check if the user is the admin
def is_admin(user_id: int):
    return user_id == ADMIN_ID

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Welcome {user.first_name}, to the Combo Cleaner Bot!")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /clean command by replying to a .txt file.")

# Admin-only /clean command
async def clean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if is_admin(user.id):
        if update.message.reply_to_message and update.message.reply_to_message.document:
            file_id = update.message.reply_to_message.document.file_id
            new_file = await context.bot.get_file(file_id)
            file_path = f"{file_id}.txt"
            await new_file.download_to_drive(file_path)
            from clean import process_file
            await process_file(update, context, file_path)
            os.remove(file_path)  # Clean up the downloaded file after processing
        else:
            await update.message.reply_text("Please reply to a .txt file with the /clean command.")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

# Flask route to keep the service alive
@app.route('/')
def index():
    return "Bot is running."

# Start the bot
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('clean', clean))

    # Start Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == '__main__':
    main()
