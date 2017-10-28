import machine
import time
import untplib

# utime.localtime has format:
# (year, month, day, hour, minute, second, weekday, yearday)

# machine.RTC().datetime has/expects format:
# (year, month, day, weekday, hours, minutes, seconds, subseconds)
def synchronize():
    response = untplib.request('us.pool.ntp.org')
    rtc = machine.RTC()
    year, month, day, hour, minute, second, weekday, yearday = time.localtime(time.time() + int(response.offset))
    rtc.datetime((year, month, day, weekday, hour, minute, second, 0))
