import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input("New data: ")
    print('Now place your tag to write data')
    reader.write(text)
    print('Written')
finally:
    GPIO.cleanup() # this can only be available in the pi
