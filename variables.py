from asyncio.windows_events import NULL
from contextlib import nullcontext
from ppadb.client import Client
import time
import os
import re
import cv2
#import divimage
from PIL import Image
import numpy as np
import atexit
import pyautogui as pg
import pytesseract
from pytesseract import Output
import yaml
import readJson
import random



adb = Client(host='localhost', port=5037)
pytesseract.pytesseract.tesseract_cmd = r'tesseract/tesseract.exe'
os.system('adb start-server')

config = yaml.safe_load(open("config.yml"))

msconfig= r"--psm 11 --oem 3"
cascade_pokestop = cv2.CascadeClassifier('cascade/cascade.xml')

devices = adb.devices()
device = devices[0]
