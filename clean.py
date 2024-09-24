import re

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    combo_type = "Email:Pass" if "@" in lines[0] else "CC"
    unique_lines = set(lines)
    total_lines = len(lines)
    duplicate_lines = total_lines - len(unique_lines)
    
    return total_lines, duplicate_lines, combo_type

def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    unique_lines = set()
    cleaned_lines = []
    
    for line in lines:
        if "@" in line or re.match(r"^\d{16}\|\d{2}\|\d{2}\|\d{3}$", line.strip()):
            if line not in unique_lines:
                cleaned_lines.append(line)
                unique_lines.add(line)
    
    cleaned_file_path = f"{len(cleaned_lines)}_cleaned.txt"
    
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.writelines(cleaned_lines)
    
    return cleaned_file_path, len(cleaned_lines)

def clean_specific_lines(file_path, first_line, last_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    unique_lines = set()
    cleaned_lines = []
    
    for i, line in enumerate(lines[first_line-1:last_line]):
        if "@" in line or re.match(r"^\d{16}\|\d{2}\|\d{2}\|\d{3}$", line.strip()):
            if line not in unique_lines:
                cleaned_lines.append(line)
                unique_lines.add(line)
    
    cleaned_file_path = f"{len(cleaned_lines)}_cleaned.txt"
    
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.writelines(cleaned_lines)
    
    return cleaned_file_path, len(cleaned_lines)
