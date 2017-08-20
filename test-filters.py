import cv2
import numpy as np
from matplotlib import pyplot as plt

file_name = '/home/addo/dev/cbd/images/1it21.png'
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 75

img = cv2.imread(file_name,0)


x = int(7 * 8.15)
y = int(1 * 8.15)
w = int(4 * 8.15)
h = int(5 * 8.15)

print 'x {0}, y {1}, w {2}, h {3}'.format(x, y, w, h)

# crop_img = img[y: y + h, x: x + w]
# cv2.imshow("cropped", crop_img)
# cv2.waitKey(0)
crop_img = img[10: 55, 95:250]


ret,thresh1 = cv2.threshold(img,IMAGE_WIDTH,IMAGE_HEIGHT,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,IMAGE_WIDTH,IMAGE_HEIGHT,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,IMAGE_WIDTH,IMAGE_HEIGHT,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,IMAGE_WIDTH,IMAGE_HEIGHT,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,IMAGE_WIDTH,IMAGE_HEIGHT,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [crop_img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
