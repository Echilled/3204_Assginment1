import requests
import json
import pandas as pd

# Change IP address of Mail server
r = requests.get("http://192.168.1.181:8025/api/v2/messages")
data = json.loads(r.text)["items"]
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

results = []

for row in data:
    content = row["Content"]
    mime = row["MIME"]
    if mime is None:
        mime = dict()
    results.append(content | mime)

df = pd.DataFrame(results)

# ID, Date Created, Sender, Recipient, Subject, Body, File name, File type, File size, Email size
try:
    # ID
    df["Headers"] = df["Headers"].astype(str)
    df["Message-ID"] = df["Headers"].str.extract("('Message-ID':\s\['\S*\'])")
    df["Message-ID"] = df["Message-ID"].str.extract("(\['.+'\])")
    df["Message-ID"] = df["Message-ID"].str.replace(r"([\['\]])", '', regex=True)

    # Date Created
    df["Date"] = df["Headers"].str.extract("('Date':\s\['[\s,:\w\(\)-]*'\])")
    df["Date"] = df["Date"].str.extract("(\['.+'\])")
    df["Date"] = df["Date"].str.replace(r"([\['\]-])", '', regex=True)

    # Sender
    df["Sender"] = df["Headers"].str.extract("('From': \['[\w@\.]+'\])")
    df["Sender"] = df["Sender"].str.extract("(\['[\w@\.]+'\])")
    df["Sender"] = df["Sender"].str.replace(r"[\[\]']", '', regex=True)

    # Recipient
    df["Recipient"] = df["Headers"].str.extract("('To': \['[\w@\.]+'\])")
    df["Recipient"] = df["Recipient"].str.extract("(\['[\w@\.]+'\])")
    df["Recipient"] = df["Recipient"].str.replace(r"[\[\]']", '', regex=True)

    # Subject
    df["Subject"] = df["Headers"].str.extract("('Subject': \['[\w\?\s=\-]+'\])")
    df["Subject"] = df["Subject"].str.extract("(\['[\w\?\s=\-]+'\])")
    df["Subject"] = df["Subject"].str.replace(r"[\[\]']", '', regex=True)

    # Email Body
    df["Email body"] = df["Body"]

    # File name
    df["Parts"] = df["Parts"].astype(str)
    df["Attachment"] = df["Parts"].str.extract("(\['attachment; filename=\"[\w\.]*\"'\])")
    df["Attachment"] = df["Attachment"].str.extract("(=\"[\w\.]*\")")
    df["Attachment"] = df["Attachment"].str.replace(r"([=\"]*)", '', regex=True)

    # File type
    df["File type"] = df["Parts"].str.extract("('Content-Type': \['[\w\/\-]+'\])")
    df["File type"] = df["File type"].str.extract("(\['[\w\/\-]+'\])")
    df["File type"] = df["File type"].str.replace(r"([\[\]'])", '', regex=True)

    # File size
    df["File size"] = df["Parts"].str.extract("('Size': \d+)")
    df["File size"] = df["File size"].str.extract("(\d+)")

    # Email size
    df["Email size"] = df["Size"]

    df = df[["Message-ID", "Date", "Sender", "Recipient", "Subject", "Email body", "Attachment", "File type", "File size", "Email size"]]
    df.columns = ['ID', 'Date Created', 'Sender', 'Recipient', 'Subject', 'Email Body', 'File name', 'File type', 'File size', 'Email Size']

    df.to_csv("out.csv")


except KeyError:
    pass