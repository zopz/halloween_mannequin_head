import os
import logging
import time
import requests
from app import HalloweenMannequinHead as app

class Test():

    def __init__(self):
        logging.info('Starting test')
        self.server_mode = bool(os.environ.get('SERVER_MODE', False))
        if not self.server_mode:
            app._setup_servo()

    def run(self):
        """Run the tests"""
        try:
            for deg in range(0, 100):
                if self.server_mode:
                    host = os.environ['RASPBERRY_PI_HOST']
                    url = f'http://{host}:8000/servo/?px={deg}&py={deg}'
                    requests.get(url)
                else:
                    app.servo_controller.set_servo_percent(deg, 'x')
                    app.servo_controller.set_servo_percent(deg, 'y')
                time.sleep(0.1)
        except KeyboardInterrupt:
            logging.info('Exiting application')

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    test = Test()
    test.run()
