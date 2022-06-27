from variables import random,device, devices,os,cv2,pytesseract,msconfig, Output, np,time,cascade_pokestop
from catchPokemon import TakeScreen, OnlyScreen
from vision import draw_rectangles

spinStop = 'input swipe 300 980 820 980 500'
exitScreen = 'input tap 545 1794'
def SearchStops():
    image = TakeScreen()
    y=880
    x=150
    h=800
    w=800
    image[0] = image[0][y:y+h, x:x+w]
    rectangles = cascade_pokestop.detectMultiScale(image[0])
    top,bot = draw_rectangles(image[0], rectangles)
    if not top:
        return False
    else:
        mid = ((top[0][0]+bot[0][0])/2,(top[0][1]+bot[0][1])/2)
        text1 = 'input tap'
        text2 = str(mid[0])
        text3 = str(mid[1])
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4
        final = " ".join((text1, text2,text3))
        print(mid[0],mid[1])
        device.shell(final)
        return True

def CheckStopUsed():
    imageOfStop = TakeScreen()
    colorOfStop = (imageOfStop[0][1845,135][0],imageOfStop[0][1845,135][1],imageOfStop[0][1845,135][2])
    if (200 <= colorOfStop[0] <= 255) and (100<=colorOfStop[1]<=255) and (20<=colorOfStop[2]<=50):
        return False
    else:
        if (195 <= colorOfStop[0] <= 250) and (60<=colorOfStop[1]<=110) and (60<=colorOfStop[2]<=110):
            return True
        else:
            return True

def SpinStop():
    device.shell(spinStop)

def ExitStopScreen():
    device.shell(exitScreen)

def TapSomewhereRandom():
    randomX = random.randint(320,922)
    randomY = random.randint(450,1000) 
    randomClickText = " ".join(('input tap',str(randomX),str(randomY)))
    device.shell(randomClickText)
    return randomX,randomY

def CheckIfBagIsFull():
    #Do something else here, maybe check the bag?
    #Checking with pytesseract in Pokestop didn't work
    return