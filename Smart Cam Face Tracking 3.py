import serial
import struct
import cv2

# for serial communication with aruino slave
port = 'COM6'
ser = serial.Serial(port, 115200, timeout=0.5)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(1)

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
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)  # what is scale factor min neighbor?
    xCenter = 0  # resetting variable to be so the camera doesn't continue pan/tilt in case the last place a face was-
    yCenter = 0  # seen was out of range and continue in that direction.

    for (x, y, w, h) in faces:
        print(x, y, w, h)  # to test if it sees the face
        roi_color_face = frame[y:y + h, x:x + w]

        end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color,
                      stroke)  # object, start coordinates, end cooordinates, color rectangle, stroke thickness
        xCenter = (x + (x + w)) / 2
        yCenter = (y + (y + h)) / 2

        if num in range(0, 101, 10):  # for saving pictures at intervals. w/o intervals = almost identical pictures
            img_item = "img" + str(num / 10) + ".png"
            cv2.imwrite(img_item, frame2)  # getting image from frame2 to be rid of colorful rectangles

        num += 1

    print(xCenter, yCenter)  # so I can see the coordinates when issues occur (troubleshooting)
    if xCenter != 0:  # checks to see if there is a coordinate y
        if abs(xCenter) < 280:  # based on resolution 480p
            ser.write('0'.encode('ascii'))  # activate pan motor
            ser.write(struct.pack('>B', 1))  # if centre of rectangle is left of OK range, move right

        elif abs(xCenter) > 360:
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 2))  # if centre of rectangle is right of OK range, move left

        elif 280 <= abs(xCenter) <= 360:
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 3))  # if centre is in range, do nothing

    if yCenter != 0:  # checks to see if there is a coordinate y
        if yCenter < 200:  # based on resolution 480p
            ser.write('1'.encode('ascii'))  # activate tilt motor
            ser.write(struct.pack('>B', 1))  # if centre rectangle is above OK range, move down

        elif yCenter > 280:
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 2))  # if centre rectangle is below OK range, move up

        elif 200 <= yCenter <= 280:
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 3))  # centre is in OK range do nothing

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
