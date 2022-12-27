# NEED TO INCLUDE BUT I DON'T THINK IM GOING TO USE IT\

from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText


def send_email(email, one_time_password):

    email_sender = "mansuracorp@gmail.com"
    password = 'gdsaqlhggkishjng'
    reciver = email

    subject = "Forgot Password Recovery"
    msg = MIMEText(f'''
    <a href="https://mansura.ca/password_reset">Reset Password</a>

    One Time Password:{one_time_password}
    ''', 'html')
    em = EmailMessage()

    #TODO: UPDATE USER DATABASE WITH A [RNG] RECOVERY NUM, CAN BE A SEPARATE TABLE
    # THEN TO MAKE THE SITE EXCLUSIVE, MAKE THE USER ENTER THE NUM WITH THE INFO

    
    em['From'] = email_sender
    em["To"] = reciver
    em['Subject'] = subject
    em.set_content(msg)

    context = ssl.create_default_context()
    # EMAIL SERVER
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, reciver, em.as_string())
    print("SENT EMAIL", email)

# send_email("foreandr@gmail.com")