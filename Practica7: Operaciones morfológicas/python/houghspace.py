from matplotlib import cm
from skimage.transform import (hough_line, hough_line_peaks)
import numpy as np
import matplotlib.pyplot as plt

# Construir imagen de muestra.
image = np.zeros((100, 100))
idx = np.arange(25, 75)
image[idx[::-1], idx] = 255
image[idx, idx] = 255

# Transformada de hough
h, theta, d = hough_line(image)

# Generar subplot
fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(12, 6))
plt.tight_layout()

ax0.imshow(image, cmap=cm.gray)
ax0.set_title('Fuente')

ax1.imshow(np.log(1 + h), extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]),d[-1], d[0]], cmap=cm.gray)
#ax1.imshow(h)
ax1.set_title('TH')
ax1.set_xlabel('Angulo (grados)')
ax1.set_ylabel('Distancia (pixeles)')
ax1.axis('image')

ax2.imshow(image, cmap=cm.gray)
row1, col1 = image.shape
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - col1 * np.cos(angle)) / np.sin(angle)
    ax2.plot((0, col1), (y0, y1), '-r')
ax2.axis((0, col1, row1, 0))
ax2.set_title('Lineas detectadas')
ax2.set_axis_off()

plt.show()