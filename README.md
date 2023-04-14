# TravelAlertsPython
Test for IMAP client and reading and parsing emails

Project for pulling in latest TravelZoo This Week's Top 20 email from an email account and displaying it. This may eventually become a hardware project, where the output is displayed on a Raspberry Pi LED screen or something.

To make the project work, you need a config.py file in the directory of the project, which should look like this:

#### config.py:
```
EMAIL_ADDRESS = "[email]"
PASSWORD = "[password]"
DEBUG = True
DISPLAY_TIMER_SECONDS = 5
DEVICE_CONNECTED = False
```
