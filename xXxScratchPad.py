import cv2
from Classes2 import Motor, Detector

# initializes two objects of the class motor
panMotor = Motor(0)
tiltMotor = Motor(1)

#sets detection filter
face = Detector("face", "haarcascade_frontalface_default.xml")
# eyes = Detector("eyes", "haarcascade_eye.xml")
face_alt = Detector("face_alt", "haarcascade_frontalface_alt.xml")
face_alt_2 = Detector("face_alt_2", "haarcascade_frontalface_alt2.xml")

cap = cv2.VideoCapture(1)   # change to 1 for usb cam

while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cap.read()  # used for showing window with rectangles
    ret, frame2 = cap.read()  # used for taking images w/o rectangles
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # to use haar cascade, frame must be gray-scale
    faceROI = face.detectROI(gray)
    faceAltROI = face_alt.detectROI(gray)
    faceAlt2ROI = face_alt_2.detectROI(gray)
    if faceROI is() and faceAltROI is () and face_alt_2 is ():
        xCenter = 0  # resetting variable to be so the camera doesn't continue indirection last known face was-
        yCenter = 0
    else:
        #face.createRectangle(frame)
        face_alt.createRectangle(frame) # best cascade in my opinion
        #face_alt_2.createRectangle(frame)
        # eyes.detectROI(gray)
        # eyes.createRectangle(frame)
        xCenter = face_alt.xCenterCoordinate()
        yCenter = face_alt.yCenterCoordinate()

#    print(xCenter, yCenter)  # so I can see the coordinates when issues occur (troubleshooting)
    if xCenter != 0:  # checks to see if there is a coordinate y
        if xCenter < 280:  # based on resolution 480p
            panMotor.moveDownOrRight()

        elif xCenter > 360:
            panMotor.moveLeftOrUp()

    if yCenter != 0:  # checks to see if there is a coordinate y
        if yCenter < 210:  # based on resolution 480p
            tiltMotor.moveDownOrRight()

        elif yCenter > 270:
            tiltMotor.moveLeftOrUp()

    if yCenter == 0:  # if there is no face coordinates will be (0, 0)
        tiltMotor.stayThere()

    if xCenter == 0:  # if there is no face coordinates will be (0, 0)
        panMotor.stayThere()

    cv2.imshow('frame', frame)  # show image frame with rectangle
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
