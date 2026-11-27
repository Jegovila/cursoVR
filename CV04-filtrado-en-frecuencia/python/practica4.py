import cv2
import numpy as np
import matplotlib.pyplot as plt

I = cv2.imread('Practica4/bars.jpg', cv2.IMREAD_GRAYSCALE)
F = np.fft.fft2(I)
Fshift = np.fft.fftshift(F)

cv2.imshow("I", I)

plt.figure("F")
plt.imshow(np.log1p(np.abs(F)), cmap='gray')

cv2.imshow("I shift", np.fft.fftshift(I))

plt.figure("F shift")
plt.imshow(np.log1p(np.abs(Fshift)), cmap='gray')

## Filtro
M, N = F.shape
H = np.zeros((M, N), dtype=np.float32)
D0 = 100
for u in range(M):
    for v in range(N):
        D = np.sqrt((u - M/2)**2 + (v - N/2)**2)
        # ----Pasa bajas ideal-----
        # if D <= D0:
        #     H[u, v] = 1
        # else:
        #     H[u, v] = 0
        # ----Pasa altas ideal----
        if D <= D0:
            H[u, v] = 0
        else:
            H[u, v] = 1
plt.figure("H")
plt.imshow(H, cmap='gray')
plt.axis('off')

Gshift = Fshift * H #Filtradoq

plt.figure("G shift")
plt.imshow(np.log1p(np.abs(Gshift)), cmap='gray')

G = np.fft.fftshift(Gshift)
plt.figure("G")
plt.imshow(np.log1p(np.abs(G)), cmap='gray')

g = np.abs(np.fft.ifft2(G))
plt.figure("g")
plt.imshow(g, cmap='gray')

plt.show()

#cv2.waitKey(0)






# --- Alternativa Filtro box
# I = cv2.imread('Practica4/lena.png', cv2.IMREAD_GRAYSCALE)
# F = np.fft.fft2(I)
# Fshift = np.fft.fftshift(F)
#
# cv2.imshow("I", I)
#
# plt.figure("F")
# plt.imshow(np.log1p(np.abs(F)), cmap='gray')
#
# M, N = F.shape
# H = np.zeros((M, N), dtype=np.float32)
# n = 15
# H[0:n, 0:n] = 1/(n*n)
# plt.figure("h")
# plt.imshow(np.real(H), cmap='gray')
#
# H = np.fft.fft2(H)
# plt.figure("H")
# plt.imshow(np.real(np.fft.fftshift(H)), cmap='gray')
#
# G = F * H #Filtradoq
#
# plt.figure("G")
# plt.imshow(np.log1p(np.abs(np.fft.fftshift(G))), cmap='gray')
#
# g = np.abs(np.fft.ifft2(G))
# plt.figure("g")
# plt.imshow(g, cmap='gray')
#
# plt.show()

