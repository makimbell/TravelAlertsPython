import imaplib
import email
import re
import time
import html
import datetime
from email.header import decode_header
import config
import socket
import os.path
import sys
import struct
import fcntl
import os
import time
import liquidcrystal_i2c

last_fetched_time = datetime.datetime.now() - datetime.timedelta(days=5)
server = 'imap.gmail.com'

def fetch_mail():
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL(server)
    imap_server.login(config.EMAIL_ADDRESS, config.PASSWORD)

    # Select the mailbox
    imap_server.select('Inbox')

    # Search for all messages in the mailbox (when you figure out how this works, find only correct subject line)
    search_criteria = 'ALL'
    result, message_ids = imap_server.search(None, search_criteria)

    # Get the most recent message ID with the specified subject line
    for message_id in message_ids[0].split()[::-1]:
        result, message_data = imap_server.fetch(message_id, '(RFC822)')
        message = email.message_from_bytes(message_data[0][1])
        subject = decode_header(message['Subject'])[0][0]
        if "THIS WEEK'S TOP 20" in subject.upper():
            target_message_body = message.get_payload(decode=True).decode('utf-8')
            break

    # Close the mailbox and logout
    imap_server.close()
    imap_server.logout()

    return target_message_body

def filter_matches():
    # Use regex to find the deals that are formatted like we expect
    pattern = r'\$.+?(?=\s<)'
    matches = re.findall(pattern, message_body)

    filtered_matches = []

    for match in matches:
        if '--' in match:
            filtered_matches.append(html.unescape(match))

    return filtered_matches

def display_deal_list(deal_list):
    for deal in deal_list:
        if config.DEBUG:
            print(deal)
        time.sleep(config.DISPLAY_TIMER_SECONDS)


while True:

    if datetime.datetime.now() - last_fetched_time > datetime.timedelta(days=1):
        if config.DEBUG:
            print("Fetching mail")
        message_body = fetch_mail()
        last_fetched_time = datetime.datetime.now()
    else:
        if config.DEBUG:
            print("Skipping mail fetch because mail was fetched within 1 day")

    filtered_matches = filter_matches()

    display_deal_list(filtered_matches)