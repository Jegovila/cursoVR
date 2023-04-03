import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

Iroi = cv2.imread('Practica6/crop.jpeg')
b, g, r = cv2.split(Iroi)

# Media
# Ar = np.mean(Iroi[:,:,2])    # recordar que es -> BGR
Ar = np.mean(r)
Ag = np.mean(g)
Ab = np.mean(b)

# Convertir a double
Rd = r.astype(np.float64)
Gd = g.astype(np.float64)
Bd = b.astype(np.float64)

# std
Dr = np.std(Rd)
Dg = np.std(Gd)
Db = np.std(Bd)

_, I = cap.read()
m, n, o = I.shape
s = 4
while True:
    _, I = cap.read()
    Ig = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    IBW = np.zeros((m, n), dtype=np.uint8)

    for i in range(m):
        for j in range(n):
            if ((Ar + s * Dr) > I[i, j, 2] > (Ar - s * Dr) and
                    (Ag + s * Dg) > I[i, j, 1] > (Ag - s * Dg) and
                    (Ab + s * Db) > I[i, j, 0] > (Ab - s * Db)):
                IBW[i, j] = 255
            else:
                IBW[i, j] = 0

    try:
        white_pixels = np.array(np.where(IBW == 255))
        min_fila = np.min(white_pixels[0, :])
        min_col = np.min(white_pixels[1, :])
        max_fila = np.max(white_pixels[0, :])
        max_col = np.max(white_pixels[1, :])
        start = [min_col, min_fila]
        end = [max_col, max_fila]
        # image = cv2.rectangle(image, start_point, end_point, color, thickness)
        I = cv2.rectangle(I, start, end, (0, 255, 0), 2)

        center2 = min_fila + (max_fila - min_fila) / 2
        center1 = min_col + (max_col - min_col) / 2
        # image = cv.circle(image, centerOfCircle, radius, color, thickness)
        I = cv2.circle(I, [int(center1), int(center2)], 10, (0, 255, 255), -1)
    except:
        pass

    cv2.imshow("Deteccion", I)
    cv2.imshow('ibw',IBW)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

