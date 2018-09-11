import cv2
from Classes2 import Motor, Detector

# initializes two objects of the class motor
panMotor = Motor(0)
tiltMotor = Motor(1)

face = Detector("face","haarcascade_frontalface_default.xml")

# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(0)   # change to 1 for usb cam

color = (0, 255, 0)  # BGR blue green red, not RGB red green blue, color of rectangle
stroke = 2  # rectangle frame thickness
num = 0  # counter for pictures

while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cap.read()  # used for showing window with rectangles
    ret, frame2 = cap.read()  # used for taking images w/o rectangles
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # to use haar cascade, frame must be grayscale
    face.detectROI(gray, frame)
    face.createRectangle(frame)
    face.centreCoordinates()
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)  # what is scale factor min neighbor?

    xCenter = 0  # resetting variable to be so the camera doesn't continue pan/tilt in case the last place a face was-
    yCenter = 0  # seen was out of range and continue in that direction.

#    for (x, y, w, h) in faces:
        #print(x, y, w, h)  # to test if it sees the face
#        roi_color_face = frame[y:y + h, x:x + w]

#        end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
#        end_cord_y = y + h
#        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color,
#                      stroke)  # object, start coordinates, end coordinates, color rectangle, stroke thickness
#        xCenter = (x + (x + w)) / 2
#        yCenter = (y + (y + h)) / 2

#        for num in range(0, 101, 10):  # for saving pictures at intervals. w/o intervals = almost identical pictures
#            img_item = "img" + str(num / 10) + ".png"
#            cv2.imwrite(img_item, frame2)  # getting image from frame2 to be rid of colorful rectangles

#        num += 1

#    print(xCenter, yCenter)  # so I can see the coordinates when issues occur (troubleshooting)
    if xCenter != 0:  # checks to see if there is a coordinate y
        if xCenter < 280:  # based on resolution 480p
            panMotor.moveDownOrRight()
        elif xCenter > 360:
            panMotor.moveLeftOrUp()

    if xCenter is 0:  # if there is no face coordinates will be (0, 0)
        panMotor.stayThere()

    if yCenter != 0:  # checks to see if there is a coordinate y
        if yCenter < 200:  # based on resolution 480p
            tiltMotor.moveDownOrRight()

        elif yCenter > 280:
            tiltMotor.moveLeftOrUp()

    if yCenter is 0:  # if there is no face coordinates will be (0, 0)
        tiltMotor.stayThere()

    cv2.imshow('frame', frame)  # show image frame with rectangle
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
