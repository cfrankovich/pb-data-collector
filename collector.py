# # # INITIALIZATION # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Imports #
import sys
import time 
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

# https://www.pandabuy.com/product?ra=772&url=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fid%3D601082922962&inviteCode=7WYA7LL7F
#https://www.pandabuy.com/product?url=https%3A%2F%2Fweidian.com%2Fitem.html%3FitemID%3D2595078898&spider_token=4572

# Constants #
USERERROR = 1
PROGRAMERROR = 2
xpaths = {
    'email' :'/html/body/div[1]/div[1]/section/div/div/div/div/div/div/form/div[1]/div/div[1]/input', 
    'password' : '/html/body/div[1]/div[1]/section/div/div/div/div/div/div/form/div[2]/div/div/input',
    'submitbtn' : '/html/body/div[1]/div[1]/section/div/div/div/div/div/div/div/button',
    'acceptriskbtn' : '/html/body/div[1]/div[1]/div[3]/div/div/div[3]/div/div[2]/div/div[2]/button',
    'price' : '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[2]/div[3]/div[1]/div/span/div[2]/span[1]',
    'name' : '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[2]/div[2]/span[1]',
    'sizesdiv' : '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]',
    'colorsdiv' : '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]',
    'picsdiv' : '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/ol'
}

# Program Arguments #
DEBUGFLAG = False
PAGESLEEPTIME = 3
CAPTCHASLEEPTIME = 5

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

print('- PandaBuy Data Collector -')

# # # STARTING NAVIGATION # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Loop Through Links #
linkcounter = 1

for link in links:
    # Get a Link and Wait For Load #
    driver.get(link)
    time.sleep(PAGESLEEPTIME)
    print(f'\n[=] Accessing Item #{linkcounter}')
    linkcounter += 1

    # If Asked to Login #
    try:
        print('[-] Login Requested...')

        for timeleft in range(CAPTCHASLEEPTIME, -1, -1):
            print(f'Please enter captcha. Continuing in {timeleft}')
            sys.stdout.write("\033[F")
            time.sleep(1)

        print('\nResuming...')

        driver.find_element(By.XPATH, xpaths['email']).send_keys(pbkeys[0])
        driver.find_element(By.XPATH, xpaths['password']).send_keys(pbkeys[1])

        driver.find_element(By.XPATH, xpaths['submitbtn']).click()
        print('[+] Successfully Logged In')
        time.sleep(PAGESLEEPTIME)
    except:
        pass

    time.sleep(PAGESLEEPTIME)

    # Get Info #
    itemlink = link

    itembaseprice = float(driver.find_element(By.XPATH, xpaths['price']).text.split()[2])

    itemsizes = []
    xpathstring = xpaths['sizesdiv']
    sizecounter = 1
    while True:
        sizexpath = xpathstring + f'/li[{sizecounter}]/span'
        try:
            newsize = driver.find_element(By.XPATH, sizexpath).text 
            itemsizes.append(newsize)
        except:
            break
        sizecounter += 1
    itemsizes.pop(-1)

    itemcolors = []
    xpathstring = xpaths['colorsdiv']
    colorscounter = 1
    while True:
        colorxpath = xpathstring + f'/li[{colorscounter}]/img'
        try:
            newcolor = driver.find_element(By.XPATH, colorxpath).get_attribute('title')
            itemcolors.append(newcolor)
        except:
            break
        colorscounter += 1

    itempicturelinks = []
    xpathstring = xpaths['picsdiv']
    picscounter = 1
    while True:
        picxpath = xpathstring + f'/li[{picscounter}]/img'
        try:
            newpic = driver.find_element(By.XPATH, picxpath).get_attribute('src')
            itempicturelinks.append(newpic)
        except:
            break
        picscounter += 1

    print('[+] Item Data Collected')
