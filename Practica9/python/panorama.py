from imutils import paths
import numpy as np
import matplotlib.pyplot as plt
import cv2

def plot_images(*imgs, figsize=(10,5), hide_ticks=False):
    '''Display one or multiple images.'''
    f = plt.figure(figsize=figsize)
    width = np.ceil(np.sqrt(len(imgs))).astype('int')
    height = np.ceil(len(imgs) / width).astype('int')
    for i, img in enumerate(imgs, 1):
        ax = f.add_subplot(height, width, i)
        if hide_ticks:
            ax.axis('off')
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


akaze = cv2.AKAZE_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Path a las imágenes
imagePaths = sorted(list(paths.list_images("./")))
images = []
images_gray = []
kpts = []
desc = []
for imagePath in imagePaths:
    image = cv2.imread(imagePath)

    scale_percent = 20  # Reducir a este porcentaje
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    images.append(image)

    keypoints, features = akaze.detectAndCompute(image, None)
    kpts.append(keypoints)
    desc.append(features)
plot_images(images[0], images[1])

# for i in range(len(images)-1):
#     matches = bf.match(desc[i], desc[i+1])
#     matches = sorted(matches, key=lambda x: x.distance)


matches = bf.match(desc[0], desc[1])
matches = sorted(matches, key=lambda x: x.distance)

keypoints_drawn_left = cv2.drawKeypoints(images[0], kpts[0], None, color=(0, 0, 255))
keypoints_drawn_right = cv2.drawKeypoints(images[1], kpts[1], None, color=(0, 0, 255))

plot_images(images[0], keypoints_drawn_left, images[1], keypoints_drawn_right)

matches_drawn = cv2.drawMatches(images[0], kpts[0], images[1], kpts[1], matches[:100], None, matchColor=(0,0,255), flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
plot_images(matches_drawn)

left_pts = []
right_pts = []
for m in matches[:100]:
    l = kpts[0][m.queryIdx].pt
    r = kpts[1][m.trainIdx].pt
    left_pts.append(l)
    right_pts.append(r)

M, _ = cv2.findHomography(np.float32(right_pts), np.float32(left_pts))
dim_x = images[0].shape[1] + images[1].shape[1]
dim_y = max(images[0].shape[0]+100, images[1].shape[0]+100)
dim = (dim_x, dim_y)

warped = cv2.warpPerspective(images[1], M, dim)
plot_images(warped)
comb = warped.copy()
# combinar las dos imagenes
comb[0:images[0].shape[0],0:images[0].shape[1]] = images[0]
# crop
r_crop = 1300
comb = comb[:, :r_crop]
plot_images(comb)

plt.show()
