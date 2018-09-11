import cv2

class Cascades:
    def __init__(self, name, cascadeclassifier, frame, grayframe):
        self.__name = name  #consider if it gets in the way/necessary
        self.__cascade = cv2.CascadeClassifier(cascadeclassifier)
        for (x, y, w, h) in self.setupMultiScaleDetection(grayframe):
            self.h = h
            self.w = w
            self.x = x
            self.y = y
            self.end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
            self.end_cord_y = y + h
            self.roi_color_face = frame[y:y + h, x:x + w]

    def returnClassifier(self):
        return self.__cascade

    def setupMultiScaleDetection(self, grayframe, scaleFactor=1.5, minNeighbors=5):
        return self.__cascade.detectMultiScale(grayframe, scaleFactor, minNeighbors)

    def createROI(self, visualframe, grayframe):
        return self.roi_color_face

    def createRect(self, frame, color=(0, 255, 0), stroke=2):
        return cv2.rectangle(frame, (self.x, self.y), (self.end_cord_x, self.end_cord_y), color, stroke)
    # def takeImage(self):


class Cascade2:
    def __init__(self, name, cascadeclassifier, frame=None, grayframe=None):
        self.name = name
        self.cascade = cv2.CascadeClassifier(cascadeclassifier)
        self.grayframe = grayframe
        self.frame = frame
        self.multiscale = self.cascade.detectMultiScale(self.grayframe, scaleFactor=1.5, minNeighbors=5)
        self.roi = None

    def getROI(self):
        for (x, y, w, h) in self.multiscale:
            self.roi = [y:y + h, x:x + w]
            return self.roi # dnt know if necessary



class Frame:
    def __init__(self, name, capture):
        self.name = name
        self.capture = capture

    def readCapture(self):
        ret, self.name = self.capture.read()

    def changeToGray(self):
        self.name = cv2.cvtColor(self.name, cv2.COLOR_BGR2GRAY)  # to use haar cascade, frame must be grayscale

class Image:
    def __init__(self, name):
