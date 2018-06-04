#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, json
from requests.auth import HTTPDigestAuth
" Main config for TV"
ip = "10.0.2.121"
port = "8080"
''' Username and Password in RDHosts.db from toshiba db app, i havent reversed the method to obtain password '''
username = r"DE-AD-BE-EF-13-37"
password = r"abcdefghijklmnop"

mainurl = "http://" + ip + ":" + port
print mainurl

def menu():
		i = input('\n --- Toshiba TV Remote --- \n1) TV an/ausschalten \n2) Lautstaerke einstellen\n3) TV Koppeln \n\n Auswahl: ')
		if (i == 1):
			url = geturl("power")
			r = sendget(url)
			resp_dict = json.loads(r.text)
			print "\nPower: " + str(resp_dict["power"])
			i = input('\n1) AN\n2) AUS\n3) STATUS\nAuswahl: ')
			if (i == 1):
				r = sendpost(url, "power", "on", "0", "0")
				print r.text
				return 0	
			elif (i == 2):
				r = sendpost(url, "power", "off")
				print r.text
				return 0
			else:
				print "Error"
				return -1
		elif (i == 2):
			url = geturl("volume")
			url2 = geturl("mute")
			r2 = sendget(url2)
			r = sendget(url)
			resp_dict = json.loads(r.text)
			resp_dict2 = json.loads(r2.text)
			print "\nLautstärke: " + str(resp_dict["volume"]) + " Mute: " + str(resp_dict2["mute"])
			i = input('\n1) Lautstärke ändern\n2) Mute\n Auswahl: ')
			if (i == 1):
				vol = input("\n Lautstärke: ")
				r = sendpost(url, "volume", vol)
				print r.text
				return 0	
			elif (i == 2):
				i = input("\n1) Mute ON\n2) Mute OFF\n Auswahl: ")
				if (i == 1):
					r = sendpost(url2, "mute", "on")
				elif (i == 2):
					r = sendpost(url2, "mute", "off")
				else:
					print "Error"
					return -1
				print r.text
				return 0
			elif (i == 3):
				payload = {"user_id": "DE-AD-BE-EF-13-37"}
				url = "http://" + ip + ":" + port + "/v2/public/request_connection"
				r = requests.post(url, data=payload)
				print url
				print r
				print r.text
			else:
				print "Error"
				return -1
				
			
def sendget(url):
	return requests.get(url, auth=HTTPDigestAuth(username, password))

def sendpost(url, type1, val1, type2 = "0", val2 = "0"):
	'''
	if (type2 == 0):
	'''
	print "Payload1"
	payload = {type1: val1}
	'''
	elif (type2 != 0):
		print "Payload2"
		payload = {type1: val1, type2: val2}
	'''
	print "post request payload: "
	print payload
	return requests.post(url, auth=HTTPDigestAuth(username, password), data=payload)

def geturl(key):
	"Returns the url for given key"
	urls = {'volume': '/v2/remote/status/volume', 'mute': '/v2/remote/status/mute', 'power': '/v2/remote/status/power', 'remotekey': '/v2/remote/remote', 'externalinput': '/v2/remote/status/external_input', 'channel': '/v2/remote/status/channel', 'browserurl': '/v2/remote/browser/url', 'power': '/v2/remote/status/power'}
	return mainurl + urls.get(key, 'default')

i = menu()
