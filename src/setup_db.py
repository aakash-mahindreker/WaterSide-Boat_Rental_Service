import os
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse

# Replace "myuser" and "mypassword" with your actual username and password
username = "useraakash"
password = "Pass@123"

# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Reconstruct the MongoDB URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.8s4f9dx.mongodb.net/?retryWrites=true&w=majority"
load_dotenv()

#uri = os.getenv('MONGODB_URI')
print(uri)
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=os.getenv('MONGODB_PERMISSION_FILEPATH'))

# Database: `waterside`
db = client['waterside']

# Collection: `users`
collection = db['users'] # fname, lname, email, password, user_type
print("Users collection:", collection, end='\n\n')

# Index: `email` | Collection: `users`
#result = collection.create_index([('email', 1)])
#print("<Email> index for <users> collection:", result, end='\n\n')

# Collection: `boats`
collection = db['boats'] # owner_id, image_url, name, type, location, price, is_available
print("Boats collection:", collection, end='\n\n')

# Collection: `payments`
collection = db['payments'] 
print("Payments collection:", collection, end='\n\n')

# Collection: `reservations`
collection = db['reservations'] 
print("Reservations collection:", collection, end='\n\n')

print('[+] Database created successfully!')