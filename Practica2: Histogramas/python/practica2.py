import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def plothist(figure, img):
    plt.figure(figure)
    plt.clf()
    gray_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    plt.plot(gray_hist)
    plt.xlim([0, 256])
    plt.draw()
    plt.pause(0.01)

def acumulado(figure, img):
    gray_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # Acumulado:
    acc = 0
    H = np.zeros(256)
    for i in range(256):
        H[i] = gray_hist[i] + acc
        acc = H[i]
    plt.figure(figure)
    plt.clf()
    plt.plot(H)
    plt.draw()
    plt.pause(.001)
    return H

# ----Alpha blend---
# def alpha(x):
#     pass
#
# cv2.namedWindow('alphablend')
# cv2.createTrackbar('alpha', 'alphablend', 0, 100, alpha)

while True:

    _, src = cap.read()
    #cv2.imshow("Figura 1", src)

    ## ------Desplegar histograma-----------
    # plt.clf()
    # color = ('b', 'g', 'r')
    # for i, col in enumerate(color):
    #     histr = cv2.calcHist([src], [i], None, [256], [0, 256])
    #     plt.plot(histr, color=col)
    #     plt.xlim([0, 256])
    # plt.draw()
    # plt.pause(0.01)
    ## --------------------------------------

    ## ------Contraste brillo --------------
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # graymod = gray * 0.3 + 80
    # graymod = graymod.astype('uint8')
    #
    #
    # plothist(0, gray)
    # plothist(1, graymod)
    #
    # cv2.imshow("Gray", gray)
    # cv2.imshow("Gray_mod", graymod)
    ## ------------------------------------------

    ## -----------Adaptacion Automática-----------
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # graymod = gray * 0.3 + 80
    # graymod = graymod.astype('uint8')
    #
    # bajo = graymod.min()
    # alto = graymod.max()
    # grayad = np.zeros((gray.shape[0], gray.shape[1], 1), np.uint8)
    # for i in range(gray.shape[0]):
    #     for j in range(gray.shape[1]):
    #         grayad[i][j] = ((graymod[i][j] - bajo) / (alto - bajo) ) * 255
    # grayad = grayad.astype('uint8')
    #
    # plothist(0, graymod)
    # plothist(1, grayad)
    # cv2.imshow("fig0", graymod)
    # cv2.imshow("fig", grayad)
    ##-------------------------------------------

    ## ---------- Ecualización lineal ------------
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # H = acumulado(1, gray)
    #
    # # Ecualización
    # Ieq = np.zeros((gray.shape[0], gray.shape[1], 1), np.uint8)
    # for i in range(gray.shape[0]):
    #     for j in range(gray.shape[1]):
    #         v = gray[i][j]
    #         Ieq[i][j] = H[gray[i][j]] * (255/(gray.shape[0]*gray.shape[1]))
    #
    # # Acumulado eq:
    # acumulado(2, Ieq)
    #
    # cv2.imshow("Fig", Ieq)
    # cv2.imshow("Fig0", gray)


    # -------AlphaBlending----------
    # img = cv2.imread('lena.jpg')
    # img = cv2.resize(img, (src.shape[1], src.shape[0]))
    #
    # #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # #src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    #
    # alpha_value = (cv2.getTrackbarPos('alpha', 'alphablend') )/ 100
    #
    # outImage = cv2.addWeighted(img, alpha_value, src_gray, 1-alpha_value, 0)
    # cv2.imshow('alphablend',outImage)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
