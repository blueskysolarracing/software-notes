from os import environ
from time import sleep

from periphery import GPIO

path = environ['path']
path_BFM_LED0 = environ['path_BFM_LED0']

line = int(environ['line'])
line_BFM_LED0 = int(environ['line_BFM_LED0'])

gpio = GPIO(path, line, 'out')
gpio_BFM_LED0 = GPIO(path_BFM_LED0, line_BFM_LED0, 'out')
value = True

while True:
  gpio.write(value)
  gpio_BFM_LED0.write(value)
  sleep(1)

  value = not value
