import cv2
import numpy as np

# Define chessboard dimensions (adjust based on your board)
chessboard_size = (11, 7)  # (rows, columns)

# Prepare termination criteria for corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

# Object points (3D coordinates of corners in real world)
# You can adjust the scale based on your actual checkerboard dimensions (in mm or cm)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# List to store object points and image points from all the captured images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Capture video or images from a camera
cap = cv2.VideoCapture(0)  # Change 0 to video file path if using pre-recorded video

while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # If found, refine corner detection and draw corners
    if ret:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners.reshape(-1, 2))
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)

    # Display the resulting frame
    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xFF

    # Press 'q' to quit
    if k == ord('q'):
        break

# Release capture and close windows
cap.release()
cv2.destroyAllWindows()

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print the camera matrix and distortion coefficients
print("Camera matrix:")
print(mtx)
print("\nDistortion coefficients:")
print(dist)

# Extract fx, fy, cx, cy from the camera matrix
fx = mtx[0, 0]
fy = mtx[1, 1]
cx = mtx[0, 2]
cy = mtx[1, 2]

# Print the intrinsic parameters
print("\nfx:", fx)
print("fy:", fy)
print("cx:", cx)
print("cy:", cy)