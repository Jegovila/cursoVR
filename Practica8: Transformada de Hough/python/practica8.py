import cv2
import numpy as np
import math
from skimage.transform import (hough_line, hough_line_peaks)
import matplotlib.pyplot as plt
from matplotlib import cm

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 6))

while True:

    _, src = cap.read()
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(src, 50, 200, None, 3)

    h, theta, d = hough_line(dst)
    ax0.imshow(np.log(1 + h), extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]], aspect='auto')

    ax1.imshow(src, cmap=cm.gray)
    row1, col1 = dst.shape
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - col1 * np.cos(angle)) / np.sin(angle)
        ax1.plot((0, col1), (y0, y1), '-r')
    ax1.axis((0, col1, row1, 0))
    ax1.set_title('Lineas detectadas')
    ax1.set_axis_off()

    plt.draw()
    plt.pause(0.01)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break