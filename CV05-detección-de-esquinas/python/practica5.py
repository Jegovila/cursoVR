import cv2
import numpy as np
import matplotlib.pyplot as plt

# trackbar callback fucntion (Necesaria para el trackbar)
def alpha(x):
	pass
def th(x):
    pass
def bloque(x):
    pass
cv2.namedWindow('I')
cv2.createTrackbar('alpha', 'I', 5, 10, alpha)
cv2.createTrackbar('th', 'I', 50, 100, th)
cv2.createTrackbar('bloque', 'I', 10, 50, bloque)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ----- BOX -----
n = 17
h = np.ones((n, n), np.float32)/(n*n)
# ----Sobel------
hx = np.matrix('-1 0 1;-2 0 2;-1 0 1')
hy = np.matrix('-1 -2 -1;0 0 0;1 2 1')
# ----- Gauss ----
hg = np.matrix('1 4 6 4 1;4 16 24 16 4;6 24 36 24 6;4 16 24 16 4;1 4 6 4 1')
hg = hg * (1/256)

_, I = cap.read()
Ig = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
M, N = Ig.shape

while True:
    alpha = int(cv2.getTrackbarPos('alpha', 'I')) / 1000  # Leer alpha del trackbar
    th = cv2.getTrackbarPos('th', 'I')                     # Leer th del trackbar
    bloque = cv2.getTrackbarPos('bloque', 'I')  # Leer vecindario del trackbar

    # Leer imagen
    _, I = cap.read()
    Ig = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    Ig = Ig.astype(np.float64) # convertir a float, de lo contrario los calculos se redondean

    # Crear la imagen en blanco dentro de while
    # para borrar las marcas en cada ciclo
    S = np.zeros((M, N), dtype=np.float64)

    # Suavizado
    Ig = cv2.filter2D(Ig, -1, h)

    # Derivadas
    Ix = cv2.filter2D(Ig, -1, hx)
    Iy = cv2.filter2D(Ig, -1, hy)
    # Ixx = cv2.filter2D(Ix, -1, hx)

    HE11 = np.multiply(Ix,Ix)
    HE22 = np.multiply(Iy,Iy)
    HE12 = np.multiply(Ix,Iy)

    A = cv2.filter2D(HE11, -1, hg)
    B = cv2.filter2D(HE22, -1, hg)
    C = cv2.filter2D(HE12, -1, hg)

    V = (A * B) - (C**2) - alpha * ((A * B) * (A * B))
    #V = np.multiply(A, B) - np.multiply(C, C) - alpha * np.multiply(np.multiply(A, B), np.multiply(A, B))
    #ret, U = cv2.threshold(V, th, 255, cv2.THRESH_BINARY)
    U = V > th

    if bloque == 0:
        bloque = 1
    vecindad = bloque

    for r in range(M):
        for c in range(N):
            if U[r, c]:
                I1 = np.array([r - vecindad, 0])
                I2 = np.array([r + vecindad, M])
                I3 = np.array([c - vecindad, 0])
                I4 = np.array([c + vecindad, N])

                datxi = np.max(I1)
                datxs = np.min(I2)
                datyi = np.max(I3)
                datys = np.min(I4)

                MaxB = np.max(V[datxi:datxs, datyi:datys])

                if V[r, c] == MaxB:
                    S[r, c] = 1

    for r in range(M):
        for c in range(N):
            if S[r, c]:
                # cv2.drawMarker(img, (x, y), color, markerType, markerSize, thickness)
                cv2.drawMarker(I, (c, r), (0, 255, 0), cv2.MARKER_CROSS, 15, 2)


    cv2.imshow("I", I)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break