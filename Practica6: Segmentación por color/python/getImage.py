# Despliega video y espera por "q" para hacer la captura
# con el mouse seleccionar la ROI y tecla enter

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    _, I = cap.read()
    cv2.imshow("I", I)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()

roi = cv2.selectROI(I)
print(roi)

# Seleccionar ROI de I
roi_cropped = I[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

# mostrar ROI
cv2.imshow("ROI", roi_cropped)
cv2.imwrite("Practica6/crop.jpeg", roi_cropped)

cv2.waitKey(0)