from asyncio.windows_events import NULL
from contextlib import nullcontext
from tracemalloc import stop
from ppadb.client import Client
import time
#import divimage
from PIL import Image
import numpy as np
import atexit
import pyautogui as pg
import pytesseract
from pytesseract import Output
import catchPokemon
import checkPhone
import findPokemon
import checkPokestop
from variables import device, devices,os,cv2,msconfig, Output
from sys import exit
from vision import CheckIfMenuButton, CheckIfX, ClickOnX, draw_rectangles


if len(devices) == 0:
    print( "No devices found")
    
print("Connected devices:",devices)
print(devices)
#Color of unused Pokestop: (32,108,224) cv2 = [232 120  32]
#Color of used Pokestop: (209, 81, 82) (216, 87, 101)
@atexit.register
def closing():
    device.shell('wm size reset')
try:
    
    checkPhone.CheckApplicationRunning(device)
    checkPhone.CheckScreenSize(device)
    
    time.sleep(1)
    #pix[x,y] = value  # Set the RGBA Value of the image (tuple)
    starttime = time.time()
    print(starttime)
    # checkPokestop.SearchStops()

    # nearbyRadarFound = findPokemon.CheckRadarAvailable()
    # print('Nearby Radar found =', nearbyRadarFound)
    # time.sleep(4)
    # value = 0
    counterOfUsedPokestopClicks = 0
    counterOfNoPokeStops = 0
    while True:
        if CheckIfX() == True:
            print('A window detected, closing it.')
            ClickOnX()
        actualtime = time.time()
        differentTime = actualtime - starttime
        if differentTime <= 15:
            print(differentTime)
            starttime = actualtime
        #region PokeStop
        foundPokeStop = checkPokestop.SearchStops()
        if counterOfUsedPokestopClicks <= 3:
            if counterOfNoPokeStops <= 3:
                if foundPokeStop == True:
                    print('Found a PokéStop! Trying to spin in 3 seconds...')
                    time.sleep(3)
                    inPlayArea = CheckIfMenuButton()
                    if inPlayArea == True:
                        print('Didn\'t click on a PokéStop')
                    else:
                        stopUsed = checkPokestop.CheckStopUsed()
                        if stopUsed == False:
                            print('It\'s an unused PokéStop')
                            checkPokestop.SpinStop()
                            time.sleep(2) #this see above
                            stopNowUsed = checkPokestop.CheckStopUsed()
                            if stopNowUsed == True:
                                print('Successfully spinned! Exiting the PokéStop screen')
                                checkPokestop.ExitStopScreen()
                            else:
                                print('Something went wrong? Exiting screen if possible (is your bag full?)')
                                # CheckIfBagFull
                                # Maybe ask here from Screen of X Symbol?
                                checkPokestop.ExitStopScreen()

                        else:
                            print('It\'s a used PokéStop or Team Rocket got it')
                            counterOfUsedPokestopClicks += 1
                            checkPokestop.ExitStopScreen()
                else:
                    #Try to spin device maybe?
                    print('CBG didn\'t find any PokéStop.')
                    counterOfNoPokeStops += 1
            else:
                randomX,randomY = checkPokestop.TapSomewhereRandom()
                print('Clicking somewhere else random... Random = ',randomX,randomY)
                counterOfNoPokeStops = 0
                time.sleep(5)
        else:
            randomX,randomY = checkPokestop.TapSomewhereRandom()
            print('Clicking somewhere else random... Random = ',randomX,randomY)
            counterOfUsedPokestopClicks = 0
            time.sleep(5)
        #endregion

            
        

        # if key == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        # elif key == ord('f'):
        #     cv2.imwrite('positive/{}.jpg'.format(value),images[0])
        #     value +=1
        # elif key == ord('d'):
        #     cv2.imwrite('negative/{}.jpg'.format(value),images[0])
        #     value +=1



        # isInEncounter = findPokemon.CheckIfEncounter()
        # if isInEncounter == True:
        #     print('Pokemon Encounter active')
        #     pokemonName = catchPokemon.GetPokemonName()
        #     if pokemonName == '':
        #         print('Couldn\'t get Pokemon name')
        #         continue
        #     else:
        #         print('Wild',pokemonName,'appeared!')
        #         catchPokemon.catchLow(pokemonName)
        # else:
        #     findPokemon.PokemonClick()

        

        #time.sleep(5)
        
        
        

        #array = divimage.scanimage(image)
        #print(array)

except Exception as e:
    print(e)
