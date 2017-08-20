import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import glob
import ntpath

FILE_PATTERN = '/home/addo/dev/cbd/images/*.png'
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 75

files = glob.glob(FILE_PATTERN)
titles = []
images = []

for f in files:
    filename = ntpath.basename(f)
    img = cv2.imread(f,0)
    crop_img = img[10: 70, 55:250]
    titles.append(filename)
    images.append(crop_img)

# img = cv2.imread(file_name,0)

# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [crop_img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(len(files)):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
