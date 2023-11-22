import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime
import geoip

def _email(to, what):

    # Sender and recipient email addresses
    sender_email = "watersideboatrentalservice@gmail.com"
    recipient_email = to

    if what == "customer-register":
        # Email details
        subject = "Thank You for Registering with WaterSide: Boat Rental Service"
        message = """
Dear Customer,

We hope this message finds you well. On behalf of the entire WaterSide team, we would like to extend our heartfelt thanks for choosing WaterSide: Boat Rental Service for your boating needs. We are thrilled to have you as a new member of our community, and we look forward to serving you in the best way possible.

At WaterSide, we are committed to providing you with the finest boating experience, and your trust in our service is greatly appreciated. Whether you're planning a relaxing day on the water, an adventure-filled journey, or a special event, we are here to make it a memorable and enjoyable experience for you.

Here are a few things you can expect from WaterSide:

- A wide selection of well-maintained boats to suit your preferences.
- Friendly and knowledgeable boat owners to assist you with any questions or special requests.
- Competitive pricing and flexible rental options.
- Safety measures to ensure your peace of mind during your boating adventure.

Please don't hesitate to reach out to us if you have any questions or need assistance with anything. Your satisfaction is our top priority, and we are here to make your boating experiences as enjoyable as possible.

Once again, thank you for choosing WaterSide. We're excited to have you on board, and we can't wait to help you create unforgettable moments on the water.

Wishing you smooth sailing and endless fun on your future boating adventures!

Warm regards,

Aakash Mahindreker
Chief Executive Officer
WaterSide: Boat Rental Service
+1(214)218-6979


"""
    elif what == "owner-register":
        subject = "Thank You for Registering with WaterSide: Boat Rental Service"
        message = """
Dear Owner,

We hope this message finds you well. On behalf of the entire WaterSide team, we would like to extend our heartfelt thanks for choosing WaterSide: Boat Rental Service as your platform for listing your boat(s) for rental. We are excited to have you on board as a valued partner, and we look forward to a successful and mutually beneficial partnership.

At WaterSide, we are committed to providing a seamless and rewarding experience for boat owners like you. Your trust in our platform is greatly appreciated, and we are dedicated to helping you maximize your boat's rental potential. Here's what you can expect as a registered boat owner on WaterSide:

- A user-friendly platform to list your boats for rental with ease.
- A wide and diverse customer base looking for memorable boating experiences.
- Tools and resources to manage your boat listings, bookings, and payments.
- Dedicated support to assist you with any questions or concerns.

We believe that your boats will add a valuable dimension to the experiences we offer, and we're excited to showcase them to our customers.

Please don't hesitate to reach out if you have any questions or need assistance with your listings. Your satisfaction and success as a boat owner on WaterSide are our top priorities.

Once again, thank you for choosing WaterSide. We're looking forward to a fruitful partnership and to making boat rentals a rewarding venture for you.

Wishing you smooth sailing and prosperous rentals ahead!

Warm regards,

Aakash Mahindreker
Chief Executive Officer
WaterSide: Boat Rental Service
+1(214)218-6979
"""

    elif what == "login":
        subject = "Thank You for Registering with WaterSide: Boat Rental Service"
        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime("%m-%d-%Y %I:%M:%S %p")
        location = geoip.get_location()
        current_location = ""
        for category in location:
            current_location+="\n"+str(category)+": "+str(location[category])
        message = f'''
Dear User,

We hope this message finds you well. We are writing to inform you about recent account activity on your WaterSide: Boat Rental Service account. Your security and privacy are of utmost importance to us, and we want to keep you informed about any account access.

Date and Time of Login: '''+str(current_datetime)+'''
Location of Login: '''+str(current_location)+'''

If you recognize this login activity, you can disregard this email. However, if you did not initiate this login or believe it is unauthorized, please take the following actions:

1. Change Your Password: We recommend changing your account password immediately to secure your account. Please contact us for changing the password.

2. Review Your Account: Check your account for any unusual or unauthorized changes, such as bookings, listings, or personal information.

3. Contact Support: If you have concerns or need assistance, please reach out to our support team at [Support Email Address] or [Support Phone Number].

We take the security of your account very seriously and have implemented measures to protect your data. If you have any security-related questions or need further assistance, please do not hesitate to reach out to us.

Thank you for being a valued member of WaterSide. We are committed to providing a safe and enjoyable boating experience for you.

Warm regards,

Aakash Mahindreker
Chief Executive Officer
WaterSide: Boat Rental Service
+1(214)218-6979



'''
    elif what == "details":
        subject = "Account Details Successfully Changed"
        message = '''
Dear [User's Name],

I hope this email finds you in good health. We wanted to inform you that the recent changes to your account have been processed successfully. Below are the updated details:

Username: [YourUsername]
Email Address: [YourEmailAddress]
If you did not initiate these changes or have any concerns about the security of your account, please contact our support team immediately at [YourSupportEmail] or [YourSupportPhone]. We take the security of your account seriously and will investigate any discrepancies promptly.

Thank you for choosing [YourCompany]. If you have any questions or need further assistance, feel free to reach out to our support team.

Best regards,

Aakash Mahindreker
Chief Executive Officer
WaterSide: Boat Rental Service
+1(214)218-6979
'''
    else :
        subject = "Your Account Credentials"

        message = f'''Dear User,

I hope this message finds you well. We are pleased to inform you that your account has been successfully created, and you can now access our services using the following credentials:

Username: {to}
Password: {str(what[1])}

If you encounter any issues or have questions regarding your account, feel free to reach out to us.

Thank you for choosing WaterSide: Boat Rental Service. We look forward to providing you with a seamless and enjoyable experience.

Best regards,

Aakash Mahindreker
Chief Executive Officer
WaterSide: Boat Rental Service
+1(214)218-6979



'''
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server (Gmail in this case)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS encryption

        # Login to your Gmail account
        server.login(sender_email, "jkif uusc ywcd gdio")  # Replace "YourPassword" with your actual Gmail password

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Quit the server
        server.quit()
        return True
    except smtplib.SMTPException:
        return False
