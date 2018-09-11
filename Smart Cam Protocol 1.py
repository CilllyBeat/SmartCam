import serial
import struct
import cv2
from Classes import Cascades

# for serial communication with aruino slave
ser = serial.Serial('COM6', 115200, timeout=0.5)
cap = cv2.VideoCapture(0)   # CHANGE BACK TO 1 WHEN NOT INTEGRATED WEBCAM

frontface = Cascades('frontface', "haarcascade_frontalface_default.xml", frame=None, gray=None)

color = (0, 255, 0)  # BGR blue green red, not RGB red green blue, color of rectangle
stroke = 2  # rectangle frame thickness
num = 0  # counter for pictures

while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cap.read()  # used for showing window with rectangles
    ret, frame2 = cap.read()  # used for taking images w/o rectangles

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # to use haar cascade, frame must be grayscale
    faces = frontface.setupMultiScaleDetection(gray)
    xCenter = 0  # resetting variable to be so the camera doesn't continue pan/tilt in case the last place a face was-
    yCenter = 0  # seen was out of range and continue in that direction.

    frontface.createROI(frame, gray)
    frontface.createRect(frame)



#    for (x, y, w, h) in faces:
#        roi_color_face = frame[y:y + h, x:x + w]
#
#        end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
#        end_cord_y = y + h
#        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color,
#                      stroke)  # object, start coordinates, end cooordinates, color rectangle, stroke thickness
#        xCenter = (x + (x + w)) / 2
#        yCenter = (y + (y + h)) / 2

#        if num in range(0, 101, 10):  # for saving pictures at intervals. w/o intervals = almost identical pictures
#            img_item = "img" + str(num / 10) + ".png"
#            cv2.imwrite(img_item, frame2)  # getting image from frame2 to be rid of colorful rectangles

#        num += 1

    # print(xCenter, yCenter)  # so I can see the coordinates when issues occur (troubleshooting)
    if xCenter != 0:  # checks to see if there is a coordinate y
        if xCenter < 280:  # based on resolution 480p
            ser.write('0'.encode('ascii'))  # activate pan motor
            ser.write(struct.pack('>B', 1))  # if centre of rectangle is left of OK range, move right

        elif xCenter > 360:
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 2))  # if centre of rectangle is right of OK range, move left

    if yCenter != 0:  # checks to see if there is a coordinate y
        if yCenter < 200:  # based on resolution 480p
            print("break b" + str(yCenter))
            ser.write('1'.encode('ascii'))  # activate tilt motor
            ser.write(struct.pack('>B', 1))  # if centre rectangle is above OK range, move down

        elif yCenter > 280:
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 2))  # if centre rectangle is below OK range, move up

    if xCenter is 0:  # if there is no face coordinates will be (0, 0)
        ser.write('0'.encode('ascii'))
        ser.write(struct.pack('>B', 3))  # there is no face, therefore it shall stay put

    if yCenter is 0:  # if there is no face coordinates will be (0, 0)
        ser.write('1'.encode('ascii'))
        ser.write(struct.pack('>B', 3))  # there is no face, therefore it shall stay put

    cv2.imshow('frame', frame)  # show image frame with rectangle
    # cv2.imshow('gray',gray) # needed for detection but not or showing
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()