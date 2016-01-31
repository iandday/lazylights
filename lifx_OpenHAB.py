"""
Adopted from VinzzB on https://github.com/mpapi/lazylights/issues/3
-------------------------------
Argument:
1 = power all bulbs
0 = set all bulbs off
-------------------------------
"""
import lazylights
import time
import struct
import sys
import string
import binascii
import colorsys

if sys.version_info[0] > 2:
    PY3K = True
else:
    PY3K = False


def setBulbPower(bulbs, power):
    elapsedTime = 0
    # exit if bulb is already in requested state
    bulbStatePre = lazylights.get_state(bulbs)
    if powerState(bulbStatePre) and power == 1:
        return
    if not powerState(bulbStatePre) and power == 0:
        return
    lazylights.set_power(bulbs, power)
    # wait for status update to ensure action was completed
    while elapsedTime < 5:
        bulbState = lazylights.get_state(bulbs)
        if powerState(bulbState) == power:
            print(getLabels(bulbState) + 'Bulbs powered ' + ('ON' if power else 'OFF'))
            return
        time.sleep(.5)
        elapsedTime += 1



def powerState(bulbList):
    """Returns boolean result for bulbs power status"""
    power = False
    for bulb in lazylights.get_state(bulbList):
        power |= bulb.power > 0
    return power

def bulbState(bulbList):
    results = lazylights.get_state(bulbList)
    for k in  results:
        print 'Gateway MAC: ' + str(k.bulb.gateway_mac)
        print 'MAC: ' + str(k.bulb.mac)
        print 'Address: ' + str(k.bulb.addr[0]) + ':' + str(k.bulb.addr[1])
        print 'Hue: ' + str(k.hue)
        print 'Saturatuion: ' + str(k.saturation)
        print 'Brightness: ' + str(k.brightness)
        print 'Kelvin: ' + str(k.kelvin)
        print 'Power: ' + str(k.power)
        print 'Label: ' + str(k.label)





def getLabels(bulbs):
    r = ""
    for bulb in bulbs:
        if PY3K:
            r += ("" if r == "" else ", ") + str(bulb.label, 'ASCII').split('\x00')[0]
        else:
            r += ("" if r == "" else ", ") + str(bulb.label).split('\x00')[0]
    return r


def createBulb(ip, macString, port=56700):
    return lazylights.Bulb(b'LIFXV2', binascii.unhexlify(macString.replace(':', '')), (ip, port))


def setBulbColor(bulb, r, g, b, kelvin, fade):
    """Sets bulb color based on RGB color instead of HSV values"""
    r /= float(255)
    g /= float(255)
    b /= float(255)
    (huevalue, saturationvalue, brightnessvalue) = colorsys.rgb_to_hsv(r, g, b)
    huevalue *= float(360)
    lazylights.set_state(bulbs, huevalue, saturationvalue, brightnessvalue, kelvin, fade, raw=False)


if __name__ == "__main__":
    # Bulb List
    #'name':{'ipAddress':'###.###.###.###', 'macAddress':'##:##:##:##:##:##'}
    bulbInventory = {
        'lifx1':{'ipAddress':'10.168.1.17', 'macAddress':'D0:73:D5:02:64:11'}
            }

    # parse bulb selection and create bulbs list
    selectedBulbs = []
    for bulb in bulbInventory:
        if bulb == sys.argv[1]:
            ipAddr = str(bulbInventory[bulb]['ipAddress'])
            macAddr = str(bulbInventory[bulb]['macAddress'])
            selectedBulbs = [createBulb(ipAddr, macAddr)]
            continue
    if not selectedBulbs:
        print('Incorrect bulb specified, terminating execution')
        sys.exit()

    # parse function
    if sys.argv[2].lower() == 'off':
        lazylights.set_power(selectedBulbs, 0)
    elif sys.argv[2].lower() == 'on':
        lazylights.set_power(selectedBulbs, 1)
    elif sys.argv[2].lower() == 'status':
        if powerState(selectedBulbs):
            sys.exit('ON')
        else:
            sys.exit('OFF')
    elif sys.argv[2].lower() == 'state':
        bulbState(selectedBulbs)

    else:
        commandInput = sys.argv[2].split(',')
        hue = int(float(commandInput[0]))
        saturation = int(float(commandInput[1]))
        brightness = int(float(commandInput[2]))
        kelvin = int(float(commandInput[3]))
        fade = int(float(commandInput[4]))

        if not powerState(selectedBulbs):
            lazylights.set_power(selectedBulbs, 1)
        lazylights.set_state(selectedBulbs, hue, saturation, brightness, kelvin, fade, raw=False)

