from time import sleep
import serial

def readresponse():
        b = bytearray(b"                   ");
        ser.readinto(b) #when the serial connection is initialized the usb-power is "flicked"
        print(b)

#setup serial connection
ser = serial.Serial('COM5',115200,timeout=0.5)  # open serial port
print(ser.name)         # check which port was really used
sleep(3)
#when the serial connection is initialized the usb-power is "flicked"
#causing the arduino to boot and thereby iddentify itself
readresponse()


ser.write('@'.encode('ascii'))
readresponse()

ser.write('r'.encode('ascii')) #reading the status of pin 7
ser.write(b"\x07")
print("pin7 status")
readresponse()

ser.write('o'.encode('ascii'))  #set pin 7 as output
ser.write(b"\x07")

print("Blinking pin7 status  ctrl-c to terminate  :-) ")
while True:
        ser.write('1'.encode('ascii'))   #set pin 7 high
        ser.write(b"\x07")
        sleep(0.2)
        ser.write('0'.encode('ascii'))   #set pin 7 high
        ser.write(b"\x07")
        sleep(0.2)
