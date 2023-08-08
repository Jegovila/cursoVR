import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



# Equalize Histogram of Color Images
def equalize_histogram_color(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img

# Calibration or intrinsic matrix (obtained with Zhang method)
K = np.array([[3422.9,      0, 3111.07],
              [0,     3421.53, 2055.06],
              [0,           0,       1]], dtype=np.float)

# Get a pair of images of the same object form different viewpoint
img1 = cv2.imread('Obs11.jpg')
img2 = cv2.imread('Obs12.jpg')

# Equalize histogram
img1 = equalize_histogram_color(img1)
img2 = equalize_histogram_color(img2)

# Gray-scale image
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Detection and description of key-points with AKAZE technique
detector = cv2.AKAZE_create()
k1, d1 = detector.detectAndCompute(gray1, None)
k2, d2 = detector.detectAndCompute(gray2, None)

# Brute-force matcher on the descriptors
bf = cv2.BFMatcher()
matches = bf.knnMatch(d1, d2, k=2)

# Make sure that the matches are good
verify_ratio = 0.9
verified_matches = []
for m1, m2 in matches:
    # Add to array only if it's a good match
    if m1.distance < verify_ratio * m2.distance:
        verified_matches.append(m1)

# Minimum number of matches
min_matches = 8
if len(verified_matches) > min_matches:

    # Array to store matching points
    img1_pts = []
    img2_pts = []

    # Add matching points to array
    for match in verified_matches:
        img1_pts.append(k1[match.queryIdx].pt)
        img2_pts.append(k2[match.trainIdx].pt)
    pts1 = np.float32(img1_pts).reshape(-1, 1, 2)
    pts2 = np.float32(img2_pts).reshape(-1, 1, 2)

# Calculate Fundamental Matrix with RANSAC or 8-point algorithm or LMEDS
# cv2.FM_LMEDS or cv2.FM_8POINT or cv2.FM_RANSAC
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
print("The fundamental matrix is \n" + str(F))

# Select only in-lier points
pts1 = pts1[mask.ravel() == 1]
pts2 = pts2[mask.ravel() == 1]

# Calculate Essential matrix using the intrinsic calibration
E = np.matmul(np.matmul(np.transpose(K), F), K)
print("The essential matrix is \n" + str(E))

# Extract extrinsic parameters
_, R, t, _ = cv2.recoverPose(E, pts1, pts2, K)
print("The rotation matrix is \n" + str(R))
print("The translation is \n" + str(t))

# Calculate camera (projection) matrix for view 1
P1 = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0]])
P1 = np.matmul(K, P1)
print("The projection matrix 1 \n" + str(P1))

# Calculate camera (projection) matrix for view 2
P2 = np.empty((3, 4))
P2[:3, :3] = R
P2[:3, 3] = t.ravel()
P2 = np.matmul(K, P2)
print("The projection matrix 2 \n" + str(P2))


# Triangulate points with least mean squares
points_3d = cv2.triangulatePoints(P1, P2, pts1, pts2)
points_3d /= points_3d[3]


# For each point obtain the image color
color = []
for i in range(pts1.shape[0]):
    color.append(tuple(img2[int(pts1[i][0][1]),
                            int(pts1[i][0][0])]/255))

# Draw points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points_3d[0], points_3d[1], points_3d[2], c=color)
ax.axes.set_xlim3d(left=-5, right=5)
ax.axes.set_ylim3d(bottom=-5, top=5)
ax.axes.set_zlim3d(bottom=0, top=10)
plt.show()
