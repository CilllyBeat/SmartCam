#borrowed code modified to blink SOS
from time import sleep
import serial

def readresponse():
        b = bytearray(b"                   ");
        ser.readinto(b) #when the serial connection is initialized the usb-power is "flicked"
        print(b)

def sosLetter(restingT):
        blinkON()
        sleep(restingT)
        blinkOFF()
        sleep(restingT)

        blinkON()
        sleep(restingT)
        blinkOFF()
        sleep(restingT)

        blinkON()
        sleep(restingT)
        blinkOFF()
        sleep(restingT)


def blinkON():
        ser.write('1'.encode('ascii'))  # set pin 7 high
        ser.write(b"\x07")

def blinkOFF():
        ser.write('0'.encode('ascii'))  # set pin 7 high
        ser.write(b"\x07")

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

while True:
        sosLetter(0.3)  #morse letter S
        sosLetter(0.8)  #morse letter O
        sosLetter(0.3)
        sleep(3)


