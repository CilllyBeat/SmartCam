import cv2, time
from Classes2 import Motor, Detector, Camera

# initializes two objects of the class motor
panMotor = Motor(0)
tiltMotor = Motor(1)
cam = Camera(1)

# sets detection filter
face_alt = Detector("face_alt", "haarcascade_frontalface_alt.xml")

cam.setupVideo()

while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cam.setupFrame()
    ret, frame2 = cam.setupFrame()
    gray = cam.setupGrayFRame(frame)

    faceAltROI = face_alt.detectROI(gray)

    if faceAltROI is():  # while an ROI doesn't exist:
        xCenter = 0  # resetting variable to be so the camera doesn't continue indirection last known face was-
        yCenter = 0
    else:   # while ROI does exist
        face_alt.createRectangle(frame)  # best cascade in my opinion
        xCenter = face_alt.xCenterCoordinate()
        yCenter = face_alt.yCenterCoordinate()

        if xCenter != 0 or yCenter != 0:  # checks to see if there is a coordinate y
            if xCenter < 280:  # based on resolution 480p
                panMotor.moveDownOrRight()

            elif xCenter > 360:
                panMotor.moveLeftOrUp()

            elif yCenter < 210:  # based on resolution 480p
                tiltMotor.moveDownOrRight()

            elif yCenter > 270:
                tiltMotor.moveLeftOrUp()
        else:
            xCenter = 0
            yCenter = 0

    time.sleep(0.04)    #adjusting framerate
    cv2.imshow('frame', frame)  # show image frame with rectangle
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cam.releaseCam()    # When everything done, release the capture
cv2.destroyAllWindows()
