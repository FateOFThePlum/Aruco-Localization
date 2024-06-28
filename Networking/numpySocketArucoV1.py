import cv2
import numpy as np
from numpysocket import NumpySocket
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36H11)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

#Set up how the camera is distorted, These values are for one of my other cameras, I currently dont have the values for this one
cameraMatrix = np.array([[526.76855366, 0.0,          345.00788018],
                [0.0,          536.47012769, 206.32374967], 
                [0.0,          0.0,          1.0]], dtype=np.float32)
distCoeffs = np.array([[0.2778742,  -2.06991963,  0.0141893,  -0.00847357,  3.11048818]], dtype=np.float32)


markerSize = 0.1

#This is definitely going to be "Temporary"
objectPoints = np.array([
    [-markerSize/2, -markerSize/2, 0],  # Bottom left
    [ markerSize/2, -markerSize/2, 0],  # Bottom right
    [ markerSize/2,  markerSize/2, 0],  # Top right
    [-markerSize/2,  markerSize/2, 0],  # Top left
], dtype=np.float32)



def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER) #Needs to be adjusted based on the camera being used


def takePicture(): #In a function to allow for better use on the Jetson, switching cameras is easier
    ret, frame = cam.read()
    return frame 

def figureOutCameraCentricPose(markerCorners, objectPoints): 
    markerCorners = np.array(markerCorners, dtype=np.float32)
    _, rVec, tVec = cv2.solvePnP(objectPoints, markerCorners, cameraMatrix, distCoeffs)
    return rVec, tVec


with NumpySocket() as s:
    s.connect(("localhost", 9999)) #TODO: IP address will need to be configured for individual use. 
    while True: 
        frame = takePicture() #Capture the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert to greyscale because color is unneeded and takes more processing power
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)#Detect tags
        
        detectedMarkers = []
        if markerCorners:
            for x in range(len(markerCorners)):
                rVec, tVec = figureOutCameraCentricPose(markerCorners[x], objectPoints)

                detectedMarkers.append([markerIds[x][0], rVec.ravel().tolist(), tVec.ravel().tolist(), markerCorners[x][0].tolist()])

            print(detectedMarkers[0])#Is only used to help with debugging, can be removed later
        exitFrame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds, (255, 255, 0))
        exitFrame = cv2.resize(cv2.cvtColor(exitFrame, cv2.COLOR_BGR2GRAY), (0, 0), fx = 0.25, fy = 0.25)


        arrayToSend = np.array([[exitFrame], [detectedMarkers]], dtype=object)
        print(arrayToSend)
        s.sendall(arrayToSend)


cam.release()
cv2.destroyAllWindows()