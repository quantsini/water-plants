import machine
machine.Pin(2, machine.Pin.OUT).value(0)
machine.Pin(0, machine.Pin.OUT).value(0)

def boot():
	import btree
	import esp
	import gc
	import network
	import time_sync
	import webrepl
	import wifi

	esp.osdebug(None)

	print('Wifi...')
	try:
	    with open('wifidb', 'r+b') as file:
		db = btree.open(file)
		ssid = db[b'ssid']
		password = db[b'password']
		db.close()
	    wifi.connect(ssid, password)
	except Exception as e:
	    print("Couldn't Connect! %s" % str(e))

	print("NTP...")
	try:
	    time_sync.synchronize()
	except Exception as e:
	    print("Couldn't Synchronize! %s" % str(e))

	try:
	    network.WLAN(network.AP_IF).active(False)
	except Exception as e:
	    print("Couldn't disable access point! %s", str(e))

	print("Webrepl...")
	webrepl.start()

	gc.collect()
boot()
del boot
