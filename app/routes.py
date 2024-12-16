import os
from flask import Flask, render_template, request, flash, redirect, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_mail import Mail, Message
import smtplib

from app import app


# Initialize Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'panditayush498@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'wzje vvmh ybpa theq'  # Replace with your app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'panditayush498@gmail.com'  # Replace with your email

mail = Mail(app)


@app.route('/')
def home():
    portraits = os.listdir('app/static/portraits')
    return render_template('home.html', portraits=portraits)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


@app.route('/artist')
def artist():
    return render_template('about_artist.html')

@app.route('/developer')
def developer():
    return render_template('about_developer.html')

@app.route('/book_order', methods=['GET', 'POST'])
def book_order():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        description = request.form['description']
        portrait_type = request.form['portrait_type']
        photo = request.files['photo']
        payment_screenshot = request.files.get('payment_screenshot')  # Optional
        payment=["NO"]

        
        # Save the uploaded files
        photo_filename = os.path.join('app/temp', photo.filename)
        photo.save(photo_filename)
        
        payment_screenshot_filename = None
        if payment_screenshot:
            payment_screenshot_filename = os.path.join('app/temp', payment_screenshot.filename)
            payment[0]="Yes"
            payment_screenshot.save(payment_screenshot_filename)

        # Prepare email message
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']  # Your email (sender)
        msg['To'] = 'babitasharmaadvocate444@gmail.com'  # Recipient's email
        msg['Subject'] = f'New Portrait Booking Request from {name}'
        
        body = f"""
        Name: {name}
        Phone: {phone}
        Email: {email}
        Description: {description}
        portrait_type: {portrait_type}
        Payment Made: {payment[0]}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach the photo
        with open(photo_filename, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={photo.filename}')
            msg.attach(part)
        
        # Attach the payment screenshot if available
        if payment_screenshot_filename:
            with open(payment_screenshot_filename, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={payment_screenshot.filename}')
                msg.attach(part)

        # Send the email
        try:
            with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                server.sendmail(app.config['MAIL_USERNAME'], 'babitasharmaadvocate444@gmail.com', msg.as_string())  # Send to this email
            flash('Your portrait booking request has been sent successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error sending email!', 'danger')
            return redirect(url_for('book_order'))
    
    return render_template('book_order.html')