import cv2, time
from Classes2 import Motor, Detector, Camera

# initializing class objects
panMotor = Motor(0)
tiltMotor = Motor(1)
cam = Camera(1)
face_alt = Detector("face_alt", "haarcascade_frontalface_alt.xml")  # sets detection filter

cam.setupVideo()  # set up video capture

while True:
    # Capture frame-by-frame; gray for the detector, frame for color showing frame
    ret, frame = cam.setupFrame()
    gray = cam.setupGrayFRame(frame)

    face_alt_ROI = face_alt.detectROI(gray)

    if face_alt_ROI is():  # while an ROI doesn't exist:
        xCenter = 0  # resetting variable to be so the camera doesn't continue indirection last known face was-
        yCenter = 0
    else:   # while ROI does exist
        face_alt.createRectangle(frame)  # creates visual rectangle around roi in show-frame
        xCenter = face_alt.xCenterCoordinate()  # returns x-center of face detection
        yCenter = face_alt.yCenterCoordinate()  # returns y-center of face detection

        if xCenter != 0 or yCenter != 0:  # checks if a face is detected
            if xCenter < 280:  # based on resolution 480p (640 by 480 pixels)
                panMotor.moveDownOrRight()

            elif xCenter > 360:
                panMotor.moveLeftOrUp()

            elif yCenter < 210:  # based on resolution 480p (640 by 480 pixels)
                tiltMotor.moveDownOrRight()

            elif yCenter > 270:
                tiltMotor.moveLeftOrUp()
        else:  # for resetting the coordinates instead of using coordinates from a previous detection
            xCenter = 0
            yCenter = 0

    time.sleep(0.04)    # for adjusting frame-rate
    cv2.imshow('Face detection and tracking', frame)  # show image frame with rectangle
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cam.releaseVideo()    # When everything done, release the capture
cv2.destroyAllWindows()
