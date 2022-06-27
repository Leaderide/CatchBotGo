import re
import time

def CheckApplicationRunning(device):
        isRunning = device.shell(f'pidof com.nianticlabs.pokemongo')
        if isRunning == '':
            print('Pokemon Go is not running, starting application...')
            device.shell(f'monkey -p com.nianticlabs.pokemongo 1')
        else:
            print('Alright, Pokemon is running, making sure it\'s the main activity')

        time.sleep(3)
        topApp = device.shell(f'dumpsys activity activities | grep mResumedActivity')

        pokeApp = "com.nianticlabs.pokemongo"

        if pokeApp in topApp:
            print("Great!")
        else:
            device.shell(f'monkey -p com.nianticlabs.pokemongo 1')

def CheckScreenSize(device):
    screenSize = device.shell(f'wm size ')

    actualScreen = re.search("Physical size: (.+?)\n", screenSize)
    overrideScreen = re.search("Override size: (.+?)\n", screenSize)
    if actualScreen:
        actualScreen = actualScreen.group(1)
        print('Screen size is',actualScreen,'changing it into 1080x1920')
    if overrideScreen:
        overrideScreen = overrideScreen.group(1)
        print('Screen is already', overrideScreen)


    if actualScreen != "1080x1920":
        device.shell('wm size 1080x1920')