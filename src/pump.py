import machine
import time

class Pump:
	def __init__(self, pin_num):
		self._pwm = machine.PWM(
			machine.Pin(pin_num, machine.Pin.OUT),
			freq=1000,
			duty=0,
		)
	
	def ramp_to(self, val, wait_step=5):
		if not (0 <= val <= 1023):
			raise ValueError("Value out of range")
		current = self._pwm.duty()
		for x in range(current, val, 1 if current < val else -1):
			self._pwm.duty(x)
			time.sleep_ms(wait_step)

	def ramp_up(self):
		self.ramp_to(1023)

	def ramp_down(self):
		self.ramp_to(0)
