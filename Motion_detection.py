import cv2, time
from Classes_Final import Motor, Detector, Camera, Motion

face_alt = Detector("face_alt", "haarcascade_frontalface_alt.xml")
panMotor = Motor(0)
tiltMotor = Motor(1)
cam = Camera(1)
motion = Motion(None)

static_back = motion.setupStaticBack()

start = time.time()

video = cam.setupVideo()

while True:
    xCenter = 0
    yCenter = 0
    ret, frame = video.read()
    gray = cam.setupGrayFRame(frame)

    gray = motion.setupGaussianBlur(gray)
    motion_counter = 0
    if static_back is None:
        static_back = gray
        continue

    if (abs( start - time.time())>2):
        static_back = gray
        print(time.time())
        start = time.time()

    motion.returnDiff(static_back, gray)
    motion.setThreshold()

    (_, cnts, _) = motion.findContours()

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.imshow(cv2.boundingRect(contour))
        xCenter = (x + (x + w)) / 2
        yCenter = (y + (y + h)) / 2
        print(xCenter, yCenter)

#    if xCenter != 0:  # checks to see if there is a coordinate y
#        if xCenter < 300:  # based on resolution 480p
#            panMotor.moveDownOrRight()

#        elif xCenter > 340:
#            panMotor.moveLeftOrUp()

#    if yCenter != 0:  # checks to see if there is a coordinate y
#        if yCenter < 220:  # based on resolution 480p
#            tiltMotor.moveDownOrRight()

#        elif yCenter > 260:
#            tiltMotor.moveLeftOrUp()

#        if yCenter == 0:  # if there is no face coordinates will be (0, 0)
#            tiltMotor.stayThere()

    if xCenter == 0:  # if there is no face coordinates will be (0, 0)
        panMotor.stayThere()
    cv2.imshow("Search Frame", frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

video.release()

cv2.destroyAllWindows()