from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("SECRET_DE2EN_KEY")
def whatcrypt(key, message, what):
    if what == "encrypt":
        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())
        return encMessage
    elif what == "decrypt":
        fernet = Fernet(key)
        decMessage = fernet.decrypt(message).decode()
        print("decrypted string: ", decMessage)
        return decMessage
    return None

#msg = "Aakash"
#en = whatcrypt(key, msg, "encrypt") 
#dec = whatcrypt(key, en, "decrypt")
#print(en, dec, type(en), type(dec))