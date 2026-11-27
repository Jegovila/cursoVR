import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt

# Function for stereo vision and depth estimation
import calibration


# def nothing(x):
#     pass
#
# cv2.namedWindow('disp', cv2.WINDOW_NORMAL)
#
# cv2.createTrackbar('numDisparities', 'disp', 1, 17, nothing)
# cv2.createTrackbar('blockSize', 'disp', 5, 50, nothing)
# cv2.createTrackbar('preFilterType', 'disp', 1, 1, nothing)
# cv2.createTrackbar('preFilterSize', 'disp', 2, 25, nothing)
# cv2.createTrackbar('preFilterCap', 'disp', 5, 62, nothing)
# cv2.createTrackbar('textureThreshold', 'disp', 10, 100, nothing)
# cv2.createTrackbar('uniquenessRatio', 'disp', 15, 100, nothing)
# cv2.createTrackbar('speckleRange', 'disp', 0, 100, nothing)
# cv2.createTrackbar('speckleWindowSize', 'disp', 3, 25, nothing)
# cv2.createTrackbar('disp12MaxDiff', 'disp', 5, 25, nothing)
# cv2.createTrackbar('minDisparity', 'disp', 5, 25, nothing)

# Open both cameras
cap_right = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap_left = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Enfoque manual en caso de ser necesario
cap_right.set(cv2.CAP_PROP_AUTOFOCUS, 2)
cap_left.set(cv2.CAP_PROP_AUTOFOCUS, 2)
cap_right.set(28, 0)
cap_left.set(28, 0)

stereoMatcher = cv2.StereoBM_create()


while (cap_right.isOpened() and cap_left.isOpened()):

    # # Updating the parameters based on the trackbar positions
    # numDisparities = cv2.getTrackbarPos('numDisparities','disp')*16
    # blockSize = cv2.getTrackbarPos('blockSize','disp')*2 + 5
    # preFilterType = cv2.getTrackbarPos('preFilterType','disp')
    # preFilterSize = cv2.getTrackbarPos('preFilterSize','disp')*2 + 5
    # preFilterCap = cv2.getTrackbarPos('preFilterCap','disp')
    # textureThreshold = cv2.getTrackbarPos('textureThreshold','disp')
    # uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio','disp')
    # speckleRange = cv2.getTrackbarPos('speckleRange','disp')
    # speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','disp')*2
    # disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff','disp')
    # minDisparity = cv2.getTrackbarPos('minDisparity','disp')
    #
    # # Setting the updated parameters before computing disparity map
    # stereoMatcher.setNumDisparities(numDisparities)
    # stereoMatcher.setBlockSize(blockSize)
    # stereoMatcher.setPreFilterType(preFilterType)
    # stereoMatcher.setPreFilterSize(preFilterSize)
    # stereoMatcher.setPreFilterCap(preFilterCap)
    # stereoMatcher.setTextureThreshold(textureThreshold)
    # stereoMatcher.setUniquenessRatio(uniquenessRatio)
    # stereoMatcher.setSpeckleRange(speckleRange)
    # stereoMatcher.setSpeckleWindowSize(speckleWindowSize)
    # stereoMatcher.setDisp12MaxDiff(disp12MaxDiff)
    # stereoMatcher.setMinDisparity(minDisparity)

    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    ################## CALIBRATION #########################################################
    fixedRight, fixedLeft = calibration.undistortRectify(frame_right, frame_left)
    ########################################################################################

    grayLeft = cv2.cvtColor(fixedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(fixedRight, cv2.COLOR_BGR2GRAY)
    depth = stereoMatcher.compute(grayLeft, grayRight)
    DEPTH_VISUALIZATION_SCALE = 2048
    cv2.imshow('depth', depth / DEPTH_VISUALIZATION_SCALE)
    cv2.imshow("Left", fixedLeft)
    cv2.imshow("Right", fixedRight)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()