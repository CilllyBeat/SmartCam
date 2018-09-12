import serial
import struct
import cv2

ser = serial.Serial('COM6', 115200, timeout=0.5)


class Motor:
    def __init__(self, address):
        self.address = address

    def moveDownOrRight(self):
        ser.write(str(self.address).encode('ascii'))  # activate pan/tilt motor
        ser.write(struct.pack('>B', 1))  # if centre of rectangle is left of OK range, move right
        # print('motor down or right' + str(self.address))   # to check functionality

    def moveLeftOrUp(self):
        ser.write(str(self.address).encode('ascii'))  # activate pan motor
        ser.write(struct.pack('>B', 2))  # if centre of rectangle is left of OK range, move right
        # print('motor left or up' + str(self.address))  # to check functionality

    def stayThere(self):
        ser.write(str(self.address).encode('ascii'))  # activate pan motor by sending address of motor
        ser.write(struct.pack('>B', 3))  # if centre of rectangle is left of OK range, move right
        # print('staying put' + str(self.address))   # to check functionality


class Detector:
    def __init__(self, name, filename):
        self.name = name
        self.cascade = cv2.CascadeClassifier(filename)
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.end_cord_x = 0  # specifying lower corner coordinates of roi rectangle
        self.end_cord_y = 0
        self.xCenter = 0
        self.yCenter = 0
        self.num = 0

    def detectROI(self, gray_frame):
        area = self.cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)
        # print(area)   # to check functionality
        for (x, y, w, h) in area:
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
            self.end_cord_y = y + h
        return area

    def createRectangle(self, show_frame):
        color = (0, 255, 0)  # BGR blue green red, not RGB red green blue, color of rectangle
        stroke = 2  # rectangle frame thickness
        cv2.rectangle(show_frame, (self.x, self.y), (self.end_cord_x, self.end_cord_y), color,
                      stroke)  # object, start +end coord., color rectangle, stroke thickness

    def xCenterCoordinate(self):
        self.xCenter = (self.x + (self.x + self.w)) / 2
        # print(self.xCenter)
        return self.xCenter

    def yCenterCoordinate(self):
        self.yCenter = (self.y + (self.y + self.h)) / 2
        # print(self.yCenter)
        return self.yCenter

    def saveFrame(self, image_frame):
        photo = self.name + str(self.num / 10) + ".png"
        cv2.imwrite(photo, image_frame)
        self.num += 1

class Camera:
    def __init__(self, input_channel):
        self.input = input_channel

    def setupVideo(self):
        self.capture = cv2.VideoCapture(self.input)
        return self.capture

    def setupFrame(self):
        return self.capture.read()

    def setupGrayFRame(self, copy_frame):
        return cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)

    def releaseCam(self):
        return self.capture.release()