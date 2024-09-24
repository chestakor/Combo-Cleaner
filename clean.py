import re
from telegram import Update
from telegram.ext import ContextTypes

# Process the file for /clean command
async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Detect type of content based on the pattern
    if "@" in content and ":" in content:
        # Email:Password format
        cleaned_content = clean_combo(content)
        await update.message.reply_text(f"Email:Password found ✅\n{cleaned_content}")
    elif re.search(r'\d{16}', content):
        # Credit Card format
        cleaned_content = clean_cc(content)
        await update.message.reply_text(f"CC found ✅\n{cleaned_content}")
    else:
        await update.message.reply_text("File format not recognized.")

# Clean email:password combos
def clean_combo(content: str) -> str:
    lines = content.strip().split("\n")
    total_lines = len(lines)
    unique_lines = list(set(lines))  # Remove duplicates
    duplicate_count = total_lines - len(unique_lines)
    
    return f"━━━━━━━━━━━━━━━━\nType: Email:Pass\nTotal: {total_lines}\nDuplicates: {duplicate_count}\n━━━━━━━━━━━━━━━━\nCombo Cleaner By: Aftab👑"

# Clean credit card numbers
def clean_cc(content: str) -> str:
    lines = content.strip().split("\n")
    total_lines = len(lines)
    unique_lines = list(set(lines))  # Remove duplicates
    duplicate_count = total_lines - len(unique_lines)
    
    return f"━━━━━━━━━━━━━━━━\nType: CC\nTotal: {total_lines}\nDuplicates: {duplicate_count}\n━━━━━━━━━━━━━━━━\nCombo Cleaner By: Aftab👑"
