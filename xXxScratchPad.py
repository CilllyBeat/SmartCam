import serial
import struct
import cv2

STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}
# funcition that sets the defalut resolution to 420p if resolution variable
# input does not match the dictionary (ensures standards are kept)


def get_dimensions(capture, res):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:  # if res is in STD_DIMENSIONS list then
        width, height = STD_DIMENSIONS[res]  # width and height is equal to res (to check if res is in the list)
    change_res(capture, width, height)
    return width, height


def change_res(capture, width, height):
    capture.set(3, width)  # x axis pixel amount
    capture.set(4, height)  # y axis pixel amount


resolution = '480p'


def readresponse():
    b = bytearray(b"                   ")
    ser.readinto(b)  # when the serial connection is initialized the usb-power is "flicked"
    print(b)


# for serial communication with aruino slave
port = 'COM6'
ser = serial.Serial(port, 115200, timeout=0.5)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")

cap = cv2.VideoCapture(1)
dims = get_dimensions(cap, res=resolution)

color = (0, 255, 0)  # BGR blue green red, not RGB red green blue, color of rectangle
stroke = 2  # rectangle frame thickness
num = 0  # counter for pictures

while True:
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cap.read()
    ret, frame2 = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,
                                          minNeighbors=5)  # what is scale factor min neighbor????
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

        eyes = eyes_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (ex, ey, ew, eh) in eyes:
            roi_color_eyes = frame[ey:ey + eh, ex:ex + ew]

            end_cord_ex = ex + ew
            end_cord_ey = ey + eh
            cv2.rectangle(frame, (ex, ey), (end_cord_ex, end_cord_ey), color, stroke)

            if num in range(0, 100, 10):  # for every image between 0 and 100 with increments of 10
                img_item = "my_img" + str(num / 10) + ".png"
                cv2.imwrite(img_item,
                            frame2)  # getting image from frame2 to be rid of colorful facial detection rectangles

            num += 1
    print(xCenter, yCenter)
    if xCenter != 0:
        if abs(xCenter) < 300:  # based on resolution 480p
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 1))

        elif abs(xCenter) > 340:
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 2))

        elif 300 <= abs(xCenter) <= 340:
            ser.write('0'.encode('ascii'))
            ser.write(struct.pack('>B', 3))

    if yCenter != 0:
        if abs(yCenter) < 230:  # based on resolution 480p
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 3))

        elif abs(yCenter) > 250:
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 2))

        elif 220 <= abs(yCenter) <= 260:
            ser.write('1'.encode('ascii'))
            ser.write(struct.pack('>B', 3))

    if xCenter is 0:
        ser.write('0'.encode('ascii'))
        ser.write(struct.pack('>B', 3))

    if yCenter is 0:
        ser.write('1'.encode('ascii'))
        ser.write(struct.pack('>B', 3))

    cv2.imshow('frame', frame)
    # cv2.imshow('gray',gray) # needed for detection but not or showing
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
