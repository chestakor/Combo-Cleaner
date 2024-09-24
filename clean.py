import re

# Process the initial file and check the format
def process_file(bot, message, file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    if "@" in content and ":" in content:
        # Email:Password format
        bot.reply_to(message, "Email:Password found ✅")
    elif re.search(r'\d{16}', content):
        # Credit Card format
        bot.reply_to(message, "CC found ✅")
    else:
        bot.reply_to(message, "File format not recognized.")

# Remove duplicates and extra data, and optionally limit to a range of lines
def remove_duplicates(file_path, start_line=None, end_line=None):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove extra data if present and keep only combos
    combos = [line.strip() for line in lines if "@" in line or re.search(r'\d{16}', line)]
    unique_combos = list(set(combos))  # Remove duplicates

    if start_line and end_line:
        unique_combos = unique_combos[start_line-1:end_line]

    new_file_path = f"cleaned_{file_path}"
    with open(new_file_path, 'w') as new_file:
        new_file.write("\n".join(unique_combos))

    return new_file_path
