import network
import time

__all__ = ['connect']


timeout = 20 # seconds
poll_rate = 2 # seconds


class CannotConnectToWifi(Exception): pass


def connect(ssid, key):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, key)
        start = time.time()
        while not sta_if.isconnected():
            print("Retrying")
            time.sleep(poll_rate)
            now = time.time()
            if now - start > timeout:
                raise CannotConnectToWifi()