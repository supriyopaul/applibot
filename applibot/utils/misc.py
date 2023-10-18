import hashlib
import re
import os

def get_resume(fpath='../../data/.myresume.txt'):
    try:
        with open(fpath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file at path {fpath} does not exist."
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"

def get_saved_info(fpath='../../data/.myinfo.txt'):
    try:
        with open(fpath, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"


def append_additional_info(info, fpath='../../data/.myinfo.txt'):
    try:
        with open(fpath, 'a') as file:
            file.write(info + '\n')
        return True
    except Exception as e:
        return f"An error occurred while writing to the file: {str(e)}"
    
def log_interaction(prompt, response, fpath='./responses.log'):
    try:
        with open(fpath, 'a') as file:
            file.write("Prompt:\n")
            file.write(prompt + "\n")
            file.write("Response:\n")
            file.write(response + "\n")
            file.write("="*80 + "\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {str(e)}")
        try:
            with open(fpath, 'w') as file:
                pass
        except Exception as e:
            print(f"An error occurred while creating the file: {str(e)}")

RED = '\033[91m'
ORANGE = '\033[93m'
GREEN = '\033[92m'
PURPLE = '\033[95m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def color_text(text, color_code):
    return f"{color_code}{text}{RESET}"

def get_multiline_input(prompt):
    print(color_text(prompt, GREEN))
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except KeyboardInterrupt:
            print(color_text("\nInput interrupted. Proceeding with the entered text.", GREEN))
            break
    return '\n'.join(lines)

def compute_sha256(text):
    """Compute the SHA-256 hash of a given text."""
    return hashlib.sha256(text.encode()).hexdigest()

def extract_output_block(text):
    pattern = r'=====.*?start=====(.*?)=====.*?end====='
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def check_formatted_info(text):
    """Test the output formatting of the given text."""
    lines = text.split('\n')
    for line in lines:
        if not line:  # Skip empty lines
            continue
        if ": " not in line:
            return False, f"Line '{line}' does not contain ': '"
        key, value = line.split(": ", 1)
        if not key or not value:
            return False, f"Line '{line}' does not have text on each side of ': '"
    return True, "All lines are correctly formatted"

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_to_file(content, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f"form_{len(os.listdir(directory)) + 1}.txt")
    with open(filename, 'w') as f:
        f.write(content)
    print(color_text(f"Form saved to: {filename}", GREEN))
