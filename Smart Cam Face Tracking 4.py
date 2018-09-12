import cv2
from Classes2 import Motor, Detector

# initializes two objects of the class motor
panMotor = Motor(0)
tiltMotor = Motor(1)

# creates Detection object
face = Detector("face_alt", "haarcascade_frontalface_alt.xml")
# Detector("face_alt", "haarcascade_frontalface_alt.xml") # different face cascade classifier
# Detector("face_alt_2", "haarcascade_frontalface_alt2.xml")    # different face cascade classifier

cap = cv2.VideoCapture(1)   # change to 1 for usb cam, begins video capture


while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected)
    ret, frame = cap.read()  # used for showing window with rectangles
    # ret, frame2 = cap.read()  # used for taking images w/o rectangles
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # frame must be gray-scale for haar cascade use

    if face.detectROI(gray) is ():
        xCenter = 0  # resetting variable to be so the camera doesn't continue indirection last known face was-
        yCenter = 0
    else:
        face.createRectangle(frame)
        xCenter = face.xCenterCoordinate()
        yCenter = face.yCenterCoordinate()

        if xCenter != 0:  # checks to see if there is a coordinate y
            if xCenter < 280:  # based on resolution 480p
                panMotor.moveDownOrRight()

            elif xCenter > 360:
                panMotor.moveLeftOrUp()

        else:
            panMotor.stayThere()

        if yCenter != 0:  # checks to see if there is a coordinate y
            if yCenter < 210:  # based on resolution 480p
                tiltMotor.moveDownOrRight()

            elif yCenter > 270:
                tiltMotor.moveLeftOrUp()
        else:
            tiltMotor.stayThere()

    cv2.imshow('frame', frame)  # show image frame with rectangle
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the videocapture and close windows
cap.release()
cv2.destroyAllWindows()
