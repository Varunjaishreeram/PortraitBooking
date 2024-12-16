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

        # Prepare email message
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']  # Your email (sender)
        msg['To'] = 'panditayush498@gmail.com'  # Recipient's email
        msg['Subject'] = f'New Portrait Booking Request from {name}'

        body = f"""
        Name: {name}
        Phone: {phone}
        Email: {email}
        Description: {description}
        Portrait Type: {portrait_type}
        Payment Made: {'Yes' if payment_screenshot else 'No'}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach the photo
        photo_data = photo.read()
        photo_part = MIMEBase('application', 'octet-stream')
        photo_part.set_payload(photo_data)
        encoders.encode_base64(photo_part)
        photo_part.add_header('Content-Disposition', f'attachment; filename="{photo.filename}"')
        msg.attach(photo_part)

        # Attach the payment screenshot if available
        if payment_screenshot:
            screenshot_data = payment_screenshot.read()
            screenshot_part = MIMEBase('application', 'octet-stream')
            screenshot_part.set_payload(screenshot_data)
            encoders.encode_base64(screenshot_part)
            screenshot_part.add_header('Content-Disposition', f'attachment; filename="{payment_screenshot.filename}"')
            msg.attach(screenshot_part)

        # Send the email
        try:
            with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                server.sendmail(app.config['MAIL_USERNAME'], 'panditayush498@gmail.com', msg.as_string())
            flash('Your portrait booking request has been sent successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'danger')
            return redirect(url_for('book_order'))

    return render_template('book_order.html')
