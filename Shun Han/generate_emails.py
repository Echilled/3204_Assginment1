# This script is used to generate "normal" email traffic on the mail server

import os
import sys
import smtplib
import datetime
import random
from datetime import timedelta
import email

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

fromAddresses = (
    "adam@example.com",
    "test@test.com",
    "test@gmail.com",
    "fabio@yahoo.com",
)

toAddresses = (
    "admin@example.com",
    "test@example.com"
)

DATE_FORMAT_1 = "%a, %d %b %Y %H:%M:%S -0700 (UTC)"
DATE_FORMAT_2 = "%d %b %Y %H:%M:%S -0800"
DATE_FORMAT_3 = "%-d %b %Y %H:%M:%S -0800"
DATE_FORMAT_4 = "%a, %d %b %Y %H:%M:%S -0700"
DATE_FORMAT_5 = "%a, %d %b %Y %H:%M:%S -0700 UTC"
DATE_FORMAT_6 = "%a, %-d %b %Y %H:%M:%S -0700 (UTC)"
DATE_FORMAT_7 = "%a, %-d %b %Y %H:%M:%S -0700"

useSSL = False
address = "192.168.91.5"
smtpPort = 25


def makeHTMLMessage(subject, date, dateFormat, body):
    msg = MIMEMultipart()
    html = MIMEText(body, "html")

    msg["Subject"] = subject
    msg["From"] = getRandomFrom()
    msg["To"] = getRandomTo()
    msg["Date"] = date.strftime(dateFormat)

    msg.attach(html)
    return msg


def makeTextMessage(subject, date, dateFormat, body, multipart=False):
    if multipart:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body))
    else:
        msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = getRandomFrom()
    msg["To"] = getRandomTo()
    msg["Date"] = date.strftime(dateFormat)

    return msg
    
def makeTextMessage2(subject, sender, recipient, date, dateFormat, body, multipart=False):
    if multipart:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body))
    else:
        msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg["Date"] = date.strftime(dateFormat)

    return msg


def makeMultipartMessage(subject, date, dateFormat, textBody, htmlBody):
    msg = MIMEMultipart()
    html = MIMEText(htmlBody, "html")
    text = MIMEText(textBody)

    msg["Subject"] = subject
    msg["From"] = getRandomFrom()
    msg["To"] = getRandomTo()
    msg["Date"] = date.strftime(dateFormat)

    msg.attach(text)
    msg.attach(html)
    return msg


def addAttachment(subject, filename, contentType, sender, recepient, base64Encode=True):
    msg = MIMEMultipart()

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recepient
    msg["Date"] = datetime.datetime.now().strftime(DATE_FORMAT_1)

    contentTypeSplit = contentType.split("/")

    part = MIMEBase(contentTypeSplit[0], contentTypeSplit[1])
    part.set_payload(open(filename, "rb").read())
    email.encoders.encode_base64(part)
    #part.add_header("Content-Type", contentType)
    part.add_header("Content-Disposition",
                    "attachment; filename=\"{0}\"".format(os.path.basename(filename)))

    msg.attach(part)
    return msg


def getRandomFrom():
    return fromAddresses[random.randint(0, len(fromAddresses) - 1)]


def getRandomTo():
    return toAddresses[random.randint(0, len(toAddresses) - 1)]


def sendMail(msg):
    if not useSSL:
        server = smtplib.SMTP("{0}:{1}".format(address, smtpPort))
    else:
        server = smtplib.SMTP_SSL("{0}:{1}".format(address, smtpPort))

    fromAddress = msg["From"]
    to = [msg["To"]]

    server.sendmail(fromAddress, to, msg.as_string())
    server.quit()

#
# Seed the random generator
#
def main():
    random.seed(datetime.datetime.now().timestamp())

    choice = [makeHTMLMessage(
            "Weird TO Address",
            datetime.datetime.now(),
            DATE_FORMAT_1,
            "<p>This is an email sent to an address with 'data' in the TO field.</p>"
        ), makeTextMessage(
            "Plain Text Email",
            datetime.datetime.now(),
            DATE_FORMAT_1,
            "This is a plain text email.\n\nSincerely,\nAdam Presley"
        ), makeTextMessage(
            "Plain Text Email with special characters (á, é, í, ó, ú)",
            datetime.datetime.now(),
            DATE_FORMAT_1,
            "This is a plain text email with special characters in the subject.\n(á, é, í, ó, ú)\n\nSincerely,\nAdam Presley"
        )]

    try:
        print(len(sys.argv))
        if len(sys.argv) == 2 and sys.argv[1].isnumeric():
            for _ in range(int(sys.argv[1])):
                msg = random.choice(choice)
                sendMail(msg)    
        elif len(sys.argv) == 3:
            msg = makeTextMessage2(
            "Plain Text Email", sys.argv[1], sys.argv[2], 
            datetime.datetime.now(),
            DATE_FORMAT_1,
            "This is a plain text email.\n\nSincerely,\nAdam Presley")
            sendMail(msg)
        elif len(sys.argv) == 6:
            new_msg = addAttachment(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            sendMail(new_msg)
        else:
            msg = random.choice(choice)

            sendMail(msg)
      

    except Exception as e:
        print(f"An error occurred while trying to connect and send the email: {e}")
        print(sys.exc_info())

if __name__ == "__main__":
    main()