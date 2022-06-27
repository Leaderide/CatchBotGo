from asyncio.windows_events import NULL
from ppadb.client import Client
import time
import readJson
from variables import pytesseract,cv2,Output,device,config

status = ['Caught', 'Fled', 'Escaped']
msconfig= r"--psm 11 --oem 3"
#region Coordinates
throwPokeball = 'input swipe 542 1700 553 870 100'
clickOKButton = 'input tap 520 1370'
clickOnPokemonSetting = 'input tap 920 1780'
clickOnTransfer = 'input tap 890 1578'
clickOnYesTransfer = 'input tap 532 1150'
#endregion
transferPokemon = config['catch']['transfer']

def TakeScreen():
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
    img = cv2.imread('screen.png')      
    f.close()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return [img,invert]
    
def OnlyScreen():
    image = device.screencap()
    return image
def catchLow(pokemonNameDraw):
    print('CBG throwing pokeball')
    device.shell(throwPokeball)
    time.sleep(1.6)
    DrawCVCatch(pokemonNameDraw)

def GetPokemonName():

    image = TakeScreen()
    pokemonName = ''
    data = pytesseract.image_to_data(image[1], lang='eng', config=msconfig, output_type=Output.DICT)
    amount_boxes = len(data['text'])
    for i in range(amount_boxes):
        if float(data['conf'][i]) > 80:
            (x, y, width, height) = (data['left'][i],data['top'][i], data['width'][i], data['height'][i])
            for j in readJson.dataPokemon:
                if data['text'][i] == j:
                    pokemonName = data['text'][i]
                    cv2.rectangle(image[0], (x, y), (x+width, y+height), (0,255,0), 2)
                    cv2.putText(image[0], pokemonName, (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2, cv2.LINE_AA)
    
    return pokemonName

def DrawCVCatch(text):
    image = TakeScreen()
    data = pytesseract.image_to_data(image[1], lang='eng', config=msconfig, output_type=Output.DICT)
    text1 = ''
    amount_boxes = len(data['text'])
    for i in range(amount_boxes):
        (x, y, width, height) = (data['left'][i],data['top'][i], data['width'][i], data['height'][i])
        for j in status:
            if data['text'][i] == j:
                cv2.rectangle(image[0], (x, y), (x+width, y+height), (0,255,0), 2)
                cv2.putText(image[0], data['text'][i], (x, y+height+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2, cv2.LINE_AA)
                text1 = data['text'][i]
    
    finalstring = " ".join((text1, text))
    time.sleep(10)
    ExitPokemonCaught(text)

def ExitPokemonCaught(pokemon):
    image = TakeScreen()
    template= cv2.imread('menu_icons/OKButtonCaught.png')
    
    for i in range(3):  
        result = cv2.matchTemplate(image[0], template, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if maxVal > 0.7:
            print('OK Button detected')
            device.shell(clickOKButton)
            time.sleep(4)
            break
        else:
            print('No OK Button, maybe already in Pokemon View? Retrying in 3 seconds',i,'/ 2')
        time.sleep(3)

    if transferPokemon == True:
        for i in range(3):
            pokemonName = GetPokemonName()
            if pokemonName == '':
                print('Maybe not in transfer screen? Retrying in 3 seconds',i,'/ 2')
            else:
                print('CBG is transferring the',pokemon)
                device.shell(clickOnPokemonSetting)
                time.sleep(1)
                device.shell(clickOnTransfer)
                time.sleep(1)
                device.shell(clickOnYesTransfer)
                break
            time.sleep(3)
        
        

    

#    img = cv2.resize(img,(540,960))
#    cv2.imshow("stats",img)
#   cv2.waitKey(0)
