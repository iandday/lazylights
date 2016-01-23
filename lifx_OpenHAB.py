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
    for bulb in lazylights.get_state(bulbs):
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
	'''Sets bulb color based on RGB color instead of HSV values'''
	r = r / float(255)
	g = g / float(255)
	b = b / float(255)
	(hue, saturation, brightness) = colorsys.rgb_to_hsv(r, g, b)
	hue = hue * float(360)
	lazylights.set_state(bulbs,hue, saturation, brightness, kelvin, fade, raw=False)
	

	
if __name__ == "__main__":  
	#Bulb List 
	#name = createBulb(IP Address, MAC Address)
	lifx1 = createBulb('10.168.1.17', 'D0:73:D5:02:64:11')
	bulbs = [lifx1]
	
	#parse bulb selection
	if sys.argv[1] == 'lifx1':
		 bulbs = [lifx1]
	
	
	#parse command selection
	if sys.argv[2] == 'off':
		lazylights.set_power(bulbs, 0)
	elif sys.argv[2] == 'on':
		lazylights.set_power(bulbs, 1)
	else:
		input = sys.argv[2].split(',')
		hue=int(float(input[0]))
		saturation=int(float(input[1]))
		brightness=int(float(input[2]))
		kelvin = int(float(input[3]))
		fade = int(float(input[4]))
		
		if not powerState(bulbs):
			lazylights.set_power(bulbs, 1)

		lazylights.set_state(bulbs, hue, saturation, brightness, kelvin, fade, raw=False)
#lazylights.get_state(bulbs)