import cv2

class Cascades:
    def __init__(self, name, cascadeclassifier):
        self.__name = name  #consider if it gets in the way/necessary
        self.__cascade = cv2.CascadeClassifier(cascadeclassifier)

    def returnClassifier(self):
        return self.__cascade

    def setupMultiScaleDetection(self, grayFrame, scaleFactor=1.5, minNeighbors=5):
        return self.__cascade.detectMultiScale(grayFrame, scaleFactor, minNeighbors)

    def createROI(self, visualframe, grayframe):
        for (x, y, w, h) in self.setupMultiScaleDetection(grayframe):
            self.roi_color_face = visualframe[y:y + h, x:x + w]
            self.end_cord_x = x + w  # specifying lower corner coordinates of roi rectangle
            self.end_cord_y = y + h

    #def createRect(self):

    #def takeImage(self):
