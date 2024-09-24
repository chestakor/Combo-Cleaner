import re

def process_file(bot, message, file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Detect type of content based on the pattern
    if "@" in content and ":" in content:
        # Email:Password format
        cleaned_content = clean_combo(content)
        bot.reply_to(message, f"Email:Password found ✅\n{cleaned_content}")
    elif re.search(r'\d{16}', content):
        # Credit Card format
        cleaned_content = clean_cc(content)
        bot.reply_to(message, f"CC found ✅\n{cleaned_content}")
    else:
        bot.reply_to(message, "File format not recognized.")

# Clean email:password combos
def clean_combo(content):
    lines = content.strip().split("\n")
    total_lines = len(lines)
    unique_lines = list(set(lines))  # Remove duplicates
    duplicate_count = total_lines - len(unique_lines)
    
    return f"━━━━━━━━━━━━━━━━\nType: Email:Pass\nTotal: {total_lines}\nDuplicates: {duplicate_count}\n━━━━━━━━━━━━━━━━\nCombo Cleaner By: Aftab👑"

# Clean credit card numbers
def clean_cc(content):
    lines = content.strip().split("\n")
    total_lines = len(lines)
    unique_lines = list(set(lines))  # Remove duplicates
    duplicate_count = total_lines - len(unique_lines)
    
    return f"━━━━━━━━━━━━━━━━\nType: CC\nTotal: {total_lines}\nDuplicates: {duplicate_count}\n━━━━━━━━━━━━━━━━\nCombo Cleaner By: Aftab👑"
