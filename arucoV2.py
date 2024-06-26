import cv2
import numpy as np
import math


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36H11)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
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

def takePicture(): #In a function to allow for better use on the Jetson
    ret, frame = cam.read()
    return frame 

def figureOutCameraCentricPose(markerCorners, objectPoints): 
    markerCorners = np.array(markerCorners, dtype=np.float32)
    _, rVec, tVec = cv2.solvePnP(objectPoints, markerCorners, cameraMatrix, distCoeffs)
    return rVec, tVec



while True: 
    frame = takePicture()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    
    detectedMarkers = []
    if markerCorners:
        for x in range(len(markerCorners)):
            rVec, tVec = figureOutCameraCentricPose(markerCorners[x], objectPoints)

            detectedMarkers.append([markerIds[x][0], rVec.ravel().tolist(), tVec.ravel().tolist(), markerCorners[x][0].tolist()])

        print(detectedMarkers[0])
    exitFrame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds, (255, 255, 0))

    #cv2.imshow('Frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    # break

cam.release()
cv2.destroyAllWindows()
