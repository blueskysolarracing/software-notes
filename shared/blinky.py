from os import environ
from time import sleep

from periphery import GPIO

path = environ['path']
line = int(environ['line'])
gpio = GPIO(path, line, 'out')
value = True

while True:
  gpio.write(value)
  sleep(1)

  value = not value
