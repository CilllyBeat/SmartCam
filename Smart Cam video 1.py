#credit: www.codingforentrepreneurs.com/blog/
import os #import operating system?
import numpy as np      #"NumPy is the fundamental package for scientific computing with Python"
import cv2



#video storage - recording
filename = 'video.avi'  #.avi or .mpa or....? whatever videofile extension u want + possible
frames_per_seconds = 24.0   #24 frames /sec - movies typically do 24
resolution  = '480p'    #default resolution - not very good resolution on camera - could do 720p or 1080p if had better camera



def change_res(cap, width, height):
    cap.set(3, width)   #x axis pixel amount
    cap.set(4, height)  #y axis pixel amount

# dictionary for standard resolutions
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}
    #funcition that sets the defalut resolution to 420p if resolution variable
    # input does not match the dictionary (ensures standards are kept)
def get_dimensions(cap, res):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:   #if res is in STD_DIMENSIONS list then
        width, height = STD_DIMENSIONS[res] #width and height is equal to res (to check if res is in the list)
    change_res(cap, width, height)
    return width, height



# dictionary of videotypes. more codecs at www.fourcc.org/codecs.php . WVID seems to work well windows/mac
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

# checking if extension is in dictionary and sets default type?
def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']




#setting up video capture as cap variable
cap = cv2.VideoCapture(1)   #no. 0 would be integrated webcam, primary device. USB webcam is no. 1
dims = get_dimensions(cap, res=resolution)  #changes resolution to default resolution
video_type_cv2 = get_video_type(filename)   #defining video type (in filename)

out = cv2.VideoWriter(filename, video_type_cv2, frames_per_seconds, dims)






while True:     #might use parenthesis around True - don't know if significant later on
    ret, frame = cap.read() #reading/capture frame by frame
    out.write(frame)    #writes out frames to videofile

    cv2.imshow('video input', frame) #show images/display frame, note im not img
    if cv2.waitKey(20) & 0xFF == ord('q'):   #to break window by pressing q having marked the frame
        break

cap.release()               #releases capture upon leaving while-loop (pressing q)
out.release()               #releases video upon leaving while-loop (pressing q)
cv2.destroyAllWindows()     #NB don't know what it does!!!!