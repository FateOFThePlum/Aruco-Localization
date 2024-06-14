import cv2
import pyapriltags
import numpy as np
import math

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera Feed")

at_detector = pyapriltags.Detector(searchpath=['apriltags'],
                       families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

cameraDistortion = [913.5581151790648, 904.7723702396544, 312.9039783468111, 254.74711910863437]

viewPortSize = 1000
arrowDistance = 50


def viewPort(coordinates, rot, frame):
    shape = frame.shape
    img = np.zeros((shape[0], shape[0], 3), np.uint8)

    coordinates = tuple(int((shape[0]/viewPortSize) * elem) for elem in coordinates) #Scales the coordinates into pixels with regard to the viewport size and the size of the window
    coordinates = tuple(int(elem+(shape[0]/2)) for elem in coordinates) #Adjusts the ogrin from center to top left because opencv works with positive coordinates only

    #Calculate arrow end position
    x_offset = arrowDistance * math.cos(rot)
    y_offset = arrowDistance * math.sin(rot)
    end_point = (int(coordinates[0] + x_offset), int(coordinates[1] + y_offset))

    img = cv2.arrowedLine(img, coordinates, end_point, (255, 255, 0), thickness=2)
    return img

def rotationMatrixToDegrees(matrix): #Don't Ask me to explain this cause I took the math of this off of the OPENCV website
    roll = np.arctan2(matrix[1, 0], matrix[0, 0])
    yaw = np.arcsin(-matrix[2, 0])
    pitch = np.arctan2(matrix[2, 1], matrix[2, 2])


    return roll, pitch, yaw


while True:
    ret, frame = cam.read()
    if not ret:
        print("ERROR: CHECK CAMERA CONNECTION")
        break

    cv2.imshow("Camera Feed", frame)

    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wait for a key press (1 ms delay)
    key = cv2.waitKey(1)

    tags = at_detector.detect(greyFrame, estimate_tag_pose=True, camera_params=cameraDistortion, tag_size=100)
    if tags:
        #print(tags[0][7])
        print("---------------------------------------------")
        cv2.imshow("Found", cv2.polylines(frame, [tags[0][6].astype(np.int32)], True, (255, 0, 255), 2))#Displays Colored Version
        roll, pitch, yaw = rotationMatrixToDegrees(tags[0][7])#Get the angles of the april tag in radians
        cv2.imshow("ViewPort", viewPort((tags[0][8][0], tags[0][8][1]), roll, frame))



    if key % 256 == 27:
        print("Escape key pressed. Closing...")
        break

# Release the camera and close the window
cam.release()
cv2.destroyAllWindows()