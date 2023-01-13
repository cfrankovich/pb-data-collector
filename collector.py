# # # INITIALIZATION # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Imports #
import sys
import time 
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

# Constants #
USERERROR = 1
PROGRAMERROR = 2
EMAILXPATH = '/html/body/div[1]/div[1]/section/div/div/div/div/div/div/form/div[1]/div/div[1]/input' 
PASSWORDXPATH = '/html/body/div[1]/div[1]/section/div/div/div/div/div/div/form/div[2]/div/div/input'
LOGINSUBMITXPATH = '/html/body/div[1]/div[1]/section/div/div/div/div/div/div/div/button'
WILLINGTOTAKERISKSBUTTONXPATH = '/html/body/div[1]/div[1]/div[3]/div/div/div[3]/div/div[2]/div/div[2]/button'

# Program Arguments #
DEBUGFLAG = False
PAGESLEEPTIME = 5
CAPTCHASLEEPTIME = 8

args = sys.argv
for arg in args:
    if (arg == '--debug'):
        DEBUGFLAG = True
    elif arg.__contains__('--page-sleep-time='):
        try:
            PAGESLEEPTIME = int(arg.split('=')[1])
        except:
            print('Please enter a valid argument.\n') 
            print('    --page-sleep-time=[INTEGER]')
            print('\nRefer to the --help document for more.')
            sys.exit(USERERROR)
    elif arg.__contains__('--captcha-sleep-time='):
        try:
            CAPTCHASLEEPTIME = int(arg.split('=')[1])
        except:
            print('Please enter a valid argument.\n') 
            print('    --captcha-sleep-time=[INTEGER]')
            print('\nRefer to the --help document for more.')
            sys.exit(USERERROR)

# Get Links #
linksfilepath = ''
if DEBUGFLAG:
    linksfilepath = 'debug/debuglinks.txt'
else:
    linksfilepath = 'links.txt'

links = []
with open(linksfilepath, 'r') as linksfile:
    links = linksfile.read().split('\n')

if links == ['']:
    print('No links inputed!')
    print('Please input links in links.txt')
    print('Refer to the --help document for more.')
    sys.exit(USERERROR)

# Get PB Keys #
pbkeysfilepath = ''
if DEBUGFLAG:
    pbkeysfilepath = 'debug/debugmodepbkeys.txt'
else:
    pbkeysfilepath = 'YOURPBKEYS.txt'

pbkeys = [] 
with open(pbkeysfilepath, 'r') as pbkeys:
    pbkeys = pbkeys.read().split('\n')

if pbkeys == ['']:
    print('No pb keys inputed!')
    print('Please input keys in YOURPBKEYS.txt')
    print('Refer to the --help document for more.')
    sys.exit(USERERROR)

# Init Driver #
driver = None
try:
    driver = webdriver.Firefox()
except:
    print('Driver did not start!')
    sys.exit(PROGRAMERROR)

# # # STARTING NAVIGATION # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Loop Through Links #
for link in links:
    # Get a Link and Wait For Load #
    driver.get(link)
    time.sleep(PAGESLEEPTIME)

    # Enter Email and Password #
    driver.find_element(By.XPATH, EMAILXPATH).send_keys(pbkeys[0])
    driver.find_element(By.XPATH, PASSWORDXPATH).send_keys(pbkeys[1])

    # Captcha #
    print('Waiting for captcha...')
    time.sleep(CAPTCHASLEEPTIME)
    print('Resuming!')

    # Press Submit #
    driver.find_element(By.XPATH, LOGINSUBMITXPATH).click()

    # Wait for Page Load #
    time.sleep(PAGESLEEPTIME) 

    # Press I Agree If Appear #
    try:
        driver.find_element(By.XPATH, WILLINGTOTAKERISKSBUTTONXPATH).click()
    except:
        pass

    # Get Info #
    print('Info!')






