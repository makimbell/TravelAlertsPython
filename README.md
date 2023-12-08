# TravelAlertsPython

This project connects to a gmail account, pulls in the latest TravelZoo "This Week's Top 20" email, parses out the list of deals, and displays it. It can run on a Raspberry Pi, and output is configured to display to a 20x4 LCD display like this one: https://amzn.to/41lqyQz.

You need a config.py file in the directory of the project, which should look like this:

#### config.py:
```
EMAIL_ADDRESS = [string]
PASSWORD = [string]
DEBUG = [bool]
DISPLAY_TIMER_SECONDS = [int]
DEVICE_CONNECTED = [bool]
```
Where
* EMAIL_ADDRESS and PASSWORD are the credentials to an email account which is signed up to receive TravelZoo "Top 20" emails.
* DEBUG is a boolean to enable logging
* DISPLAY_TIMER_SECONDS is an int that represents how long each deal should display on the screen
* DEVICE_CONNECTED is a boolean that represents whether or not you have a physical 20x4 LCD hooked up
