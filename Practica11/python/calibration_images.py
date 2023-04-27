import cv2


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

# Enfoque manual en caso de ser necesario
cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)
cap2.set(cv2.CAP_PROP_AUTOFOCUS, 2)
cap.set(28, 0)
cap2.set(28, 0)

num = 0


while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()


    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('./images/stereoLeft/imageL' + str(num) + '.png', img)
        cv2.imwrite('./images/stereoright/imageR' + str(num) + '.png', img2)
        num += 1
        print("images saved!", num)

    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)
