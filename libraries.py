
import os
from os import system
import signal
from urllib.parse import quote
import csv
import json
from time import sleep
from colors import *
from linkedIn_scraper import *
import platform

from linkedIn_scraper import logo

logo()

#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Installing Libraries" + W + ' - ' + R + "[]" + W, end="\r")
my_os = platform.system()
if "Darwin" in my_os:
    system("pip3 install -r requirements.txt > /dev/null 2>&1")
if "Linux" in my_os:
    system("pip3 install -r requirements.txt > /dev/null 2>&1")
if "Windows" in my_os:
    system("py -m pip3 install -r requirements.txt >nul")

print(O + "[" + C + "*" + O + "] " + C +
          "Installing Libraries" + W + ' - ' + G + "[OK]")
print("")
print(O + "[" + C + "*" + O + "] " + G +
      "Importing Libraries" + W)
print("")

#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Selenium Webdriver" + W + ' - ' + R + "[]" + W, end="\r")
try:
    from selenium import webdriver as uc
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Selenium Webdriver Common" + W + ' - ' + R + "[]" + W, end="\r")
try:
    from selenium.webdriver.common.by import By
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Common" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Common" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Selenium Webdriver Manager" + W + ' - ' + R + "[]" + W, end="\r")
try:
    from webdriver_manager.chrome import ChromeDriverManager
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Manager" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Manager" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Selenium Webdriver Service" + W + ' - ' + R + "[]" + W, end="\r")
try:
    from selenium.webdriver.chrome.service import Service
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Service" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Service" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Selenium Webdriver Options" + W + ' - ' + R + "[]" + W, end="\r")
try:
    from selenium.webdriver.chrome.options import Options
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Options" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Selenium Webdriver Options" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Requests" + W + ' - ' + R + "[]" + W, end="\r")
try:
    import requests
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Requests" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Requests" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#

print(O + "[" + C + "*" + O + "] " + C +
      "Importing Re" + W + ' - ' + R + "[]" + W, end="\r")
try:
    import re
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Re" + W + ' - ' + G + "[OK]")
except ImportError:
    print(O + "[" + C + "*" + O + "] " + C +
          "Importing Re" + W + ' - ' + R + "[ERROR]")
    exit()

# Sleeping
sleep(0.5)
#========================================================================================#
print("")
print(O + "[" + C + "*" + O + "] " + G +
      "All Libraries have been Imported" + W)

# Sleeping
sleep(2)
