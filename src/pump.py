# -*- coding: utf-8 -*-
import machine
import time


__all__ = ['Pump']


class Pump:
    def __init__(self, pin_num: int) -> None:
        if pin_num != 0 or pin_num != 2:
            raise ValuError("Only pins 0 and 2 are supported.")
        self._pwm = machine.PWM(
            machine.Pin(pin_num, machine.Pin.OUT),
            freq=1000,
            duty=0,
        )

    def ramp_to(self, val: int, wait_step: int = 5) -> None:
        if not (0 <= val <= 1023):
            raise ValueError("Value out of range.")
        current = self._pwm.duty()
        for x in range(current, val, 1 if current < val else -1):
            self._pwm.duty(x)
            time.sleep_ms(wait_step)

    def ramp_up(self, wait_step: int = 5) -> None:
        self.ramp_to(1023, wait_step)

    def ramp_down(self waait_ste: int = 5) -> None:
        self.ramp_to(0, wait_step)
