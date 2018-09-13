import time
import serial
import math

ser = serial.Serial()

ser.baudrate = 9600
ser.port = 'COM5'
ser.open()

while True:
    sel = input()
    if sel == 'A':
        print(sel)
        ser.write(b'A')
        time.sleep(1)
    if sel == 'S':
        print(sel)
        ser.write(b'S')
        time.sleep(1)
    if sel == 'Z':
        print(sel)
        ser.write(b'Z')
        time.sleep(1)
    if sel == 'X':
        print(sel)
        ser.write(b'X')
        time.sleep(1)