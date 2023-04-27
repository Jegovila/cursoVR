import cv2
import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt
import yaml

filas = 6
cols = 8
square_size_mm = 28

scale_percent = .15 # reducción porcentaje

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((filas*cols,3), np.float32)
objp[:,:2] = np.mgrid[0:cols,0:filas].T.reshape(-1,2) * square_size_mm

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('./chessboard/*.jpg')

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
        cv.waitKey(100)

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
    x = tvecs[i][0,0]
    y = tvecs[i][1,0]
    z = tvecs[i][2,0]
    ax.scatter(x, y, z, c='r')

    #plot reference frame
    xr = [[1], [0], [0]]
    yr = [[0], [1], [0]]
    zr = [[0], [0], [1]]
    R = cv2.Rodrigues(rvecs[i])[0]

    P0 = np.transpose(R) @ xr
    P1 = np.transpose(R) @ yr
    P2 = np.transpose(R) @ zr

    ax.plot([x, x + P0[0] * 50], [y, y + P0[1] * 50], [z, z - P0[2] * 50], color='r')
    ax.plot([x, x + P1[0] * 50], [y, y + P1[1] * 50], [z, z - P1[2] * 50], color='g')
    ax.plot([x, x + P2[0] * 50], [y, y + P2[1] * 50], [z, z - P2[2] * 50], color='b')

    X, Y = np.meshgrid(np.arange(x, x + P0[0] * 50), np.arange(y, y + P1[1] * 25))
    Z = -1 * (((-P2[0]*(X-x)-P2[1]*(Y-y))/P2[2])-z)
    #plt.contour(X, Y, Z, colors='black');
    ax.plot_surface(X, Y, Z, alpha=0.5)

# Graficar cámara
s = 20
ax.plot([-s, -s],[-s,-s],[-s, s],color='b')
ax.plot([s, s],[-s,-s],[-s, s],color='b')
ax.plot([-s, -s],[s,s],[-s, s],color='b')
ax.plot([s, s],[s,s],[-s, s],color='b')

ax.plot([-s, s],[-s,-s],[-s, -s],color='b')
ax.plot([s, s],[-s,s],[-s, -s],color='b')
ax.plot([-s, s],[s,s],[-s, -s],color='b')
ax.plot([-s, -s],[-s,s],[-s, -s],color='b')

ax.plot([-s, s],[-s,-s],[s, s],color='b')
ax.plot([s, s],[-s,s],[s, s],color='b')
ax.plot([-s, s],[s,s],[s, s],color='b')
ax.plot([-s, -s],[-s,s],[s, s],color='b')

ax.plot([-s, -1.5*s],[-s,-1.5*s],[s, 1.5*s],color='b')
ax.plot([s, 1.5*s],[-s,-1.5*s],[s, 1.5*s],color='b')
ax.plot([s, 1.5*s],[s,1.5*s],[s, 1.5*s],color='b')
ax.plot([-s, -1.5*s],[s,1.5*s],[s, 1.5*s],color='b')

ax.plot([-1.5*s, 1.5*s],[-1.5*s,-1.5*s],[1.5*s, 1.5*s],color='b')
ax.plot([1.5*s,1.5*s],[-1.5*s,1.5*s],[1.5*s, 1.5*s],color='b')
ax.plot([1.5*s, -1.5*s],[1.5*s,1.5*s],[1.5*s, 1.5*s],color='b')
ax.plot([-1.5*s,-1.5*s],[-1.5*s,1.5*s],[1.5*s, 1.5*s],color='b')

ax.scatter(0, 0, 0, c='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

elev = 0
azim = 65
ax.view_init(elev, azim)


plt.show()

print('ax.azim {}'.format(ax.azim))
print('ax.elev {}'.format(ax.elev))

#cv.waitKey(0)