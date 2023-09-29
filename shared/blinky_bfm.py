from os import environ
from time import sleep

from periphery import GPIO

path_Ixora_LED4_GREEN = environ['path_Ixora_LED4_GREEN']
path_BFM_LED0 = environ['path_BFM_LED0']

line_Ixora_LED4_GREEN = int(environ['line_Ixora_LED4_GREEN'])
line_BFM_LED0 = int(environ['line_BFM_LED0'])

gpio_Ixora_LED4_GREEN = GPIO(path_Ixora_LED4_GREEN, line_Ixora_LED4_GREEN, 'out')
gpio_BFM_LED0 = GPIO(path_BFM_LED0, line_BFM_LED0, 'out')
value = True

while True:
  gpio_Ixora_LED4_GREEN.write(value)
  gpio_BFM_LED0.write(value)
  sleep(1)

  value = not value
