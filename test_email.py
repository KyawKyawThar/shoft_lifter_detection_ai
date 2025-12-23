import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Test email credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = "kyawkyaw.thar84@gmail.com"
sender_password = "uvgzlmaaxbjdcoxw"
recipient_email = 'kyawkyaw.thar14@gmail.com'

print("Testing Gmail SMTP connection...")
try:
    print(f"Connecting to {smtp_server}:{smtp_port}...")
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
    server.set_debuglevel(1)  # Enable debug output
    
    print("\nStarting TLS...")
    server.starttls()
    
    print("\nLogging in...")
    server.login(sender_email, sender_password)
    print("✓ Authentication successful!")
    
    # Send test email
    msg = MIMEMultipart('alternative')
    msg['From'] = f"shoft_lifting_detection <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = "Test Email - Shoplifting Detection System"
    msg.attach(MIMEText("This is a test email from the shoplifting detection system.", 'plain'))
    
    print("\nSending test email...")
    server.send_message(msg)
    print("✓ Test email sent successfully!")
    
    server.quit()
    print("✓ Connection closed\n✅ All systems ready!")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ Authentication Failed: {e}")
    print("→ Check if app password is correct")
    
except smtplib.SMTPServerDisconnected as e:
    print(f"\n✗ Server disconnected: {e}")
    print("→ This usually means authentication failed")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
