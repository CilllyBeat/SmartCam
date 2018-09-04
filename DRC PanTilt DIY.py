from time import sleep
import serial

ser = serial.Serial('COM6', 112500, timeout=0.5)
print(ser.name)

ser.write('@'.encode('ascii'))  #pining and get

while True:
    ser.write(b"\x31")  #'1', top servo
    ser.write(b"\x7A")  #'z', high value
    sleep(0.8)
    ser.write(b"\x30")  #'0', bottom servo
    ser.write(b"\x7A")  #'z'
    sleep(0.8)
    ser.write(b"\x31")  #'1'
    ser.write(b"\x0A")  #dec 10, low value
    sleep(0.8)
    ser.write(b"\x30")  #'0'
    ser.write(b"\x0A")  #dec 10
    sleep(0.8)