import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) #Establecer manual
#cap.set(cv2.CAP_PROP_EXPOSURE, -5) #Establecer exposición

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Trackbars
def iter_erode(x):
	pass
def iter_dilate(x):
	pass
cv2.namedWindow('Modificada')
cv2.createTrackbar('Erosion', 'Modificada', 0, 20, iter_erode)
cv2.namedWindow('Modificada')
cv2.createTrackbar('Dilatacion', 'Modificada', 0, 20, iter_dilate)



# # Tomar imágen de referencia y generar el detector
# while True:
#     _, I = cap.read()
#     Ig_ref = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
#
#     cv2.imshow("Referencia", Ig_ref)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#
#
# params = cv2.SimpleBlobDetector_Params()
# # # Change thresholds
# # params.minThreshold = 10
# # params.maxThreshold = 200
#
# # Filter by Area.
# params.filterByArea = False
# params.minArea = 15
#
# # Filter by Circularity
# params.filterByCircularity = False
# params.minCircularity = 0.1
#
# # Filter by Convexity
# params.filterByConvexity = False
# params.minConvexity = 0.87
#
# # Filter by Inertia
# params.filterByInertia = False
# params.minInertiaRatio = 0.01
#
# # Create a detector with the parameters
# detector = cv2.SimpleBlobDetector_create(params)
# # ----------------------------

kernel = np.ones((5, 5), np.uint8)

while True:

    _, src = cap.read()                                             # Leer
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)                     # Escala grises
    _, src_bin = cv2.threshold(src, 80, 255, cv2.THRESH_BINARY)     # Binaria
    cv2.imshow("Original", src_bin)

    # # Erosión y dilatación
    # iter_erode = cv2.getTrackbarPos('Erosion', 'Modificada')
    # im_out = cv2.erode(src_bin, kernel, iterations=iter_erode)      # Erosion
    # iter_dilate = cv2.getTrackbarPos('Dilatacion', 'Modificada')
    # im_out = cv2.dilate(im_out, kernel, iterations=iter_dilate)    # Dilatacion
    # cv2.imshow("Modificada", im_out)

    # # Apertura
    # im_open1 = cv2.morphologyEx(src_bin, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("Apertura 1 vez", im_open1)
    #
    # im_open3 = cv2.morphologyEx(src_bin, cv2.MORPH_OPEN, kernel)
    # im_open3 = cv2.morphologyEx(im_open3, cv2.MORPH_OPEN, kernel)
    # im_open3 = cv2.morphologyEx(im_open3, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("Apertura 3 veces", im_open3)
    #
    # # Cierre
    # im_close = cv2.morphologyEx(src_bin, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Cierre", im_close)


    ## ----------- Detección de bordes ----------------
    # srcE = cv2.erode(src_bin, kernel, iterations=1)
    # srcE_inv = cv2.bitwise_not(srcE)
    # I_bordes = cv2.bitwise_and(srcE_inv, src_bin)
    # cv2.imshow("Bordes", I_bordes)


    # ------------ PRACTICA ---------------------
    # I_diff = np.abs(Ig_ref - src)
    # _, I_diff_bin = cv2.threshold(I_diff, 80, 255, cv2.THRESH_BINARY)
    # 
    # im_salida = cv2.erode(I_diff_bin, kernel, iterations=3)
    # im_salida = cv2.dilate(im_salida, kernel, iterations=6)
    #
    # im_salida = cv2.bitwise_not(im_salida)        # Detecta los blobs negros
    # keypoints = detector.detect(im_salida)
    # nblobs = len(keypoints)
    # print(nblobs)
    # im_with_keypoints = cv2.drawKeypoints(src, keypoints, np.array([]), (255, 0, 0),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("Out", im_salida)
    # cv2.imshow("ImKeypoints", im_with_keypoints)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break