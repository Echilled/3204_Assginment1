from math import nan
import requests
import json
import pandas as pd

# Change request IP to mail server IP address
r = requests.get("http://192.168.1.108:8025/api/v2/messages")
data = json.loads(r.text)['items']

pd.options.display.max_columns = None
df = pd.json_normalize(data)

df = df[['ID', 'Content.Headers.Date', 'Content.Headers.From', 'Content.Headers.To', 'Content.Headers.Subject', 'Content.Body', 'MIME.Parts', 'MIME.Parts', 'MIME.Parts', 'Content.Size']]
df.columns = ['ID', 'Date Created', 'Sender', 'Recipient', 'Subject', 'Body', 'File name', 'File type', 'File size', 'Email Size']
df['Date Created'] = df['Date Created'].str[0]
df['Sender'] = df['Sender'].str[0]
df['Recipient'] = df['Recipient'].str[0]
df['Subject'] = df['Subject'].str[0]

# df['File name'] = ''.join(df['File name'][0][0]['Headers']['Content-Disposition']).split('filename=')[1].replace('"', '')
# print(len(df['File name']))

# df['File name'] = df['File name'][0][0]['Headers']['Content-Disposition']
# df['File type'] = df['File type'][0][0]['Headers']['Content-Type']
# df['File size'] = df['File size'][0][0]['Size']

df.to_csv('out.csv')