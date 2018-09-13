import time
import serial
import math

ser = serial.Serial()

ser.baudrate = 9600
ser.port = 'COM5'
ser.open()

while True:
        ser.write(b'A')
        time.sleep(1)
        ser.write(b'B')
        time.sleep(1)
