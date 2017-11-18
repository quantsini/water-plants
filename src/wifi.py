# -*- coding: utf-8 -*-
import network
import time
from micropython import const

__all__ = ['connect']


_timeout = const(20) # seconds
_poll_rate = const(2) # seconds


class CannotConnectToWifi(Exception): pass


def connect(ssid: str, key: str) -> None:
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, key)
        start = time.time()
        while not sta_if.isconnected():
            print("Retrying")
            time.sleep(_poll_rate)
            now = time.time()
            if now - start > _timeout:
                raise CannotConnectToWifi()