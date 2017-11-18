# -*- coding: utf-8 -*-

import machine
import time
import untplib


__all__ = ['synchronize']


def synchronize(ntp_url: str = 'us.pool.ntp.org') -> None:
    response = untplib.request(ntp_url)

    # utime.localtime has format:
    # (year, month, day, hour, minute, second, weekday, yearday)
    year, month, day, hour, minute, second, weekday, yearday = time.localtime(time.time() + int(response.offset))

    # machine.RTC().datetime has/expects format:
    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    machine.RTC().datetime((year, month, day, weekday, hour, minute, second, 0))
