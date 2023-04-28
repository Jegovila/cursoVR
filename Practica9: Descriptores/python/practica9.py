import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

akaze = cv2.AKAZE_create()

while True:
    _, I1 = cap.read()
    cv2.imshow("I1", I1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


while True:
    _, I2 = cap.read()
    cv2.imshow("I2", I2)

    kpts1, desc1 = akaze.detectAndCompute(I1, None)
    kpts2, desc2 = akaze.detectAndCompute(I2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)

    ## Ordenarlos por distancia y mostrar con drawMatches los mejores
    ## ej. matches[:10].
    matches = sorted(matches, key=lambda x: x.distance)

    ## Crear un nuevo arreglo donde solo se guarden los que
    ## hagan un mejor match basado en la distancia
    ## Después drawMatches con el arreglo completo good_matches
    # good_matches = []
    # for m in matches:
    #     if m.distance < 0.9:
    #         good_matches.append(m)

    I3 = cv2.drawMatches(I1, kpts1, I2, kpts2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imshow("AKAZE matching", I3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
