
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


if __name__ == "__main__":
    print(get_saved_info())


