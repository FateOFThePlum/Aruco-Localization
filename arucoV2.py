import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)

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

            detectedMarkers.append([markerIds[x].ravel().tolist(), rVec.ravel().tolist(), tVec.ravel().tolist(), markerCorners[x].ravel().tolist()])

        print(detectedMarkers[0])
    exitFrame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds, (255, 255, 0))

    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()