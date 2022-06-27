from cgitb import reset
from pickle import TRUE
import argparse
from pydoc import classname
import imutils
import glob

from variables import cv2,device,time,os,pytesseract,msconfig,Output,readJson
import keyboard

pokemonListClick = ['input tap 75 240']
selfClick = 'input tap 525 1260'

isInEncounter = False
nearbyRadarFound = False
def CheckRadarAvailable():
   

    img = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(img)
    img = cv2.imread('screen.png')      
    f.close()
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_data(invert, lang='eng', config=msconfig, output_type=Output.DICT)
    isInMenu = False
    words = []
    for i in data['text']:
        for j in readJson.dataMenu:
            if i == j:
                isInMenu = True
                words.append(j)
    if isInMenu == True:
        print('Found words:', words, 'application is in menu, checking if nearby radar is ready and exiting.')
        device.shell(f'input tap 560 1760')
        time.sleep(1)
    img = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(img)
    image= cv2.imread('screen.png')

    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    template= cv2.imread('menu_icons/nearbyradar.png',0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    result= cv2.matchTemplate(invert, template, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

    height, width= template.shape[:2]

    top_left= maxLoc
    bottom_right= (top_left[0] + width, top_left[1] + height)

    mid = ((top_left[0]+bottom_right[0])/2,(top_left[1]+bottom_right[1])/2)
    cv2.rectangle(image, top_left, bottom_right, (0,0,255),5)
    if maxVal > 0.7:
        nearbyRadarFound = True
        text1 = 'input swipe'
        text2 = str(mid[0])
        text3 = str(mid[1])
        text4 = '30 130 1000'
        nearbyRadarPos = " ".join((text1, text2,text3,text4))
        time.sleep(2)
        device.shell(nearbyRadarPos)
    else:
        nearbyRadarFound = False
    

    
    return nearbyRadarFound

def PokemonClick():
    device.shell(pokemonListClick[0])
    print('Clicking on Pokemon in Nearby Radar')
    time.sleep(5)
    print('Clicking on Character')
    device.shell(selfClick)
    time.sleep(5)

def CheckIfEncounter():
    img = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(img)
    image= cv2.imread('screen.png')

    gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template= cv2.imread('menu_icons/ARSymbol.png',0)
    template2= cv2.imread('menu_icons/ARSymbolDay.png',0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    result= cv2.matchTemplate(invert, template, cv2.TM_CCOEFF_NORMED)
    result2= cv2.matchTemplate(invert, template2, cv2.TM_CCOEFF_NORMED)

    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    (_, maxVal2, _, maxLoc2) = cv2.minMaxLoc(result2)


    if maxVal > 0.70 or maxVal2 > 0.70:
        isInEncounter = True
    else:
        isInEncounter = False
    
    return isInEncounter