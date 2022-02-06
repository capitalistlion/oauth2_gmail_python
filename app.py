import requests
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import logging
import json
import os, sys
from urllib.parse import quote, unquote
import base64

# make it log.info to the console.
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
log.setLevel(logging.INFO)

REDIRECT_URI = "--------"
CLIENT_ID = "-----------.apps.googleusercontent.com"
CLIENT_SECRET = "---------------"
OAUTH_SCOPE = "https://www.googleapis.com/auth/gmail.send"
ACCESS_TOKEN = REFRESH_TOKEN = ""

# Paste AUTHORIZATION_CODE from the redirected url after running function getAUTHORIZATION_CODE()
AUTHORIZATION_CODE = ""

def getAUTHORIZATION_CODE():
    payload = "redirect_uri="+str(REDIRECT_URI)+"&scope="+str(OAUTH_SCOPE)+"&prompt=consent&response_type=code&access_type=offline&client_id="+CLIENT_ID
    return "https://accounts.google.com/o/oauth2/v2/auth?"+payload

def getTokens(AUTHORIZATION_CODE):
    payload = "redirect_uri="+str(REDIRECT_URI)+"&code="+str(AUTHORIZATION_CODE)+"&client_secret="+CLIENT_SECRET+"&grant_type=authorization_code&client_id="+CLIENT_ID
    log.info(quote(payload))
    url = "https://oauth2.googleapis.com/token"
    head = {"Content-Type": "application/x-www-form-urlencoded"}
    log.info("payload - "+str(payload))
    response = requests.post(url, headers=head, data=payload)
    log.info("getTokens response - "+str(response))
    log.info("getTokens response.text - "+str(response.text))
    if response.status_code == 200:
        log.info("getTokens response.json()"+str(response.json()))

        # Save ACCESS_TOKEN to your Database
        global ACCESS_TOKEN, REFRESH_TOKEN
        ACCESS_TOKEN = response.json()["access_token"]
        REFRESH_TOKEN = response.json()["refresh_token"]

def is_token_valid(access_token):
    url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+access_token

    response = requests.get(url)
    log.info("is_token_valid response - "+str(response))
    log.info("is_token_valid response.text - "+str(response.text))
    log.info("is_token_valid response.json() - "+str(response.json()))

    if "error" in response.json():
        log.info("is_token_valid - invalid")
        return "invalid"
    else:
        log.info("is_token_valid - valid")
        return "valid"

def refresh_access_token():
    payload = "client_secret="+CLIENT_SECRET+"&grant_type=refresh_token&refresh_token="+REFRESH_TOKEN+"&client_id="+CLIENT_ID

    url = "https://oauth2.googleapis.com/token"
    head = {"Content-Type": "application/x-www-form-urlencoded"}
    log.info("payload - "+str(payload))
    response = requests.post(url, headers=head, data=payload)
    log.info("refresh_access_token response - "+str(response))
    log.info("refresh_access_token response.text - "+str(response.text))
    log.info("refresh_access_token response.json() - "+str(response.json()))

    if "access_token" in response.json():
        new_access_token = response.json()["access_token"]
    else:
        log.info("error")
        return "error"

    # UPDATE DATABASE WITH NEW ACCESS TOKEN

    return new_access_token

# designing your email using HTML
def get_html_content(subject, email_content):
    html_email = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>"""+str(subject)+"""</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <!-- styles -->
        <link href="https://getbootstrap.com/2.3.2/assets/css/bootstrap.css" rel="stylesheet">
        <style>
        body {
            padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
        }
        </style>
        <link href="https://getbootstrap.com/2.3.2/assets/css/bootstrap-responsive.css" rel="stylesheet">

    </head>
    <body>
        <div class="container">

        <h1>"""+str(subject)+"""</h1>
        <p>"""+str(email_content)+"""</p>

        </div> <!-- /container -->
    </body>
    </html>
    """
    return html_email

def compose_email(receiver_email, subject, email_content, cc_emails):
    html_email = get_html_content(subject, email_content)
    log.info("html content generated")
    EMAIL_FROM = "youremail@gmail.com"

    msg_html_content = MIMEText(html_email, "html", "utf-8")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject, "utf-8").encode()
    msg["From"] = "TestName <"+EMAIL_FROM+">" # You can replace where EMAIL_FROM is supposed to be with a custom domain if you"ve linked it to your mail provider and confirmed it
    msg["To"] = receiver_email
    msg["CC"] = ",".join(cc_emails)
    msg.attach(msg_html_content)

    # Get ACCESS_TOKEN from your Database
    global ACCESS_TOKEN
    status = is_token_valid(ACCESS_TOKEN)
    log.info("ACCESS_TOKEN status - "+str(status))
    if status == "invalid":
        ACCESS_TOKEN = refresh_access_token()

    Authorization = "Bearer "+ACCESS_TOKEN
    head = {"Content-Type": "application/json", "Authorization": Authorization}
    log.info("compose head - "+str(head))
    body = {"raw": base64.urlsafe_b64encode(msg.as_string().encode("utf-8")).decode("utf-8")}

    return head, body

def sendEmail(receiver_email, cc_emails, subject, email_content):
    payload = compose_email(receiver_email, subject, email_content, cc_emails)

    url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"
    response = requests.post(url, headers=payload[0], data=json.dumps(payload[1]))
    log.info("sendEmail response - "+str(response))
    log.info("sendEmail response.text - "+str(response.text))
    log.info("sendEmail response.json() - "+str(response.json()))
    if "labelIds" in response.json():
        if "SENT" in response.json()["labelIds"]:
            return "success"

    return "error"

choice = int(input("""
Select an option

1. Generate Authorization Code
2. Generate Tokens
3. Send Email

"""))

def sendmail():
    receiver_email = input("""Email to send to: """)
    
    response = sendEmail(receiver_email, [], "Testing Function", "Hi there. it works!")
    log.info("response - "+str(response))

if choice == 1:
    authcodeurl = getAUTHORIZATION_CODE()
    if sys.platform=="win32":
        os.startfile(authcodeurl)
    elif sys.platform=="darwin":
        subprocess.Popen(["open", authcodeurl])
    else:
        try:
            subprocess.Popen(["xdg-open", authcodeurl])
        except OSError:
            log.info("Please open a browser on: "+authcodeurl)

elif choice == 2:
    getTokens(AUTHORIZATION_CODE)

    log.info("---------------------")
    choice = input("""Do you want to send an email now? (Y/N): """)

    if choice.lower() == "y":
        sendmail()

elif choice == 3:
    sendmail()
