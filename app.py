import os
import hashlib
import datetime
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request,jsonify, redirect, url_for, flash, session
import urllib.parse
import stripe
from ed import whatcrypt
from em import _email
from datetime import datetime as dt

load_dotenv()

stripe.api_key = 'sk_test_51O9FyrErLa42fbUSMRlT5TYaoYnro6Gsq7mq2iSmHKMj2kU2G9pzkz61PHFQANQdvJN471f46VyydY6abf6SRmNV00oadLxKEw'

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
reservations_collection = db['reservations']
# Define user types
users = ['owner', 'customer']

# Define file upload extensions
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# If the directory doesn't exist, make it exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_APP_SECRET").encode()
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=1)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to get md5 checksum of image file
def get_md5_checksum(image_path):
    with open(image_path, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

# Function to generate image file name
gen_img_name = lambda image_path: f"{get_md5_checksum(image_path)}.{os.path.basename(image_path).split('.')[-1]}"

###### Define application routings ######

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/<user>/login', methods=['GET', 'POST'])
def user_login(user):
    if user not in users:
        return render_template('404.html')

    match request.method:
        case 'GET':
            return render_template(f'{user}/login.html')
        case 'POST':
            email = request.form['email'].lower()
            password = request.form['password']
            # Retrieve the document with <email> id
            user_creds = users_collection.find_one({'email': email})
            if user_creds:
                if user_creds['user_type'] == user:
                    if check_password_hash(user_creds['password'], password):
                        # Initialize session
                        session['email'] = email
                        session['user_type'] = user
                        session['user_id'] = str(user_creds['_id'])
                        # Authenticate login
                        _email(email, "login")
                        flash(f'User [{session["user_id"][-5:]}] authenticated successfully!', 'success')
                        return redirect(f'/{user}/dashboard')
                    else: # password doesn't match
                        flash(f"Password doesn't match! Please, try again...", 'error')
                        return redirect(f'/{user}/login')
                else: # no account registered with <user_creds> in <users_collection>
                    flash(f"Want to create a [{user}] account? Please, register...", 'info')
                    return redirect(f'/{user}/login')
            flash(f"Account with [{email}] doesn't exist! Please register...", 'error')
            return redirect(f'/{user}/register')
        case _:
            return render_template('405.html')

@app.route('/<user>/resetpassword', methods=['GET', 'POST'])
def pass_reset(user):
    if user not in users:
        return render_template('404.html')
    match request.method:
        case 'GET':
            return render_template(f'{user}/reset.html')
        case 'POST':
            email = request.form['email'].lower()
            user_creds = users_collection.find_one({'email': email})
            if user_creds:
                if user_creds['user_type'] == user:
                    key = os.getenv("SECRET_DE2EN_KEY")
                    _email(email,[user_creds, whatcrypt(key, user_creds['enpass'], "decrypt")])
                    flash(f'Your credentials are sent to your email.', 'success')
                    return redirect(f'/{user}/resetpassword')
            else: # no account registered with <user_creds> in <users_collection>
                flash(f"Email is not registered with us", 'error')
                return redirect(f'/{user}/resetpassword')
            flash(f"Email is not registered as {user}", 'error')
            return redirect(f'/{user}/resetpassword')
        case _:
            return render_template('405.html')

@app.route('/<user>/register', methods=['GET', 'POST'])
def user_register(user):
    key = os.getenv("SECRET_DE2EN_KEY")
    if user not in users:
        return render_template('404.html')
    match request.method:
        case 'GET':
            return render_template(f'{user}/register.html')
        case 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email'].lower()
            password = request.form['password']
            _ = request.form['confirm-password']
            try:
                import mcheck
                required = f"The email address {email} is valid."
                value = mcheck.check_email_exists(email)
                if value==required:
                    try:
                        user_cred = len(users_collection.find_one({'email': email}))
                        if user_cred > 0:
                        # Register/save user credentials to `users` collection
                            flash(f'Email address is already registered.', 'info')
                            return redirect(f'/{user}/register')
                    except:
                        _ = users_collection.insert_one(dict(fname=fname,
                                                            lname=lname,
                                                            email=email,
                                                            password=generate_password_hash(password, method='pbkdf2:sha256'),
                                                            enpass=whatcrypt(key, password, "encrypt"),
                                                            user_type=user))
                        _email(to=email,what=f'{user}-register')
                        flash(f'Hello "{fname} {lname}" {chr(0x1F44B)} You have registered successfully. Now, please login...', 'success')
                        return redirect(f'/{user}/login')
                else:
                    flash(f"Error: Email doesn't exist. Please enter a valid email", 'error')
                    return render_template(f'{user}/register.html')
            except Exception as e:
                flash(f'{e}', 'error')
                return render_template(f'{user}/register.html')
        case _:
            return render_template('405.html')
        
@app.route('/<user>/dashboard', methods=['GET']) # Only accepts redirects from login
def user_dashboard(user):
    if 'email' not in session or 'user_type' not in session or 'user_id' not in session:
        flash('Access restricted! Please login to continue...', 'warning')
        return redirect(f'/{user}/login')
    if user not in users:
        return render_template('404.html')
    boat_documents = list()
    match user:
        case 'owner':
            boat_documents = boats_collection.find({"owner_id": ObjectId(session['user_id'])})
            user_documents = users_collection.find_one({"_id": ObjectId(session['user_id'])})
        case 'customer':
            user_documents = users_collection.find_one({"_id": ObjectId(session['user_id'])})
            boat_documents = boats_collection.find()
    return render_template(f'{user}/dashboard.html', str=str, users=user_documents ,boats=boat_documents)

@app.route('/owner/boats/create', methods=['GET', 'POST'])
def create_boat():
    if 'email' not in session or 'user_type' not in session or 'user_id' not in session:
        flash('Access restricted! Please login to continue...', 'warning')
        return redirect('/owner/login')

    match request.method:
        case 'GET':
            return render_template('owner/create.html')
        case 'POST':
            try:
                img_file = request.files['image']
                filename = secure_filename(img_file.filename)
                img_file.save(filepath:=os.path.join(app.config['UPLOAD_FOLDER'], filename))
                os.rename(filepath, os.path.join(app.config['UPLOAD_FOLDER'], new_filename:=gen_img_name(filepath)))
                try:
                    boat_name = request.form['name']
                    boat_type = request.form['type']
                    boat_location = request.form['location']
                    try:
                        boat_price = float(request.form['price'])
                    except:
                        flash(f'Invalid Price. Please check!', 'error')
                        return redirect(f'/owner/boats/edit/{str(_id)}')
                    boat_availability = request.form['availability']
                    _ = boats_collection.insert_one(dict(owner_id=ObjectId(session['user_id']),
                                            image_url=os.path.join(os.path.split(app.config['UPLOAD_FOLDER'])[-1], new_filename),
                                            name=boat_name,
                                            type=boat_type,
                                            location=boat_location,
                                            price=boat_price,
                                            availability=boat_availability))
                except:
                    flash('Unable to add new boat! Please try again later...', 'error')
                    return redirect('/owner/dashboard')
            except Exception as ex:
                flash(f'{ex}', 'error')
                flash('Unable to upload image! Please try again later...', 'error')
                return redirect('/owner/dashboard')
            flash(f'New boat details added!', 'info')
            return redirect('/owner/dashboard')
        case _:
            return render_template('405.html')

@app.route('/owner/boats/edit/<_id>', methods=['GET', 'POST'])
def edit_boat_document(_id):
    if 'email' not in session or 'user_type' not in session or 'user_id' not in session:
        flash('Access restricted! Please login to continue...', 'warning')
        return redirect('/owner/login')
    match request.method:
        case 'GET':
            boat_document = boats_collection.find_one({"_id": ObjectId(_id)})
            return render_template('owner/edit.html', str=str, boat=boat_document)
        case 'POST':
            try:
                # Get the details from <form>
                boat_name = request.form['name']
                boat_type = request.form['type']
                boat_location = request.form['location']
                try:
                    boat_price = float(request.form['price'])
                except:
                    flash(f'Invalid Price. Please check!', 'error')
                    return redirect(f'/owner/boats/edit/{_id}')
                boat_availability = request.form['availability']
                # Update in <boats_collection>
                filter_map = {'_id': ObjectId(_id)}
                update = {"$set": dict(name=boat_name,
                                        type=boat_type,
                                        location=boat_location,
                                        price=boat_price,
                                        availability=boat_availability)}

                result = boats_collection.update_one(filter_map, update)
                flash(f'Boat [{_id[-5:]}] details updated!', 'success')
                return redirect('/owner/dashboard')
            except:
                flash(f'Boat [{_id[-5:]}] details not updated!', 'error')
                return redirect('/owner/dashboard')

        case _:
            return render_template('405.html')
        
@app.route('/<user>/details', methods=['GET', 'POST'])
def edit_account_document(user):
    if 'email' not in session or 'user_type' not in session or 'user_id' not in session:
        flash('Access restricted! Please login to continue...', 'warning')
        return redirect(f'/{user}/login')
    
    match request.method:
        case 'GET':
            user_creds = users_collection.find_one({'email': session['email']})
            return render_template(f'{user}/details.html', str=str, user=user_creds)
        case 'POST':
            f_name = request.form['fname']
            l_name = request.form['lname']
            email = str(session['email']).lower()
            password = request.form['password']
            confirm_password = request.form['confirm-password']
            user_creds = users_collection.find_one({'email': email})
            if user_creds:
                if user_creds['user_type'] == user:
                    if confirm_password == password and check_password_hash(user_creds['password'], password) and user_creds['email'] == email:
                        try:
                            # Update in <users_collection>
                            filter_map = {'email': user_creds['email']}
                            update = {"$set": dict(fname=f_name,
                                                    lname=l_name)}
                            result = users_collection.update_one(filter_map, update)
                            flash(f'Account details updated!', 'success')
                            return redirect(f'/{user}/dashboard')
                        except:
                            flash(f'{user_creds["email"]} Unable to update account details! Please try again later...', 'error')
                            return redirect(f'/{user}/dashboard')
                    else:
                        flash(f'Unable to update account details! Email or passwords do not match', 'warning')
                        return redirect(f'/{user}/dashboard')
            flash(f'Unable to update account details! Passwords do not match', 'error')
            return redirect(f'/{user}/dashboard')
        case _:
            return render_template('405.html')

@app.route('/owner/boats/delete/<_id>', methods=['GET', 'POST'])
def delete_boat_document(_id):
    try:
        filter_map = {'_id': ObjectId(_id)}
        boats_collection.delete_one(filter_map) # Delete document
        flash(f'Boat [{_id[-5:]}] deleted successfully!', 'info')
        return redirect('/owner/dashboard')
    except Exception as ex:
        flash(f'{ex}', 'error')
        flash(f'Unable to delete boat [{_id[-5:]}] details! Please try again later...', 'error')
        return redirect('/owner/dashboard')

@app.route('/<user>/delete', methods=['GET', 'POST'])
def delete_account_document(user):
    if user not in users:
        return render_template('404.html')
    
    match request.method:
        case 'GET':
            return render_template(f'/{user}/delete.html')
        case 'POST':
            email = request.form['email'].lower()
            _ = request.form['email1'].lower()
            user_creds = users_collection.find_one({'email': email})
            try:
                filter_map = {'_id': user_creds["_id"]}
                users_collection.delete_one(filter_map)
                if user=="owner":
                    filter_map = {'owner_id': user_creds["_id"]}
                    boats_collection.delete_many(filter_map)
                flash(f'{user_creds["fname"]} {user_creds["lname"]}`s {user} account is deleted.',"success")
                return redirect('/')
            except:
                flash(f'Unable to delete account details! Please try again later...', 'error')
                return redirect(f'/{user}/delete')
        case _:
            return render_template('405.html')
        
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/customer/boats/payment/<_id>', methods=['GET', 'POST'])
def boat_booking(_id):
    if 'email' not in session or 'user_type' not in session or 'user_id' not in session:
        flash('Access restricted! Please login to continue...', 'warning')
        return redirect('/customer/login')

    #flash(f'Payment for boat [{_id[-5:]}] is processing...', 'info')
    match request.method:
        case 'GET':
            filter_map = {'_id': ObjectId(_id)}
            a = boats_collection.find_one(filter_map)
            b = users_collection.find_one({'_id': ObjectId(session['user_id'])})
            if a["availability"] == "no":
                flash(f'No availability! Booking cannot be done.', 'error')
                return redirect('/customer/dashboard')
            hr = 1
            amt = a["price"]
            return render_template(f'payment.html', _id = _id, amt = int(amt), hr=hr)
        
        case 'POST':
            # Add stripe logic here for making real payments
            filter_map = {'_id': ObjectId(_id)}
            a = boats_collection.find_one(filter_map)
            b = users_collection.find_one({'_id': ObjectId(session['user_id'])})
            hours = int(request.form.get("number-of-hours"))
            amt = int(a["price"])
            trn_id = dt.now().strftime("%d%s")
            noc = b["fname"]+" "+b["lname"]
            if float(amt) <= 0 and len(noc)<=2:
                flash(f'Please enter valid details', 'error')
                return render_template(f'payment.html', _id = _id, amt = int(amt), hr=1)
            else:
                try:
                    token = request.form.get('token')
                    customer = stripe.Customer.create(name=f"{b['fname']} {b['lname']}",email=b['email'],source=token)  # replace with an actual token obtained from Stripe.js or Elements
                    payment_method = "pm_card_visa" #stripe.PaymentMethod.create(type='card', card={'number': "4242424242424242",'exp_month': "04", 'exp_year': "24", 'cvc': "242"})
                    payment_intent = stripe.PaymentIntent.create(customer=customer,amount=amt*100, currency='usd',description= f"Waterside: Boat Rental Services, Reservation Number: {trn_id}", payment_method=payment_method, confirm = True, automatic_payment_methods={'enabled': True}, return_url="http://127.0.0.1:3030/success")
                    update = {"$set": dict(availability="no")}
                    boats_collection.update_one(filter_map, update)
                    _ = payments_collection.insert_one(dict(intent_id = [str(payment_intent["client_secret"]).split("_secret")][0],
                                                            transaction_id = trn_id,
                                                            customer_id = b["_id"],
                                                            owner_id = a["owner_id"],
                                                            amount_paid = int(amt),
                                                            boat_id = a["_id"],
                                                            hours = hours))
                    _ = reservations_collection.insert_one(dict(transaction_id = trn_id, status = "Confirmed"))
                    return render_template('thank_you.html', amt=amt, noc = noc, rsvn = trn_id, email = b['email'])
                except Exception as e:
                    flash(f'Error: {str(e)}', 'error')
                    return render_template(f'payment.html', _id = _id, amt = int(amt), hr=1)
        case _ :
            return render_template('405.html')
        
@app.route('/success', methods = ['GET'])
def success():
    if request.method=='GET':
        return render_template('thank_you.html')
    

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    match request.method:
        case 'GET':
            try:
                transaction_id = request.form.get("conf")
            except:
                transaction_id = ""
            return render_template('reservations.html', conf = transaction_id)
        case 'POST':
            
            try:
                transaction_id = request.form.get("conf")
                payment_document = payments_collection.find_one({'transaction_id': transaction_id})
                boat_id = payment_document["boat_id"]
                customer_id = payment_document["customer_id"]
                owner_id = payment_document["owner_id"]
                boat = boats_collection.find_one({'_id': boat_id})
                customer = users_collection.find_one({'_id' : customer_id})
                owner = users_collection.find_one({'_id': owner_id})
                reservation = reservations_collection.find_one({'transaction_id': transaction_id})
                receipt = f"Customer: {customer['fname']} {customer['lname']}<br>"
                receipt += f"Confirmation Number: {reservation['transaction_id']}<br><br>"
                from markupsafe import Markup
                receipt += "Boat Information:<br>"
                receipt += f"Boat Name: {boat['name']}<br>"
                receipt += f"Boaty Type: {boat['type']}<br>"
                receipt += f"Boat Location: {boat['location']}</center><br>"
                receipt += f"Boat Owner Name: {owner['fname']} {owner['lname']}<br>"
                
                receipt += f"Reservation Status: {reservation['status']}<br>"
                receipt += f"Boat Price: ${boat['price']:.2f}\hr<br>"
                receipt += f"Total Hours: {payment_document['hours']}<br>"
                receipt += f"Total Amount: ${payment_document['amount_paid']:.2f}<br>"
                flash(f'Reservation details found.', 'success')
                return render_template('reservations.html', receipt = Markup(receipt), imgurl = boat['image_url'], conf = transaction_id)
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
                return render_template('reservations.html', conf = transaction_id)
        case _ :
            return render_template('405.html')

@app.route('/reservations/cancel/<transaction_id>', methods=['GET', 'POST'])
def cancel(transaction_id):
    try:
        payment_document = payments_collection.find_one({'transaction_id': transaction_id})
        payment_intent_id = payment_document['intent_id'][0]
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        try:
            if payment_intent['status'] == 'succeeded': 
                refund = stripe.Refund.create(
                        payment_intent=payment_intent_id)
                result = f"Refund successful. Refund ID: {refund['id']}"
            else:
                result ="PaymentIntent is not in a refundable state."
        except:
            result ="Charge has already been refunded."

        update = {"$set": dict(availability="yes")}
        boats_collection.update_one({'_id':payment_document['boat_id']}, update)
        update = {"$set": dict(status="Canceled")}
        reservations_collection.update_one({'transaction_id':transaction_id}, update)
        flash(f'Reservation {transaction_id} has been canceled. {result}', 'success')
        return redirect('/reservations')
    except Exception as e:
        flash(f'Reservation {e} has been canceled already.', 'error')
        return redirect('/reservations')
        
   
@app.route('/logout', methods=['GET'])
def logout():
    # Destroy session
    session.pop('email')
    session.pop('user_type')
    session.pop('user_id')
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(port = 3030, debug=False)