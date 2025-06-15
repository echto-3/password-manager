import random
import string
import json
import os
from cryptography.fernet import Fernet

def generate_password(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    password = ""
    criteria = False
    has_numbers = False
    has_special_chars = False

    while not criteria or len(password) < min_length:
        random_char = random.choice(characters)
        password += random_char

        if random_char in digits:
            has_numbers = True
        elif random_char in special:
            has_special_chars = True

        criteria = True
        if numbers:
            criteria = has_numbers
        if special_characters:
            criteria = criteria and has_special_chars

    return password

PASSWORD_FILE = "passwords.json"
KEY_FILE = 'hehehaha.key'

def load_key():
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Key file not found. Run the key generator script first.")
    with open(KEY_FILE, "rb") as key_file:
        return Fernet(key_file.read())

fernet = load_key()

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}

    with open(PASSWORD_FILE, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data) 
        return json.loads(decrypted_data)
    except Exception as e:
        print("Error decrypting file:", e)
        return {}

def save_passwords(passwords):
    json_data = json.dumps(passwords, indent=4)
    encrypted_data = fernet.encrypt(json_data.encode())

    with open(PASSWORD_FILE, "wb") as file:
        file.write(encrypted_data)


def add_password(label, password):
    passwords = load_passwords()
    passwords[label.lower()] = password
    save_passwords(passwords)
    print(f"Password for '{label}' saved.")

def view_passwords():
    passwords = load_passwords()
    if not passwords:
        print("No passwords saved.")
        return
    for label, pwd in passwords.items():
        print(f"{label}: {pwd}")

# --- Main CLI interface ---
def main():
    while True:
        print("\n1. Generate and Save New Password")
        print("2. View All Passwords")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            label = input("Label for this password (e.g., Gmail): ")
            min_length = int(input("Minimum length of password: "))
            has_numbers = input("Include numbers? (y/n): ").lower() == "y"
            has_special = input("Include special characters? (y/n): ").lower() == "y"
            password = generate_password(min_length, has_numbers, has_special)
            print("Generated Password:", password)
            add_password(label, password)

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()