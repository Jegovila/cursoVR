import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt

filas = 6
cols = 8
square_size_mm = 28

scale_percent = .15 # reducción porcentaje

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((filas*cols,3), np.float32)
objp[:,:2] = np.mgrid[0:cols,0:filas].T.reshape(-1,2) * square_size_mm

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('G:/Mi unidad/clases/vision robotica/10 Modelo pinhole/cal2/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (cols,filas), None)

    # Si encuentra el patrón
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Dibuja las esquinas
        cv.drawChessboardCorners(img, (cols,filas), corners2, ret)
        cv.imshow('img', cv.resize(img,(int(img.shape[1] * scale_percent),int(img.shape[0] * scale_percent))))
        cv.waitKey(500)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv.imread(images[0])
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h)) # alpha = 1 : zona sin distorsión

# Rectificar
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imshow('imagen rectificada', cv.resize(dst,(int(dst.shape[1] * 2 * scale_percent),int(dst.shape[0] * 2 *scale_percent))))

print("K = ", mtx)
print("Parámetros de distorsión = ", dist)
print("Vectores R: ", len(rvecs))
print("R: ", rvecs)
print("Vectores t: ", len(tvecs))
print("t: ", tvecs)


ax = plt.figure().add_subplot(projection='3d')
for i in range(len(tvecs)):
    ax.scatter(tvecs[i][0,0], tvecs[i][1,0], tvecs[i][2,0], c='r')
ax.scatter(0, 0, 0, c='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

cv.waitKey(0)