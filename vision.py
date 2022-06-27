from variables import cv2,device
from catchPokemon import TakeScreen

xButtonOffset = [524, 1788]

def draw_rectangles(haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4
        mid = []
        top = []
        bot = []
        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x+150, y+880)
            bottom_right = (x+150 + w, y+880 + h)
            top.append(top_left)
            bot.append(bottom_right)
            

            #mid.append((top_left[0]+bottom_right[0])/2)
            #mid.append((top_left[1]+bottom_right[1])/2)
            


            # draw the box
            #cv2.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)
     
        return top,bot

def CheckActualStatusOfScreen():
    return
def CheckIfMenuButton():
    white = (255,255,255)
    red = (69,57,255)
    menuButtonWhiteOffset = [585, 1780]
    menuButtonRedOffset = [585,1735]
    image = TakeScreen()
    menuColorWOnScreen = image[0][menuButtonWhiteOffset[1],menuButtonWhiteOffset[0]]
    menuColorROnScreen = image[0][menuButtonRedOffset[1],menuButtonRedOffset[0]]
    if menuColorWOnScreen[0] == white[0] and menuColorWOnScreen[1] == white[1] and menuColorWOnScreen[2] == white[2]:
        if menuColorROnScreen[0] == red[0] and menuColorROnScreen[1] == red[1] and menuColorROnScreen[2] == red[2]:
            return True
        else:
            return False
    else:
        return False
def CheckIfX():
    image = TakeScreen()
    y=1700
    x=440
    h=200
    w=200
    image[0] = image[0][y:y+h, x:x+w]
    template= cv2.imread('menu_icons/x.png')
    result = cv2.matchTemplate(image[0], template, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    
    if maxVal > 0.7:
        return True
    else:
        return False

def ClickOnX():
    text1 = 'input tap'
    text2 = str(xButtonOffset[0])
    text3 = str(xButtonOffset[1])
    clickOnX = " ".join((text1, text2,text3))
    device.shell(clickOnX)