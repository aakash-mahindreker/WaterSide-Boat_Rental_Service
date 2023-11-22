import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse
import stripe
from ed import whatcrypt
from em import _email
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
import requests
load_dotenv()
stripe.api_key = ''
username = "useraakash"
password = "Pass@123"
# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Reconstruct the MongoDB URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.8s4f9dx.mongodb.net/?retryWrites=true&w=majority"
# Create client to connect the database
#uri = os.getenv('MONGODB_URI')
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=os.getenv('MONGODB_PERMISSION_FILEPATH'))

# Connect to database (through client)
db = client['waterside']
users_collection = db['users']
boats_collection = db['boats']
payments_collection = db['payments']
reservations_collections = db['reservations']
'''
users = users_collection.find()
for data in users:
    print(data)

boats = boats_collection.find()
for data in boats:
    print(data)

payments = payments_collection.find()
for data in payments:
    print(data)
'''


transaction_id = '201700479757'
filter_map = {'transaction_id': transaction_id}
payment_document = payments_collection.find_one({'transaction_id': transaction_id})
payment = list
print(len(payment_document))

boat_id = payment_document["boat_id"]
customer_id = payment_document["customer_id"]
owner_id = payment_document["owner_id"]
amount = payment_document["amount_paid"]
hours = payment_document["hours"]

boats = boats_collection.find_one({'_id': boat_id})
customer = users_collection.find_one({'_id' : customer_id})
owner = users_collection.find_one({'_id': owner_id}) 
