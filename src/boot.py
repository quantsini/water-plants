# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
print("Setting GPIOs to low...")
import machine
machine.Pin(0, machine.Pin.OUT, 0)
machine.Pin(2, machine.Pin.OUT, 0)
print("GPIOs set to low!")

print("Connecting to wifi...",)
import wifi
import btree
try:
    with open('wifidb', 'r+b') as file:
        db = btree.open(file)
        ssid = db[b'ssid']
        password = db[b'password']
        db.close()
    wifi.connect(ssid, password)
    print("Connected!")
except Exception as e:
    print("Couldn't Connect! %s", str(e))

print("Synchronizing time with NTP...",)
import time_sync
try:
    time_sync.synchronize()
    print("Synchronized!")
except Exception as e:
    print("Couldn't Synchronize! %s", str(e))

print("Disabling access point...",)
import network
try:
    network.WLAN(network.AP_IF).active(False)
except Exception as e:
    print("Couldn't disable access point! %s", str(e))

print("Enabling web repl...",)
import webrepl
webrepl.start()
print("Enabled!")

print("Garbage Collecting...",)
import gc
gc.collect()
print("Garbage Collected!")
print("Ready to rock")