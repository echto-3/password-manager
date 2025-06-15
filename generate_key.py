from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()

# Save it to a file
with open("hehehaha.key", "wb") as key_file:
    key_file.write(key)

print("Encryption key generated and saved to hehehaha.key")
