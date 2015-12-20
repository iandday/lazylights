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
import sys, string
import binascii
import colorsys

if sys.version_info[0] > 2:
    PY3K = True
else:
    PY3K = False

def setBulbPower(bulbs, power): 
	elapsedTime = 0
	#exit if bulb is already in requested state
	bulbStatePre = lazylights.get_state(bulbs)
	if powerState(bulbStatePre) and power == 1:
		return
	if not powerState(bulbStatePre) and power == 0:
		return
	lazylights.set_power(bulbs, power)
	#wait for status update to ensure action was completed
	while elapsedTime < 5:
		bulbState = lazylights.get_state(bulbs) 
		if powerState(bulbState) == power: 
			print(getLabels(bulbState) +  'Bulbs powered '+ ("ON" if power else "OFF"))
			return
		time.sleep(.5)
		elapsedTime += 1
	



#Check if all bulbs are powered on or off   
def powerState(bulbs):
    power = False #Off by default.
    for bulb in bulbs:
		power |= bulb.power>0 #once True, always True!
    return power

def getLabels(bulbs):
	r =""
	for bulb in bulbs:
		if PY3K:
			r += ("" if r=="" else ", ") + str(bulb.label,'ASCII').split('\x00')[0]
		else:
			r += ("" if r=="" else ", ") + str(bulb.label).split('\x00')[0]
	return r

def createBulb(ip, macString, port = 56700):        
	return lazylights.Bulb(b'LIFXV2', binascii.unhexlify(macString.replace(':', '')), (ip,port))


def setBulbColor(bulb, r, g, b, kelvin, fade): 
	r = r / float(255)
	g = g / float(255)
	b = b / float(255)
	(hue, saturation, brightness) = colorsys.rgb_to_hsv(r, g, b)
	hue= hue * float(360)
	lazylights.set_state(bulbs,hue, saturation, brightness, kelvin, fade, raw=False)
	
"""
    Sets the state of `bulbs`.
    If `raw` is True, hue, saturation, and brightness should be integers in the
    range of 0x0000 to 0xffff. Otherwise, hue should be a float from 0.0 to
    360.0 (where 360.0/0.0 is red), and saturation and brightness are floats
    from 0.0 to 1.0 (0 being least saturated and least bright)..
    `kelvin` is an integer from 2000 to 8000, where 2000 is the warmest and
    8000 is the coolest. If this is non-zero, the white spectrum is used
    instead of the color spectrum (hue and saturation are be ignored).
    `fade` is an integer number of milliseonds over which to transition the
    state change, carried out by the bulbs.
"""	
	
if __name__ == "__main__":  
    #Create our own Bulbs
	myBulb1 = createBulb('10.168.1.21', 'D0:73:D5:02:64:11')
    #append to bulbs list
	bulbs = [myBulb1]

	
	
	#setBulbPower(bulbs,sys.argv[1] == '1')
	#RGB Colors
	#setBulbColor(bulbs, 255, 255, 255, 8500, 0) 
	input = sys.argv[1].split(',')

	hue=int(input[0])
	saturation=int(input[1])
	brightness=int(input[2])
	lazylights.set_state(bulbs, hue, saturation, brightness, kelvin=0, fade=0, raw=False)

	