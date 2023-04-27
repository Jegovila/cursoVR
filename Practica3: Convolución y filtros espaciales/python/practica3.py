import cv2
import numpy as np
import math
import random

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# ----- BOX -----
n = 7
h = np.ones((n, n), np.float32)/(n*n)

#----- Gauss ----
# h = np.matrix('1 4 6 4 1;4 16 24 16 4;6 24 36 24 6;4 16 24 16 4;1 4 6 4 1')
# h = h * (1/256)

#----Sobel------
# hx = np.matrix('-1 0 1;-2 0 2;-1 0 1')
# hy = np.matrix('-1 -2 -1;0 0 0;1 2 1')

#----Laplacian----
# hl = np.matrix('1 1 1;1 -8 1;1 1 1')

#----Mediana-----
def add_noise(img):
    row, col = img.shape
    number_of_pixels = random.randint(1000, 10000)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        img[y_coord][x_coord] = 255

    number_of_pixels = random.randint(1000, 10000)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        img[y_coord][x_coord] = 0
    return img



while True:
    _, src = cap.read()
    cv2.imshow("fig", src)

    #------Suavizado---------------
    # dst = cv2.filter2D(src, -1, h)
    # cv2.imshow("fig2", dst)

    #------Sobel--------------------
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # #gray = cv2.filter2D(gray, -1, h)
    # sx = cv2.filter2D(gray, -1, hx)
    # sy = cv2.filter2D(gray, -1, hy)
    # #sx = cv2.convertScaleAbs(sx)
    # #sy = cv2.convertScaleAbs(sy)
    # s = cv2.addWeighted(sx, 0.5, sy, 0.5, 0)
    #
    # s = cv2.inRange(s,50,255)
    # cv2.imshow("fig2", s)

    #----------Laplace------------
    # # --- sin suavizar
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # dst = cv2.filter2D(gray, -1, hl)
    # dst = cv2.inRange(dst,60,255)
    # cv2.imshow("fig2", dst)
    #
    # # --- Suavizada
    # gray_s = cv2.filter2D(gray, -1, h)
    # dst_s= cv2.filter2D(gray_s, -1, hl)
    # dst_s = cv2.inRange(dst_s,15,255)
    # cv2.imshow("fig3", dst_s)

    #---------Mediana---------------
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # ruido = add_noise(gray)
    # cv2.imshow("fig2",ruido)
    # dst = cv2.medianBlur(ruido, 3)
    # cv2.imshow("fig3",dst)


    if cv2.waitKey(1) == ord('q'):
        break