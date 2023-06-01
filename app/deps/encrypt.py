from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt(secret_value):
    """
    Encrypts a secret_value
    """
    key = load_key()
    encoded_secret_value = secret_value.encode()
    f = Fernet(key)
    encrypted_secret_value = f.encrypt(encoded_secret_value)

    return encrypted_secret_value

def decrypt(encrypted_value):
    """
    Decrypts an encrypted value
    """
    key = load_key()
    f = Fernet(key)
    decrypted_value = f.decrypt(encrypted_value)

    return decrypted_value.decode()