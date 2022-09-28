import RPi.GPIO as gpio
import time
import logging


class ServoController():

    def __init__(self):
        """Set up the servos"""
        logging.info('Setting up servo')
        self.channels = [11,12]
        self._setup_gpio()
        self._set_servo_range()

    def _set_servo_range(self):
        """Sets the range of the servo"""
        self.servo_bounds_degrees = 20
        self.servo_max = 180 - self.servo_bounds_degrees
        self.servo_min = self.servo_bounds_degrees
        self.servo_range = self.servo_max - self.servo_min

    def __del__(self):
        """Clean up"""
        self.pwm.stop()
        gpio.cleanup()

    def _setup_gpio(self):
        """Set up the gpio"""
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.channels, gpio.OUT)
        self.pwm = gpio.PWM(self.channels, 50)
        self.pwm.start(0)

    def set_servo_angle(self, angle, axis):
        """Set the angle of the servo"""
        logging.info(f'Setting {axis} axis angle to {angle}')
        if axis == 'x':
            channel = self.channels[0]
        else:
            channel = self.channels[1]
        gpio.output(channel, True)
        self.pwm.ChangeDutyCycle(angle / 18 + 2)
        time.sleep(1)
        gpio.output(channel, False)
        self.pwm.ChangeDutyCycle(0)

    def set_servo_percent(self, percent, axis):
        """Converts a decimal percentage into servo angle"""
        angle = int((1 - percent) * self.servo_range) + self.servo_min
        self.set_servo_angle(angle, axis)
