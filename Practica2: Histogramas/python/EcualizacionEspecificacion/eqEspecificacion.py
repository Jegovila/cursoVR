import cv2
import numpy as np
from matplotlib import pyplot as plt


def acumulado(img, figure):
    color = ('b', 'g', 'r')
    H = np.zeros([256, 3])
    for i, col in enumerate(color):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        # Acumulado:
        acc = 0
        for j in range(256):
            H[j][i] = hist[j] + acc
            acc = H[j][i]
        #Normalizado
        H[:,i] = H[:,i] / (img.shape[0] * img.shape[1])
        plt.figure(figure)
        plt.plot(H[:,i],color=col)
        plt.draw()
        plt.pause(.001)
    return H


I2 = cv2.imread('im1.jpg')
I1 = cv2.imread('im2.jpg')

H1 = acumulado(I1, 1)
H2 = acumulado(I2, 2)

[m, n, p] = I1.shape
I3 = np.zeros([m, n, p])
# for k in range(p):
#     for i in range(256):
#         H1[i, k] = np.round(H1[i, k] * 255)
#         H2[i, k] = np.round(H2[i, k] * 255)
#--------Ecualización por especificación----------
for k in range(p):
    for i in range(m):
        for j in range(n):
            z = 0
            Sk = H1[I1[i, j, k], k]
            while H2[z, k] - Sk < 0:
                z += 1
                if z == 256:
                    H2[z, k] = Sk
            I3[i, j, k] = z

I3 = I3.astype('uint8')
H3 = acumulado(I2, 3)

cv2.imshow("Imagen 1", I1)
cv2.imshow("Imagen 2", I2)
cv2.imshow("Imagen 3", I3)


cv2.waitKey(0)


