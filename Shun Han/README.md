# Requirements for ELK

```sysctl -w vm.max_map_count=262144```

May need to allow ports 9200, 5601 and 5044 if unable to access ELK services

## generate_emails.py usage
```
python3 generate_emails.py <integer> # Sends x amount of emails to the mail server
python3 generate_emails.py <subject> <attachment name> <content type> <sender email> <recepient email>
```