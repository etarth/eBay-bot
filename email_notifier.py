# email_notifier.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, RECEIVER_EMAIL

def send_email_notification(items):
    subject = f"[eBay Alert] {len(items)} New Item(s) Found"

    html_body = "<h2>🛎️ New eBay Listings:</h2><ul>"
    for item in items:
        html_body += f"<li><b>{item['title']}</b> - ${item['price']}<br><a href='{item['url']}'>View on eBay</a></li><br>"
    html_body += "</ul>"

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email with links sent successfully!")
    except Exception as e:
        print(f"[Email Error] {e}")
