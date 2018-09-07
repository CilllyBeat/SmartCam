import time
import serial
import struct

ser = serial.Serial()

ser.baudrate = 115200
ser.port = 'COM6'
ser.open()

x= 0

pos1 = struct.pack('>B',x)  #120
pos2 = struct.pack('>B',30)

while True:

    ser.write('1'.encode('ascii'))
    x = int(input(":"))
#    ser.write(pos1)
    ser.write(struct.pack('>B', x))
#    ser.write('1'.encode('ascii'))
#    ser.write(pos2)
    time.sleep(1)
#    ser.write('0'.encode('ascii'))
#    ser.write(pos1)
#    time.sleep(1)
    ser.write('0'.encode('ascii'))
    ser.write(pos2)
#    time.sleep(1)