import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Tomar captura para calcular tamaño
# y generar imagen destino
_, src = cap.read()
dimensions = src.shape
dst = np.zeros((dimensions[0] + 200,dimensions[1] + 200,1), np.uint8)
theta = 0
t = 0


# trackbar callback fucntion (Necesaria para el trackbar)
def rot(x):
	pass
def trans(x):
    pass
cv2.namedWindow('Figura 2')
cv2.createTrackbar('theta', 'Figura 2', 0, 700, rot)
cv2.createTrackbar('t', 'Figura 2', 0, 200, trans)

while True:

    _, src = cap.read()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Figura 1", gray)
    dst = np.zeros((dimensions[0] + 200, dimensions[1] + 200, 1), np.uint8)

    theta = int(cv2.getTrackbarPos('theta', 'Figura 2')) / 100  # Leer theta del trackbar
    t = cv2.getTrackbarPos('t', 'Figura 2')                     # Leer traslación del trackbar

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            x = (math.ceil(i * math.cos(theta) + j * math.sin(theta)))
            y = (math.ceil(-i * math.sin(theta) + j * math.cos(theta)))

            # Evitar salir de los límites
            if x + t > dst.shape[0]-1:
                x = dst.shape[0]-t-1
            if y + t > dst.shape[1]-1:
                y = dst.shape[1]-t-1
            if x + t < 0:
                x = 0
            if y + t < 0:
                y = 0

            dst[x + t][y + t] = gray[i][j]

    # Usando las funciones de opencv
    # scale = 100
    # rows, cols = gray.shape
    # M = np.float32([[1, 0, t], [0, 1, t]])
    # dst = cv2.warpAffine(src, M, (cols, rows))
    # R = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), theta, 1)
    # dst = cv2.warpAffine(dst, R, (cols, rows))

    # width = int(gray.shape[1] * scale / 100)
    # height = int(gray.shape[0] * scale / 100)
    # dim = (width, height)
    # dst = cv2.resize(dst, dim, interpolation=cv2.INTER_AREA)

	
    # Rellenar espacios negros
    # for i in range(dst.shape[0]-1):
    #     for j in range(dst.shape[1]-1):
    #         if dst[i][j] == 0:
    #             dst[i][j] = dst[i][j+1]

    cv2.imshow("Figura 2", dst)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
