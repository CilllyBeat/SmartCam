import numpy as np
import cv2

# had major trouble referencing a classifier if it wansn't on same directory level as code
#  - couldn't decipher path to classifier in data folder so it said the module was "empty"
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")


cap = cv2.VideoCapture(1)

color = (0, 255, 0)  # BGR blue green red, not RGB red green blue, color of rectangle
stroke = 2  # rectangle frame thickness
num = 0 #counter for pictures
centre = 0

while(True):
    # Capture frame-by-frame, one color for visual with rectangles showing, one for color visual without the
    # distracting rectangle (from which images will be collected
    ret, frame = cap.read()
    ret, frame2 = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #what is scale factor min neighbor????
    for (x, y, w, h) in faces:
#        print(x, y, w, h)  #to test if it sees the face
#        roi_gray = gray[y:y+h, x:x+w]   # starting at y coordinate start (top left corner -> lower y coordinate (y plus height)
        roi_color_face = frame[y:y + h, x:x + w]
#        img_item = "my_img.png"     # consider storing in other format?
#        cv2.imwrite(img_item, roi_gray) #saves only roi of the image
#        cv2.imwrite(img_item, roi_color_face)

        end_cord_x = x+w #specifying lower corner cordinates of roi rectangle
        end_cord_y = y+h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)   #object, start coordinates, end cooordinates, color rectangle, stroke thickness

        centreX = x+(w/2)
        centreY = y+(h/2)
        centre = (centreX, centreY) #centre value x,y of centre rectangle

        eyes = eyes_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (ex, ey, ew, eh) in eyes:
            roi_color_eyes = frame[ey:ey + eh, ex:ex + ew]

            end_cord_ex = ex+ew
            end_cord_ey = ey+eh
            cv2.rectangle(frame, (ex,ey), (end_cord_ex, end_cord_ey), color, stroke)

#            if num in range(0,100,10):  #for every image between 0 and 100 with increments of 10
#                img_item = "my_img" + str(num/10) + ".png"
#                cv2.imwrite(img_item,frame2)  # getting image from frame2 to be rid of colorful facial detection rectangles

#            num += 1
    # Display the resulting frame
    print(centre)
    cv2.imshow('frame',frame)
#    cv2.imshow('gray',gray) # needed for detection but not or showing

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()