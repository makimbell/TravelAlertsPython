import imaplib
import email
import re
import time
import html
import datetime
import http.client as httplib
from email.header import decode_header
import config
if config.DEVICE_CONNECTED:
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
        subject = decode_header(message['Subject']).__str__().upper()
        if "TOP 20" in subject.upper():
            target_message_body = message.get_payload(
                decode=True).decode('utf-8')
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
        if "—" in match:
            match = match.replace('—', ' -- ')
            filtered_matches.append(html.unescape(match))

    return filtered_matches

def display_deal_list(deal_list):
    for deal in deal_list:
        if config.DEBUG:
            print(deal)
        if config.DEVICE_CONNECTED:
            cols = 20
            rows = 4

            currentRow = 1
            row1 = ""
            row2 = ""
            row3 = ""
            row4 = ""

            dealWords = deal.split()
            for word in dealWords:
                if currentRow == 1:
                    if len(row1) + len(word) < cols:
                        row1 = row1 + word + " "
                    else:
                        currentRow += 1
                if currentRow == 2:
                    if len(row2) + len(word) < cols:
                        row2 = row2 + word + " "
                    else:
                        currentRow += 1
                if currentRow == 3:
                    if len(row3) + len(word) < cols:
                        row3 = row3 + word + " "
                    else:
                        currentRow += 1
                if currentRow == 4:
                    if len(row4) + len(word) < cols:
                        row4 = row4 + word + " "
                    else:
                        currentRow += 1
                
            lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)
            lcd.clear()
            lcd.printline(0, row1)
            lcd.printline(1, row2)
            lcd.printline(2, row3)
            lcd.printline(3, row4)
        time.sleep(config.DISPLAY_TIMER_SECONDS)

def checkInternetConnection(url="www.google.com", timeout=3):
    connection = httplib.HTTPConnection(url, timeout=timeout)

    try:
        connection.request("HEAD", "/")
        connection.close()
        return True
    except:
        return False

if checkInternetConnection():
    if config.DEBUG:
        print("Internet Connected")
    if config.DEVICE_CONNECTED:
        lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
        lcd.clear()
        lcd.printline(0, "Internet Connected")
    
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
else:
    if config.DEBUG:
        print("No internet")
    if config.DEVICE_CONNECTED:
        lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
        lcd.clear()
        lcd.printline(0, "No internet")
        lcd.printline(1, "Tell Andy")