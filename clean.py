import os

def process_file(file_path):
    total_lines = 0
    combos = set()
    combo_type = ""

    with open(file_path, 'r') as file:
        for line in file:
            total_lines += 1
            line = line.strip()
            # Determine the combo type based on line content
            if ":" in line:
                if "@" in line.split(":")[0]:  # Email:Pass format
                    combo_type = "Email:Pass"
                    combos.add(line)
            elif "|" in line:
                combo_type = "CC"
                combos.add(line)  # Treat all CC lines as unique, use set to avoid duplicates
    
    duplicate_lines = total_lines - len(combos)  # Only consider unique combos
    with open(file_path, 'w') as file:
        for combo in combos:
            file.write(combo + "\n")

    return total_lines, duplicate_lines, combo_type

def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    unique_lines = set(lines)
    cleaned_file_path = file_path.replace('.txt', '_cleaned.txt')
    
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.writelines(unique_lines)
    
    return cleaned_file_path, len(unique_lines)

def clean_specific_lines(file_path, first_line, last_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    specific_lines = lines[first_line - 1:last_line]  # Adjust for 0-based index
    unique_specific_lines = set(specific_lines)
    cleaned_file_path = file_path.replace('.txt', '_custom_cleaned.txt')
    
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.writelines(unique_specific_lines)
    
    return cleaned_file_path, len(unique_specific_lines)
